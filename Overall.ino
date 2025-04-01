const int trigPin1 = 2;
const int echoPin1 = 3;

const int trigPin2 = 4;
const int echoPin2 = 5;

const int distanceThreshold = 20;

void setup() {
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);

  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);

  Serial.begin(9600);
}

long measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);

  long distance = duration * 0.034 / 2;
  return distance;
}

void loop() {
  long distance1 = measureDistance(trigPin1, echoPin1);
  Serial.print("Distance Sensor 1: ");
  Serial.print(distance1);
  Serial.println(" cm");

  if (distance1 < distanceThreshold && distance1 > 0) {
    Serial.println("Parking Spot 1: Occupied");
  } else {
    Serial.println("Parking Spot 1: Empty");
  }

  long distance2 = measureDistance(trigPin2, echoPin2);
  Serial.print("Distance Sensor 2: ");
  Serial.print(distance2);
  Serial.println(" cm");

  if (distance2 < distanceThreshold && distance2 > 0) {
    Serial.println("Parking Spot 2: Occupied");
  } else {
    Serial.println("Parking Spot 2: Empty");
  }

  delay(2000);
}
