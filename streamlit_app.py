import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title='Credit Card Eligibility', page_icon='📊')
st.title('📊 Credit Card Eligibility')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  
st.subheader('Which Movie Genre performs ($) best at the box office?')


df = pd.read_csv('dataset/creditcard_eligibility_dataset.csv')
st.write(df)

# Create histogram for Age Distribution
age_hist = alt.Chart(df).mark_bar().encode(
    x=alt.X('Age:Q', bin=True, title='Age'),
    y='count()',
).properties(
    title='Distribution of Age',
    width=600,
    height=400
).interactive()

# Display Age Distribution Histogram
st.altair_chart(age_hist, use_container_width=True)

# Displaying gender distribution using a count bar chart
st.header('Gender Distribution')
gender_chart = alt.Chart(df).mark_bar().encode(
    alt.X('Gender:N', title='Gender'),
    alt.Y('count()', title='Number of Applicants'),
    tooltip=['Gender:N', 'count()']
).properties(
    title='Gender Distribution',
    width=700,
    height=400
).interactive()
st.altair_chart(gender_chart, use_container_width=True)

# # Csoportos oszlopdiagram létrehozása
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# for (family_status, years_employed), group in df.groupby(['Family_status', 'Years_employed']):
#     approval_counts = group['Target'].value_counts(normalize=True).sort_index()
#     approval_counts.plot(kind='bar', color=['green', 'red'], alpha=0.7, ax=ax, label=f"{family_status}, {years_employed} years")

# ax.set_xlabel('Family Status')
# ax.set_ylabel('Years Employed')
# ax.set_zlabel('Credit Approval')

# plt.legend()
# plt.title('Relationship between Family Status, Years Employed, Housing Type and Credit Approval')
# plt.tight_layout()

# plt.show()

# kodreszlet 2
import plotly.graph_objects as go

# Három dimenzió: Családi állapot, Évek a foglalkozásban, Lakóhely típusa
csaladi_allapot = df['Family_status'].unique()
evek_foglalkozasban = df['Years_employed'].unique()
lakohely_tipus = df['Housing_type'].unique()

# Hitelképesség színezés szerint
df['Color'] = df['Target'].replace({0: 'red', 1: 'green'})

# 3D Surface Plot létrehozása
fig = go.Figure(data=[go.Surface(
    x=df['Family_status'],
    y=df['Years_employed'],
    z=df['Housing_type'],
    colorscale='Viridis',  # Színskála beállítása
    colorbar=dict(title='Hitelképesség'),
)])

# Grafikon beállításai
fig.update_layout(
    title='Családi állapot, Évek a foglalkozásban és Lakóhely típusa közötti összefüggések hitelképességgel',
    scene=dict(
        xaxis_title='Családi állapot',
        yaxis_title='Évek a foglalkozásban',
        zaxis_title='Lakóhely típusa',
    )
)
st.plotly_chart(fig)

chart = alt.Chart()

# kodreszlet 3
import plotly.express as px
import streamlit as st

# Színezéshez a hitelképesség átnevezése
df['Hitelképesség'] = df['Target'].replace({0: 'Elutasított', 1: 'Jóváhagyott'})

# 1. Vizualizáció: Családi állapot, Évek a foglalkozásban és Lakóhely típusa
fig1 = px.scatter_3d(df, 
                     x='Family_status', 
                     y='Years_employed', 
                     z='Housing_type', 
                     color='Hitelképesség',
                     title='Családi állapot, Évek a foglalkozásban és Lakóhely típusa közötti összefüggések hitelképességgel',
                     labels={
                         'Family_status': 'Családi állapot',
                         'Years_employed': 'Évek a foglalkozásban',
                         'Housing_type': 'Lakóhely típusa',
                         'Hitelképesség': 'Hitelképesség'
                     },
                     color_discrete_map={'Jóváhagyott': 'green', 'Elutasított': 'red'}
                    )

# 2. Vizualizáció: Jövedelem, Végzettség és Évek a foglalkozásban
fig2 = px.scatter_3d(df, 
                     x='Total_income', 
                     y='Education_type', 
                     z='Years_employed', 
                     color='Hitelképesség',
                     title='Jövedelem, Végzettség és Évek a foglalkozásban közötti összefüggések hitelképességgel',
                     labels={
                         'Total_income': 'Jövedelem',
                         'Education_type': 'Végzettség',
                         'Years_employed': 'Évek a foglalkozásban',
                         'Hitelképesség': 'Hitelképesség'
                     },
                     color_discrete_map={'Jóváhagyott': 'green', 'Elutasított': 'red'}
                    )

# Streamlit oldalon való megjelenítés
st.plotly_chart(fig1)
st.plotly_chart(fig2)

#kodreszlet4
import pandas as pd
import plotly.express as px
import streamlit as st

# Hitelképesség megjelölése
df['Hitelképesség'] = df['Target'].replace({0: 'Elutasított', 1: 'Jóváhagyott'})

# Streamlit cím
st.title("Jövedelem típus és végzettség összefüggése hitelképesség alapján")

# Grouped Bar Chart létrehozása
fig = px.bar(
    df,
    x='Income_type',
    y='ID',  # Számolja meg az egyéneket
    color='Hitelképesség',
    barmode='group',
    facet_col='Education_type',
    labels={'ID': 'Egyének száma', 'Income_type': 'Jövedelem típus', 'Education_type': 'Végzettség'},
    title='Jövedelem típus és végzettség összefüggése hitelképesség alapján'
)

# Diagram megjelenítése
st.plotly_chart(fig)

