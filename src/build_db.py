import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv("DB_PASSWORD"), 
    'database': 'credit_risk_db'
}
CSV_PATH = "../data/raw_data.csv"

def create_database():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' is ready.")
        conn.close()
    except Error as e:
        print(f"Connection Failed: {e}")
        exit()

def build_tables_and_load_data():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        conn.autocommit = True 

        try:
            df = pd.read_csv(CSV_PATH)
            df = df.fillna("Unknown")
            print(f"Loaded CSV with {len(df)} rows.")
        except FileNotFoundError:
            print("Error: Could not find raw_data.csv. Check the data folder!")
            exit()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            Age INT,
            Sex VARCHAR(10),
            Job INT,
            Housing VARCHAR(20),
            Saving_accounts VARCHAR(50),
            Checking_account VARCHAR(50)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            Credit_amount INT,
            Duration INT,
            Purpose VARCHAR(50),
            Risk VARCHAR(10),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        """)
        print("SQL Tables created successfully.")

        print("Inserting data...")

        cursor.execute("TRUNCATE TABLE loans")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0") 
        cursor.execute("TRUNCATE TABLE customers")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO customers (Age, Sex, Job, Housing, Saving_accounts, Checking_account)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['Age'], row['Sex'], row['Job'], row['Housing'], row['Saving accounts'], row['Checking account']))
            
            new_customer_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO loans (customer_id, Credit_amount, Duration, Purpose, Risk)
                VALUES (%s, %s, %s, %s, %s)
            """, (new_customer_id, row['Credit amount'], row['Duration'], row['Purpose'], row['Risk']))

        print("SUCCESS! Pipeline Complete. Data is now in MySQL.")
        conn.close()

    except Error as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    create_database()
    build_tables_and_load_data()