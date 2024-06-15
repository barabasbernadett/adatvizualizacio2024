import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title='Interactive Data Explorer', page_icon='📊')
st.title('📊 Interactive Data Explorer')

df = pd.read_csv('dataset/creditcard_eligibility_dataset.csv')

st.title('Credit Card Eligibility')
st.write(df)

chart = alt.Chart()