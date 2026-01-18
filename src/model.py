import os
import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv("DB_PASSWORD"), 
    'database': 'credit_risk_db'
}

def training():
    print("Loading Data from SQL...")
    conn = mysql.connector.connect(**DB_CONFIG)
    query = """SELECT * FROM customers c JOIN loans l ON c.customer_id = l.customer_id"""
    d = pd.read_sql_query(query,conn)
    conn.close()

    print("Cleaning and formatting data...")
    d=d.drop(columns=['customer_id','loan_id','unnamed:0'],errors='ignore')

    label_encoders={}
    for col in d.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        d[col] = le.fit_transform(d[col])
        label_encoders[col] = le

    X = d.drop(columns=['Risk'])
    y = d['Risk']

    print("Training the model...")

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train,y_train)

    print("Testing Accuracy...")
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test,predictions)
    print(f"Model Accuracy :{accuracy:.2%}")

    print("Saving The Model...")
    dataToSave = {
        "model":model,
        "encoders":label_encoders
    }
    os.makedirs("models", exist_ok=True)
    joblib.dump(dataToSave, 'models/credit_risk_model.pkl')
    print("Model saved as credit_risk_model.pkl")

if __name__ == "__main__":
    training()