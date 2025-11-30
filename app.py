from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

print("🔄 Loading model...")
model = joblib.load("nslkdd_sklearn_model.joblib")
print("✅ Model loaded successfully!")

# Feature names (41 features - without label)
feature_names = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

categorical_features = ['protocol_type', 'service', 'flag']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        feature_values = data.get("features", [])

        if len(feature_values) != 41:
            return jsonify({"error": f"Expected 41 features, got {len(feature_values)}"}), 400

        feature_dict = {}
        for name, val in zip(feature_names, feature_values):
            if name in categorical_features:
                feature_dict[name] = val
            else:
                try:
                    feature_dict[name] = float(val)
                except ValueError:
                    return jsonify({"error": f"Invalid value for {name}: {val}"}), 400

        X = pd.DataFrame([feature_dict])
        X = X[feature_names]

        prediction = model.predict(X)[0]
        proba = model.predict_proba(X)[0]

        result = {
            "prediction": "Normal" if prediction == 0 else "Neptune",
            "confidence": round(max(proba) * 100, 2),
            "probabilities": {
                "normal": round(proba[0] * 100, 2),
                "neptune": round(proba[1] * 100, 2)
            }
        }
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "message": "Neptune vs Normal Detector API"
    })

if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:8000")
    app.run(debug=True, host='0.0.0.0', port=8000)
