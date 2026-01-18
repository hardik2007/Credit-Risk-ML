# Credit Risk ML Project

This project is an end-to-end credit risk prediction system built using Python and machine learning.

The goal of the project is to simulate how financial institutions assess the risk associated with lending money to customers, using structured customer and loan data.

---

## Project Overview

The project covers the complete machine learning workflow:
- Loading raw data into a MySQL database
- Preprocessing and cleaning data
- Encoding categorical features
- Training a machine learning model
- Saving the trained model and encoders
- Using the saved model for future predictions

The focus of the project is correctness, clarity, and understanding of the ML pipeline rather than heavy optimization.

---

## Project Structure


---

## Data Flow

1. Raw data is read from a CSV file.
2. The data is loaded into a MySQL database using `build_db.py`.
3. Data is fetched from the database for training.
4. Categorical features are encoded using Label Encoding.
5. A Random Forest classifier is trained to predict credit risk.
6. The trained model and encoders are saved using Joblib.

---

## Machine Learning Model

- Algorithm: Random Forest Classifier
- Train/Test Split: 80/20
- Evaluation Metric: Accuracy

Encoders used during training are saved along with the model to ensure consistent preprocessing during inference.

---

## Security Note

Database credentials are **not hardcoded** in the source code.  
The MySQL password is read from an environment variable (`DB_PASSWORD`) to avoid exposing sensitive information.

---

## Technologies Used

- Python
- Pandas
- Scikit-learn
- MySQL
- Joblib

---

## Author

Hardik Bhagtani  
BTech Computer Science Engineering (First Year)
