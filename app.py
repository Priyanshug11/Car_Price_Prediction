import streamlit as st
import pandas as pd
import pickle
import time
import os
from pathlib import Path

# Option 1: Relative path
model_path = Path(__file__).parent / 'model.pkl'

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Car Price Prediction", page_icon="🚗", layout="wide")

# ================= LOAD MODEL =================
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
body {
    background-color: #fafafa;
}
.header {
    font-size: 42px;
    font-weight: bold;
    color: #e23744;
}
.subheader {
    font-size: 18px;
    color: #555;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.08);
}
.predict-box {
    background: linear-gradient(135deg, #ff4b2b, #ff416c);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}
.stButton>button {
    background: linear-gradient(135deg, #ff4b2b, #ff416c);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ================= ALLOWED MODELS =================
ALLOWED_MODELS = [
'Alto', 'Grand', 'i20', 'Ecosport', 'Wagon R', 'i10', 'Venue',
'Swift', 'Verna', 'Duster', 'Ciaz', 'Baleno', 'Swift Dzire',
'Vento', 'Creta', 'City', 'KWID', 'Amaze', 'Santro', 'Bolero',
'KUV100', 'Ignis', 'RediGO', 'Scorpio', 'Marazzo', 'Aspire',
'Figo', 'Vitara', 'Tiago', 'Polo', 'Seltos', 'Celerio', 'GO',
'KUV', 'Jazz', 'Tigor', 'Ertiga', 'Eeco', 'Civic', 'XUV500',
'Hector', 'Rapid', 'Freestyle', 'Nexon', 'XUV300', 'Superb',
'Dzire VXI', 'WR-V', 'Triber', 'Elantra', 'Yaris', 'S-Presso',
'A4', 'Safari', 'Harrier', 'Octavia', 'Cooper', 'CR-V', 'Innova'
]

# ================= VALIDATION FUNCTION =================
def validate_input(data):
    errors = []

    if data['vehicle_age'] < 0:
        errors.append("Vehicle age cannot be negative")

    if data['km_driven'] < 0:
        errors.append("KM driven cannot be negative")

    if data['mileage'] <= 0:
        errors.append("Mileage must be greater than 0")

    if data['engine'] <= 0:
        errors.append("Engine must be greater than 0")

    if data['max_power'] <= 0:
        errors.append("Max power must be greater than 0")

    if data['model'] not in ALLOWED_MODELS:
        errors.append("Invalid car model!")

    if data['fuel_type'] not in ['Petrol', 'Diesel', 'CNG','Electric','LPG']:
        errors.append("Invalid fuel type")

    if data['seller_type'] not in ['Dealer', 'Individual','Trustmark Dealer']:
        errors.append("Invalid seller type")

    if data['transmission_type'] not in ['Manual', 'Automatic']:
        errors.append("Invalid transmission type")

    if data['seats'] not in [4, 5,6, 7, 8,9]:
        errors.append("Seats must be 4,5,6,7,8,9")

    return errors

# ================= HERO SECTION =================
col1, col2 = st.columns([2,1])

with col1:
    st.markdown('<div class="header">🚗 Car Price Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Are You planning to sell your Car!?</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">So Lets try evaluating the Price.</div>', unsafe_allow_html=True)

# ================= MAIN CARD =================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        model_name = st.selectbox("Car Model", ALLOWED_MODELS)
        vehicle_age = st.slider("Vehicle Age", 0, 30, 5)
        km_driven = st.number_input("KM Driven", min_value=0, value=150000)
        seller_type = st.selectbox("Seller Type", ["Dealer", "Individual","Trustmark Dealer"])

    with col2:
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG","LPG","Electric"])
        transmission_type = st.selectbox("Transmission", ["Manual", "Automatic"])
        mileage = st.number_input("Mileage", min_value=5.0, max_value=35.0)
        engine = st.number_input("Engine (CC)", min_value=700, max_value=2100)

    max_power = st.slider("Max Power", 35.0, 200.0, 20.0)
    seats = st.selectbox("Seats", [4, 5,6, 7,8, 9])

    st.write("")

    # ================= PREDICTION =================
    if st.button("🚀 Predict Price"):

        new_data = pd.DataFrame([{
            'model': model_name,
            'vehicle_age': vehicle_age,
            'km_driven': km_driven,
            'seller_type': seller_type,
            'fuel_type': fuel_type,
            'transmission_type': transmission_type,
            'mileage': mileage,
            'engine': engine,
            'max_power': max_power,
            'seats': seats
        }])

        input_data = new_data.iloc[0].to_dict()
        errors = validate_input(input_data)

        if errors:
            for err in errors:
                st.error(err)
        else:
            try:
                with st.spinner("Calculating best price..."):
                    time.sleep(1)

                prediction = model.predict(new_data)

                st.markdown(f"""
                    <div class="predict-box">
                        💰 ₹ {int(prediction[0]):,}
                        <br><span style="font-size:16px;">Estimated Resale Value</span>
                    </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)