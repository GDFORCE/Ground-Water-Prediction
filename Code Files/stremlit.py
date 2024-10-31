import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb

@st.cache_resource
def load_model():
    model = xgb.Booster()
    model.load_model('model.json')
    return model

xg_model = load_model()


@st.cache_data
def load_data():
    return pd.read_csv('DWLR_Dataset_2023.csv')

data = load_data()


numeric_features = data.select_dtypes(include=[np.number]).columns.tolist()

st.title("DWLR Sensor Data Prediction App")
st.write("Dataset preview:")
st.write(data.head())

st.sidebar.header("Input Features")
user_input = {}
for feature in numeric_features:
    default_value = float(data[feature].mean())
    user_input[feature] = st.sidebar.text_input(f"{feature}", value=str(default_value))


input_df = pd.DataFrame([{feature: float(user_input[feature]) for feature in numeric_features}])
d_matrix = xgb.DMatrix(input_df)


if st.button("Predict"):
    prediction = xg_model.predict(d_matrix)
    st.write("Prediction:", prediction[0])
