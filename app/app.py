import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Credit Risk Engine", page_icon=None)

@st.cache_resource
def load_model():
    try:
        data = joblib.load('models/credit_risk_model.pkl')
        return data['model'], data['encoders']
    except FileNotFoundError:
        return None, None

model, encoders = load_model()

if model is None:
    st.error("Model file not found! Please run 'train_model.py' first.")
    st.stop()

st.sidebar.header("User Input Features")

def user_input_features():
    age = st.sidebar.number_input("Age (Years)", min_value=18, max_value=100, value=30)
    credit_amount = st.sidebar.number_input("Credit Amount ($)", min_value=100, max_value=20000, value=5000)
    duration = st.sidebar.number_input("Loan Duration (Months)", min_value=6, max_value=72, value=24)
    job_map = {
        "Unskilled (Non-resident)": 0,
        "Unskilled (Resident)": 1,
        "Skilled Employee": 2,
        "Highly Skilled / Management": 3
    }
    selected_job = st.sidebar.selectbox("Job Category", list(job_map.keys()))
    job = job_map[selected_job]

    sex = st.sidebar.selectbox('Sex', encoders['Sex'].classes_)
    housing = st.sidebar.selectbox('Housing', encoders['Housing'].classes_)
    saving_accounts = st.sidebar.selectbox('Saving Accounts', encoders['Saving_accounts'].classes_)
    checking_account = st.sidebar.selectbox('Checking Account', encoders['Checking_account'].classes_)
    purpose = st.sidebar.selectbox('Purpose', encoders['Purpose'].classes_)

    data = {
        'Age': age,
        'Sex': sex,
        'Job': job, 
        'Housing': housing,
        'Saving_accounts': saving_accounts,
        'Checking_account': checking_account,
        'Credit_amount': credit_amount,
        'Duration': duration,
        'Purpose': purpose
    }
    
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

st.title("Credit Risk Assessment")
st.write("This application predicts the risk of a loan default using Machine Learning.")

st.subheader("Customer Profile")

display_df = input_df.T
display_df.columns = ["User Details"]
display_df.index.name = "Feature"
st.table(display_df)

if st.button("Calculate Risk"):
    
    processed_df = input_df.copy()
    for col in processed_df.columns:
        if col in encoders: 
            le = encoders[col]
            processed_df[col] = le.transform(processed_df[col])

    prediction = model.predict(processed_df)
    probability = model.predict_proba(processed_df)

    st.subheader("Risk Prediction")
    
    if prediction[0] == 0:
        st.error("HIGH RISK (Bad Credit)")
        st.write(f"Confidence: {probability[0][0]:.2%}")
    else:
        st.success("LOW RISK (Good Credit)")
        st.write(f"Confidence: {probability[0][1]:.2%}")