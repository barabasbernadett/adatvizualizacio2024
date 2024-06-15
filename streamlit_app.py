import streamlit as streamlit
import pandas as pandas

df = pd.read_csv('dataset/creditcard_eligibility_dataset.csv')

st.title('Credit Card Eligibility')
st.write(df)