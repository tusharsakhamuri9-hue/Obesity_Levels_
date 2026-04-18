import streamlit as st
import pickle
import pandas as pd
import joblib
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Obesity Prediction", layout="wide")

# -----------------------------
# Load Model
# -----------------------------

model_path = os.path.join(os.path.dirname(__file__), "bestmodel.pkl")
model = joblib.load(model_path)

# -----------------------------
# Custom CSS (UI Styling)
# -----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #2c3e50;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    .box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.markdown('<p class="title">🧠 Obesity Prediction App</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your lifestyle details to predict obesity level</p>', unsafe_allow_html=True)

# -----------------------------
# Layout (2 Columns)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Personal Info")
    age = st.number_input("Age", 1, 100, 25)
    height = st.number_input("Height (meters)", 1.0, 2.5, 1.7)
    weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    st.markdown("### 🥗 Lifestyle")
    calc = st.selectbox("Alcohol", ["no", "Sometimes", "Frequently"])
    favc = st.selectbox("High Calorie Food", ["yes", "no"])
    fcvc = st.slider("Vegetable Intake", 1.0, 3.0, 2.0)
    ncp = st.slider("Meals per Day", 1.0, 5.0, 3.0)
    ch2o = st.slider("Water Intake", 1.0, 5.0, 2.0)
    faf = st.slider("Physical Activity", 0.0, 10.0, 2.0)

# Extra section
st.markdown("### ⚙️ Other Factors")
col3, col4 = st.columns(2)

with col3:
    scc = st.selectbox("Monitor Calories", ["yes", "no"])
    smoke = st.selectbox("Smoking", ["yes", "no"])
    family = st.selectbox("Family History", ["yes", "no"])

with col4:
    tue = st.slider("Screen Time", 0.0, 10.0, 2.0)
    caec = st.selectbox("Snacking", ["no", "Sometimes", "Frequently", "Always"])
    mtrans = st.selectbox("Transport", ["Walking", "Public_Transportation", "Automobile"])

# -----------------------------
# Prediction Button
# -----------------------------
st.markdown("---")
if st.button("🚀 Predict Obesity Level"):

    bmi = weight / (height ** 2)

    input_data = pd.DataFrame([{
        "Age": age,
        "Gender": gender,
        "CALC": calc,
        "FAVC": favc,
        "FCVC": fcvc,
        "NCP": ncp,
        "SCC": scc,
        "SMOKE": smoke,
        "CH2O": ch2o,
        "family_history_with_overweight": family,
        "FAF": faf,
        "TUE": tue,
        "CAEC": caec,
        "MTRANS": mtrans,
        "BMI": float(bmi)
    }])

    prediction = model.predict(input_data)

    # -----------------------------
    # Output Section
    # -----------------------------
    st.markdown("### 🎯 Result")

    st.success(f"Predicted Obesity Level: {prediction[0]}")

    st.info(f"Your BMI: {round(bmi, 2)}")

    # BMI Category
    if bmi < 18.5:
        st.warning("Category: Underweight")
    elif bmi < 25:
        st.success("Category: Normal")
    elif bmi < 30:
        st.warning("Category: Overweight")
    else:
        st.error("Category: Obese")