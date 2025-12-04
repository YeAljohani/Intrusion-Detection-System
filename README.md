# Intrusion Detection System (Attack vs Normal)

A compact educational IDS that uses a Random Forest trained on the NSL-KDD dataset to classify network connections as either Normal or Attack (SYN Flood DoS). The model and encoders are saved and served via a Flask API for real-time predictions.

Quick overview
- Model: RandomForestClassifier (n_estimators=100, class_weight='balanced').
- Labels: normal → 0, attack → 1.
- Encoders: LabelEncoder for protocol_type, service, flag.
- Saved artifacts: rf_neptune_normal_model.pkl, label_encoders.pkl.

Quickstart
1. Install dependencies:
   pip install -r requirements.txt
2. Train (example):
   python train.py --train data/KDDTrain+.txt --test data/KDDTest+.txt --out-dir models
3. Run API:
   python app.py
   By default the Flask app listens on http://127.0.0.1:5000
   
<img width="1470" height="956" alt="Screenshot 1447-06-13 at 5 02 43 AM" src="https://github.com/user-attachments/assets/b45cffdc-3f47-4086-99ed-8c7977a0d583" />

API
- GET /health
  - Returns 200 when the server is up.
- POST /predict
  - Body: {"features": [f1, f2, ..., f41]} — 41 NSL-KDD features in order (numeric values for numeric features; strings for categorical).
  - Response example:
    {
      "prediction": "Normal",
      "confidence": 97.3,
      "probabilities": {"normal": 97.3, "attack": 2.7}
    }
<img width="1470" height="956" alt="Screenshot 1447-06-13 at 5 08 57 AM" src="https://github.com/user-attachments/assets/25aa64ae-3949-4b1b-b205-fb66fe578f0b" />


## Training & Experimentation Notebook

The `training/` directory contains all experimental work performed during the model development process, including:

- Data cleaning and preprocessing steps  
- Exploratory Data Analysis (EDA)  
- Label encoding trials  
- Multiple model experiments (Random Forest, AutoML, XGBoost, etc.)  
- Performance comparison (Normal vs Attack → Normal vs Neptune)  
- Final model selection and evaluation  

The full workflow is documented in the notebook:
training/IDS_model_experiments.ipynb


This notebook shows every attempt, decision, and result that led to the final deployed model used in the API.


