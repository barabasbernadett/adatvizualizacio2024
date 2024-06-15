import streamlit as st
import pandas as pd

df = pd.read_csv('dataset/creditcard_eligibility_dataset.csv')

st.title('Credit Card Eligibility')
st.write(df)