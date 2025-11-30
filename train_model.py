
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import requests
from io import StringIO


url_train = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt"
url_test  = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt"

columns = [
    'duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent',
    'hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root',
    'num_file_creations','num_shells','num_access_files','num_outbound_cmds','is_host_login','is_guest_login',
    'count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate',
    'diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count','dst_host_same_srv_rate',
    'dst_host_diff_srv_rate','dst_host_same_src_port_rate','dst_host_srv_diff_host_rate','dst_host_serror_rate',
    'dst_host_srv_serror_rate','dst_host_rerror_rate','dst_host_srv_rerror_rate','label','difficulty'
]

r = requests.get(url_train)
r.raise_for_status()
train = pd.read_csv(StringIO(r.text), names=columns)

r = requests.get(url_test)
r.raise_for_status()
test = pd.read_csv(StringIO(r.text), names=columns)

train = train[train['label'].isin(['normal', 'neptune'])]
test  = test[test['label'].isin(['normal', 'neptune'])]


train['label'] = train['label'].map({'normal': 0, 'neptune': 1})
test['label']  = test['label'].map({'normal': 0, 'neptune': 1})

categorical_cols = ['protocol_type', 'service', 'flag']

le_dict = {}
for col in categorical_cols:
    le = LabelEncoder()
    train[col] = le.fit_transform(train[col])
    test[col]  = test[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else 0)
    le_dict[col] = le

X_train = train.drop(['label', 'difficulty', 'num_outbound_cmds'], axis=1, errors='ignore')
y_train = train['label']

X_test  = test.drop(['label', 'difficulty', 'num_outbound_cmds'], axis=1, errors='ignore')
y_test  = test['label']

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'
)
rf.fit(X_train, y_train)


y_pred = rf.predict(X_test)

print(f"✅ Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%\n")
print(classification_report(y_test, y_pred, target_names=['normal','neptune']))

import joblib
joblib.dump(rf, "rf_neptune_normal_model.pkl")
print("Model saved as rf_neptune_normal_model.pkl")
joblib.dump(le_dict, "label_encoders.pkl")
