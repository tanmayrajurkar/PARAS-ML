# Paras ML Models

## Overview
Paras (Parking Automation and Reservation Analytics System) uses machine learning models to optimize parking management through real-time detection, prediction, and analytics. This repository documents the ML models integrated into the system.

## Features
- **Vehicle Detection**: Identifies and classifies vehicles using computer vision.
- **Parking Slot Availability Prediction**: Predicts available slots using time-series data and sensor inputs.
- **License Plate Recognition (LPR)**: Extracts license plate numbers using OCR.
- **Anomaly Detection**: Detects illegal parking, unauthorized access, and unusual activities.
- **Dynamic Pricing Optimization**: Recommends pricing based on demand and occupancy trends.

## Model Details

### 1. **Vehicle Detection Model**
- **Algorithm**: YOLOv8 (You Only Look Once)
- **Training Data**: COCO dataset + custom annotated parking images
- **Input**: CCTV camera feed
- **Output**: Bounding boxes and vehicle classifications
- **Dependencies**:
  - `ultralytics`
  - `opencv-python`
  - `torch`

### 2. **Parking Slot Availability Prediction**
- **Algorithm**: LSTM (Long Short-Term Memory)
- **Training Data**: Historical occupancy data, weather conditions, and traffic patterns
- **Input**: Time-series occupancy data
- **Output**: Probability of slot availability at a future timestamp
- **Dependencies**:
  - `tensorflow`
  - `pandas`
  - `numpy`

### 3. **License Plate Recognition (LPR)**
- **Algorithm**: CRNN (Convolutional Recurrent Neural Network) + Tesseract OCR
- **Training Data**: OpenLPR dataset
- **Input**: Cropped vehicle license plate image
- **Output**: Extracted text (license plate number)
- **Dependencies**:
  - `pytesseract`
  - `opencv-python`
  - `torch`

### 4. **Anomaly Detection Model**
- **Algorithm**: Autoencoder + Isolation Forest
- **Training Data**: Normal vs. abnormal parking behaviors
- **Input**: Surveillance footage and parking history logs
- **Output**: Anomaly scores and detected suspicious activity
- **Dependencies**:
  - `scikit-learn`
  - `tensorflow`
  - `numpy`

### 5. **Dynamic Pricing Optimization**
- **Algorithm**: Reinforcement Learning (Deep Q-Networks)
- **Training Data**: Historical pricing trends, occupancy rates, and external factors (e.g., weather, events)
- **Input**: Current occupancy and demand levels
- **Output**: Recommended pricing strategy
- **Dependencies**:
  - `gym`
  - `stable-baselines3`
  - `pandas`

## Installation
To set up the ML models, clone the repository and install the required dependencies:
```bash
# Clone the repository
git clone https://github.com/your-repo/paras-ml.git
cd paras-ml

# Install dependencies
pip install -r requirements.txt
```

## Usage
Each model is structured as a separate module. To run a specific model, use the following:
```bash
python vehicle_detection.py
```
For real-time deployment, integrate the models into the main Paras system using APIs or microservices.

## Live Demo
Check out the live demo here: [Live Demo](https://drive.google.com/file/d/1wX-IE_uASCK0FSwwlkYFGm_ZgvDI3HLo/view?usp=sharing)

## Contributors
- **Prasanna Pal** (CTO) - ML development and optimization
- **Chinmay Bhat** (CIO) - Hardware integration and sensor data handling

## License
This project is licensed under the MIT License.

---

For further inquiries, contact us at [your-email@paras.com](mailto:your-email@paras.com).
