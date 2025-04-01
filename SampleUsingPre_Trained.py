import serial
import threading
import cv2
import pytesseract
from ultralytics import YOLO
from supabase import create_client
import time
import winsound

SUPABASE_URL = "https://ipmshfkymnflueddojcw.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwbXNoZmt5bW5mbHVlZGRvamN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE5NDU0NzAsImV4cCI6MjA0NzUyMTQ3MH0.CIAqAEJ_aV5OIbyCKEShSljutfYdmGR67tvpVgO1gUc"
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

arduino = serial.Serial('COM10', 9600, timeout=1)  

model_plate = YOLO(r"D:\Integration\NUMBER PLATE MODEL\roboflow\runs\detect\train\weights\best.pt")

model_car = YOLO('yolov8n.pt') 

slot_1_occupied = False
slot_2_occupied = False
car_detected_in_slot_1 = False
car_detected_in_slot_2 = False
animal_detected_in_slot_1 = False
animal_detected_in_slot_2 = False

def insert_to_test_table(plate_text):
    response = supabase.table("test").insert({"plate": plate_text, "timestamp": "NOW()"}).execute()
    if response.data:
        print(f"Plate '{plate_text}' inserted successfully into the test table.")
    else:
        print(f"Failed to insert plate '{plate_text}': {response.get('error', 'Unknown Error')}")

def update_parking_status(slot_number, status): 
    response = supabase.table("parking_spots").update({"status": status, "timestamp": "NOW()"}).eq("slot_number", slot_number).execute()
    if response.data:
        print(f"Slot {slot_number} status updated to: {status}")
    else:
        print(f"Failed to update Slot {slot_number}: {response.get('error', 'Unknown Error')}")

def detect_number_plate():
    cap_plate = cv2.VideoCapture(0)  
    while True:
        ret, frame = cap_plate.read()
        if not ret:
            print("Failed to capture frame from webcam.")
            break

        results_plate = model_plate(frame)  

        for result in results_plate:
            boxes = result.boxes.xyxy  # Bounding box coordinates
            confidences = result.boxes.conf  # Confidence values
            class_ids = result.boxes.cls  # Class IDs of the detected objects

            # Assuming class_id 0 corresponds to the number plates class
            for i, class_id in enumerate(class_ids):
                if class_id == 0:  # Class ID for number plate (if that's how it's trained)
                    x1, y1, x2, y2 = map(int, boxes[i])
                    confidence = confidences[i]

                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, f"Plate {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    # Extract the detected number plate text using OCR if desired
                    # Crop the image of the number plate for OCR processing
                    cropped_plate = frame[y1:y2, x1:x2]
                    plate_text = pytesseract.image_to_string(cropped_plate, config="--psm 7").strip()

                    if plate_text:
                        print(f"Detected Plate: {plate_text}")
                        insert_to_test_table(plate_text)

                        cap_plate.release()
                        cv2.destroyAllWindows()
                        return plate_text

        cv2.imshow("Number Plate Detection Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_plate.release()
    cv2.destroyAllWindows()
    return None

def detect_car_webcam2():
    global car_detected_in_slot_1, car_detected_in_slot_2, animal_detected_in_slot_1, animal_detected_in_slot_2
    cap_car = cv2.VideoCapture(1)  
    while True:
        ret, frame = cap_car.read()
        if not ret:
            print("Failed to capture frame from webcam.")
            break

        results_car = model_car(frame)  

        for result in results_car:
            boxes = result.boxes.xyxy  # Bounding box coordinates
            confidences = result.boxes.conf  # Confidence values
            class_ids = result.boxes.cls  # Class IDs of the detected objects

            for i, class_id in enumerate(class_ids):
                if class_id == 2:  # Class ID for "car" in COCO dataset is 2
                    x1, y1, x2, y2 = map(int, boxes[i])
                    confidence = confidences[i]
                    
                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"Car {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    if slot_1_occupied:
                        car_detected_in_slot_1 = True
                        print("Car detected in Slot 1")
                    if slot_2_occupied:
                        car_detected_in_slot_2 = True
                        print("Car detected in Slot 2")
                
                elif class_id == 16:  # Assuming class ID for "animal" is 16
                    if slot_1_occupied:
                        animal_detected_in_slot_1 = True
                        print("Animal detected in Slot 1")
                    if slot_2_occupied:
                        animal_detected_in_slot_2 = True
                        print("Animal detected in Slot 2")

        # Display the frame with detections
        cv2.imshow("Car Detection Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_car.release()
    cv2.destroyAllWindows()

def listen_to_arduino():
    global slot_1_occupied, slot_2_occupied
    while True:
        if arduino.in_waiting > 0:
            try:
                sensor_data = arduino.readline().decode('utf-8').strip()
                print(f"Raw Arduino data: {sensor_data}")

                if "Slot 1" in sensor_data:
                    if "Slot 1 is occupied" in sensor_data:
                        slot_1_occupied = True
                        if car_detected_in_slot_1:
                            update_parking_status(1, "Occupied")
                            print("Slot 1 is occupied by vehicle")
                        else:
                            print("⚠️ Unknown object detected in Slot 1!")
                            winsound.Beep(2500, 1000)  # Higher frequency beep for 1 second
                    elif "Slot 1 is available" in sensor_data:
                        slot_1_occupied = False
                        update_parking_status(1, "Available")
                        print("Slot 1 is available")
                    check_slot_status(1)

                if "Slot 2" in sensor_data:
                    if "Slot 2 is occupied" in sensor_data:
                        slot_2_occupied = True
                        if car_detected_in_slot_2:
                            update_parking_status(2, "Occupied")
                            print("Slot 2 is occupied by vehicle")
                        else:
                            print("⚠️ Unknown object detected in Slot 2!")
                            winsound.Beep(2500, 1000)  # Higher frequency beep for 1 second
                    elif "Slot 2 is available" in sensor_data:
                        slot_2_occupied = False
                        update_parking_status(2, "Available")
                        print("Slot 2 is available")
                    check_slot_status(2)

            except UnicodeDecodeError:
                print("Error reading Arduino data")
                continue

        time.sleep(0.1)

# Function to check slot status and detect if a car or unknown object is occupying the slot
def check_slot_status(slot_number):
    global slot_1_occupied, slot_2_occupied, car_detected_in_slot_1, car_detected_in_slot_2, animal_detected_in_slot_1, animal_detected_in_slot_2
    
    if slot_number == 1:
        if slot_1_occupied:
            if car_detected_in_slot_1:
                print("Car has been detected in Slot 1")
            elif animal_detected_in_slot_1:
                print("Animal detected in Slot 1")
                print("Activate buzzer!!!")
                update_parking_status(1, "Available")
            elif not car_detected_in_slot_1:  # No car and no animal
                print("No car detected in Slot 1")
                update_parking_status(1, "Available")
        car_detected_in_slot_1 = False  # Reset detection for next cycle
        animal_detected_in_slot_1 = False  # Reset detection for next cycle

    elif slot_number == 2:
        if slot_2_occupied:
            if car_detected_in_slot_2:
                print("Car has been detected in Slot 2")
            elif animal_detected_in_slot_2:
                print("Animal detected in Slot 2")
                print("Activate buzzer!!!")
                update_parking_status(2, "Available")
            elif not car_detected_in_slot_2:  # No car and no animal
                print("No car detected in Slot 2")
                update_parking_status(2, "Available")
        car_detected_in_slot_2 = False  # Reset detection for next cycle
        animal_detected_in_slot_2 = False  # Reset detection for next cycle

if __name__ == "__main__":
    # Start the number plate detection first
    detected_plate = detect_number_plate()
    if detected_plate:
        print(f"Number plate detected: {detected_plate}")

        # After detecting the plate, start the car detection
        thread_webcam2 = threading.Thread(target=detect_car_webcam2, daemon=True)
        thread_webcam2.start()

        # Start the Arduino listening thread
        thread_arduino = threading.Thread(target=listen_to_arduino, daemon=True)
        thread_arduino.start()

        # Join threads to ensure they run continuously
        thread_webcam2.join()
        thread_arduino.join()
    else:
        print("No number plate detected.")
