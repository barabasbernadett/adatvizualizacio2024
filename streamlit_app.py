import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import plotly.express as px


st.set_page_config(page_title='Hitelkártya jogosultságot meghatározó tényezők', page_icon='📊')
st.title('📊 Hitelkártya jogosultságot meghatározó tényezők')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  
st.subheader('Adatok')
df = pd.read_csv('dataset/creditcard_eligibility_dataset.csv')
st.write(df)

st.subheader('Bevezető')
st.markdown('A projekt célja a hitelkártya-jogosultsági adatbázis részletes elemzése, amely megvilágítja, hogy mely tényezők befolyásolják az egyén hitelkártya-igénylésének sikerességét. Az elemzés célja, hogy megértsük a hitelképességet befolyásoló különböző demográfiai, pénzügyi és személyes tényezőket, és ezek alapján fejlesszünk ki jobb hitelbírálati stratégiákat és célzott marketingkampányokat.')
st.markdown('Az elemzéshez használt adatok egy átfogó hitelkártya-jogosultsági adatbázisból származnak, amely tartalmazza az egyes igénylők demográfiai jellemzőit (például kor, nem), pénzügyi mutatóit (például jövedelem, foglalkoztatási idő), valamint személyes adatokat (például családi állapot, lakhatási körülmények). Az adatok több mint 1000 egyénről gyűjtött információkat tartalmaznak, és változókat tartalmaznak, mint például: ID, Kor, nem , végzettség, családi állapot, lakhatási típus, hitelképesség.')     

st.subheader('Demográfiai változok')

# Create histogram for Age Distribution
age_hist = alt.Chart(df).mark_bar().encode(
    x=alt.X('Age:Q', bin=True, title='Age'),
    y='count()',
).properties(
    title='Egyének életkor szerinti eloszlása',
    width=600,
    height=400
).interactive()

# Display Age Distribution Histogram
st.altair_chart(age_hist, use_container_width=True)

st.markdown('A korosztály szerinti eloszlás elemzése lehetővé teszi, hogy azonosítsuk azokat a korcsoportokat, amelyek dominálnak a hiteligénylők között és leginkább érdeklődnek a hitelkártyák irénylésére és segít abban, hogy felismerjük, mely korosztályok kevésbé képviselték magukat a hitelpiacon.')


# Displaying gender distribution using a count bar chart
st.header('Egyének nem szerinti eloszlása')
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

st.markdown('Hitelkártya jogosultsági szempontból a nemek eloszlásának szemléltetése az elemzésben segítséget nyújt abban, hogy meglássuk, mely nemek képviselői jelentkeznek gyakrabban hitelkártyákért. Ez a tudás lehetővé teszi a pénzintézetek számára, hogy jobban megértsék és célzottabban alakítsák ki a hitelkártya ajánlataikat és marketing stratégiáikat, figyelembe véve a nemek közötti pénzügyi szokások és igények különbségeit.')
  

st.subheader('A változok közötti kapcsolatok tanulmányozása')

#2
df['Hitelképesség'] = df['Target'].replace({0: 'Elutasított', 1: 'Jóváhagyott'})

# Streamlit cím
st.title("Végzettség és hitelképesség összefüggése")

# Grouped Bar Chart létrehozása
fig = px.bar(
    df,
    x='Education_type',
    y='ID',  # Számolja meg az egyéneket
    color='Hitelképesség',
    barmode='group',
    labels={'ID': 'Egyének száma', 'Education_type': 'Végzettség'},
    #title='Végzettség és hitelképesség összefüggése'
)
# Diagram megjelenítése
st.plotly_chart(fig)

st.markdown('')

# Diagram megjelenítése
st.plotly_chart(fig)
# kodreszlet 3

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

st.plotly_chart(fig1)
st.markdown('A vizualizáció szemlélteti, hogyan befolyásolják a családi állapot, évek a  foglalkozásban és lakóhely típusa a hitelképességet, külön kiemelve a jóváhagyott és elutasított hitelképességeket.Az eredmények alapján megállapíthatjuk, hogy például házas családos emberek esetében gyakran jobb a hitelképesség, míg egyedülállók vagy élettársakkal élők körében ez eltérhet. Emellett a hosszabb munkaviszony gyakran kedvező hatással van a hitelképességre, míg a rövidebb foglalkoztatási időszakok esetén magasabb lehet a kockázat. A lakóhely típusa (például városi vagy vidéki) szintén jelentős tényező lehet: a nagyvárosokban élők esetében esetlegesen jobb a hitelképesség, mivel magasabb jövedelmi szint és stabilitás tapasztalható.')

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

st.plotly_chart(fig2)
st.markdown('Az ábra azt mutatja, hogyan függ össze a jövedelem típusa és a végzettség a hitelképességgel. A diagram csoportos oszlopdiagram formájában ábrázolja, hogy az egyes jövedelem típusok és végzettségek szerint hány egyént jelöltek meg hitelképességi státusszal. A színek különbsége azt jelzi, hogy az egyének mennyire lettek jóváhagyva vagy elutasítva hitelkérelmükkel.A vizualizációból látható, hogy bizonyos jövedelem típusok és végzettségek esetén magasabb a jóváhagyott hitelképességi arány, míg más esetekben alacsonyabb. A magasabb végzettséggel rendelkezők és bizonyos jövedelem típusok esetén nagyobb eséllyel jóváhagyott a hitelkérelem. Azok az egyének, akik magasabb jövedelemmel rendelkeznek és jobb végzettséggel bírnak stabilabb hitelképességgel rendelkeznek.')

#kodreszlet4

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

st.markdown('Az ábra azt mutatja, hogyan függ össze a jövedelem típusa és a végzettség a hitelképességgel. \
            A diagram csoportos oszlopdiagram formájában ábrázolja, hogy az egyes jövedelem típusok és végzettségek \
            szerint hány egyént jelöltek meg hitelképességi státusszal. A színek különbsége azt jelzi, hogy az egyének\
             mennyire lettek jóváhagyva vagy elutasítva hitelkérelmükkel.A vizualizációból látható, hogy bizonyos jövedelem típusok és végzettségek esetén magasabb a jóváhagyott hitelképességi arány, míg más esetekben alacsonyabb. A magasabb végzettséggel rendelkezők és bizonyos jövedelem típusok esetén nagyobb eséllyel jóváhagyott a hitelkérelem.')
        
#pleda5 

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
    #labels={'ID': 'Egyének száma', 'Income_type': 'Jövedelem típus', 'Education_type': 'Végzettség'},
    #title='Jövedelem típus és végzettség összefüggése hitelképesség alapján'
)

# Diagram megjelenítése
st.plotly_chart(fig)

#6
df['Hitelképesség'] = df['Target'].replace({0: 'Elutasított', 1: 'Jóváhagyott'})

# Streamlit cím
st.title("Végzettség és hitelképesség összefüggése")

# Grouped Bar Chart létrehozása
fig = px.bar(
    df,
    x='Education_type',
    y='ID',  # Számolja meg az egyéneket
    color='Hitelképesség',
    barmode='group',
    labels={'ID': 'Egyének száma', 'Education_type': 'Végzettség'},
    #title='Végzettség és hitelképesség összefüggése'
)

# Diagram megjelenítése
st.plotly_chart(fig)

#5.2
# Hitelképesség megjelölése
df['Hitelképesség'] = df['Target'].replace({0: 'Elutasított', 1: 'Jóváhagyott'})

# Streamlit cím
st.title("Jövedelem típus és hitelképesség összefüggése")

# Grouped Bar Chart létrehozása
fig = px.bar(
    df,
    x='Income_type',
    y='ID',  # Számolja meg az egyéneket
    color='Hitelképesség',
    barmode='group',
    labels={'ID': 'Egyének száma', 'Income_type': 'Jövedelem típus'},
    title='Jövedelem típus és hitelképesség összefüggése'
)

# Diagram megjelenítése
st.plotly_chart(fig)

#7
df['Hitelképesség'] = df['Target'].replace({0: 'Elutasított', 1: 'Jóváhagyott'})

# Streamlit cím
st.title("Kor és jövedelem hatása hitelképességre")

# Heatmap létrehozása
fig = px.density_heatmap(
    df,
    x='Age',
    y='Total_income',
    z='Hitelképesség',
    color_continuous_scale='Viridis',
    labels={'Age': 'Kor', 'Total_income': 'Jövedelem', 'Hitelképesség': 'Hitelképesség'},
    title='Kor és jövedelem hatása hitelképességre'
)

# Diagram megjelenítése
st.plotly_chart(fig)

#kodreszlet3

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