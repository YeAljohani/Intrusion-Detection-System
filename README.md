🚀 Overview
<img<img width="1470" height="956" alt="Screenshot 1447-06-13 at 5 08 57 AM" src="https://github.com/user-attachments/assets/9be8c67a-5fc2-4eb4-a551-fff33d757d04" />
 width="1470" height="956" alt="Screenshot 1447-06-13 at 5 02 43 AM" src="https://github.com/user-attachments/assets/68116773-9a64-4a81-b406-8f6a174934c3" />
![Uploading Screenshot 1447-06-13 at 5.08.57 AM.png…]()

This project is a lightweight Intrusion Detection System (IDS) that uses a machine learning model to classify network connections as either:
Normal
Neptune Attack (SYN Flood DoS)
The system is built end-to-end:
Model Training → Random Forest on NSL-KDD dataset
Feature Encoding → LabelEncoder for protocol, service, and flags
Model Serving → Flask API for real-time prediction
Frontend Integration (optional) → HTML/JS UI that sends live traffic features
Confidence Score → Probability returned with each prediction
This design demonstrates how ML can be embedded into real-world cybersecurity detection pipelines.
🎯 Project Idea — What This Project Solves
Modern networks generate massive volumes of traffic. Security analysts cannot manually inspect every flow, and signature-based IDS systems (Snort, Suricata) often fail to detect unknown or variant attack patterns.
This project proposes a simple but effective idea:
Use a trained ML model to automatically classify network flows and detect Neptune (SYN Flood) attacks in real time.
Why this idea matters:
Shows how supervised ML can classify attack behavior using real features
Demonstrates how to embed a trained model inside a live API service
Provides an extendable base for multi-attack detection systems
Helps students & researchers understand practical IDS pipeline design
Your system acts like a minimal, educational version of:
Snort + Machine Learning Backend + Web API
🧠 Machine Learning Model
Dataset
Uses NSL-KDD (KDDTrain+ and KDDTest+), a popular benchmark dataset for IDS research.
Labels Used:
normal → 0
neptune → 1
Model:
RandomForestClassifier
100 trees
Balanced class weights
Trained on 41 input features
Encoders
Categorical features (protocol_type, service, flag) are encoded using LabelEncoder.
All encoders are saved to allow valid inference later.
⚙️ Model Training Pipeline
Download NSL-KDD training + testing data
Filter dataset to only normal and neptune classes
Encode categorical features
Train Random Forest
Evaluate accuracy
Save:
rf_neptune_normal_model.pkl
label_encoders.pkl
The training code is included inside the file for reproducibility.
🔌 API Architecture (Flask Server)
The Flask API loads the trained model and exposes:
Endpoints
/predict → POST
Accepts 41 features in order.
Returns:
{
  "prediction": "Normal",
  "confidence": 97.3,
  "probabilities": {
    "normal": 97.3,
    "neptune": 2.7
  }
}
/health → GET
Simple health-check endpoint.
/ → GET
Serves index.html (frontend UI).
📡 How Prediction Works
The client sends an array of 41 values:
{
  "features": [0, "tcp", "http", "SF", 300, 200, 0, ...]
}
The API:
Validates input
Converts numerical features
Leaves categorical strings unchanged
Creates a DataFrame
Calls:
model.predict()
model.predict_proba()
Then returns prediction + confidence.
