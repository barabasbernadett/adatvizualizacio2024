import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

st.subheader('A változok közötti kapcsolatok tanulmányozása')

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

st.markdown('A családi állapot,foglalkozás és lakóhely típusa közötti összefüggéseket a hitelképességgel kapcsolatban a háromdimenziós felületi diagram szemléltet. Az eredmények alapján megállapíthatjuk, hogy például házas családos emberek esetében gyakran jobb a hitelképesség, míg egyedülállók vagy élettársakkal élők körében ez eltérhet. Emellett a hosszabb munkaviszony gyakran kedvező hatással van a hitelképességre, míg a rövidebb foglalkoztatási időszakok esetén magasabb lehet a kockázat. A lakóhely típusa (például városi vagy vidéki) szintén jelentős tényező lehet: a nagyvárosokban élők esetében esetlegesen jobb a hitelképesség, mivel magasabb jövedelmi szint és stabilitás tapasztalható.')


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

st.plotly_chart(fig1)
st.markdown('A vizualizáció szemlélteti, hogyan befolyásolják a családi állapot, évek a  foglalkozásban és lakóhely típusa a hitelképességet, külön kiemelve a jóváhagyott és elutasított hitelképességeket.A vizualizációk alapján számos fontos következtetést vonhatunk le a családi állapot, évek a foglalkozásban és lakóhely típusa közötti összefüggésekről a hitelképességgel kapcsolatban. Először is, látható, hogy bizonyos családi állapotok és hosszú távú munkatapasztalat jobb hitelképességet eredményezhetnek, míg másoknál ez gyengébb lehet. Ez arra utal, hogy ezek a társadalmi-gazdasági tényezők meghatározó szerepet játszanak az egyének pénzügyi stabilitásában és hitelminősítésében. Az összefüggések tanulmányozása lehetővé teszi a pénzügyi szolgáltatók számára, hogy mélyebben megértsék, milyen társadalmi-gazdasági tényezők játszanak szerepet az egyének pénzügyi stabilitásában és hitelképességében.')

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


st.markdown('A második vizualizáció fókuszában a jövedelem, végzettség és évek a foglalkozásban szerepelnek, és ezek kapcsán mutatja be, hogyan határozzák meg ezek a tényezők az egyén hitelképességét. Azok az egyének, akik magasabb jövedelemmel rendelkeznek és jobb végzettséggel bírnak stabilabb hitelképességgel rendelkeznek. Ez annak tudható be, hogy ezek az emberek képesek hatékonyan kezelni pénzügyi kötelezettségeiket és hosszú távú pénzügyi stabilitást biztosítani számukra.')
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

st.markdown('Az ábra azt mutatja, hogyan függ össze a jövedelem típusa és a végzettség a hitelképességgel. A diagram csoportos oszlopdiagram formájában ábrázolja, hogy az egyes jövedelem típusok és végzettségek szerint hány egyént jelöltek meg hitelképességi státusszal. A színek különbsége azt jelzi, hogy az egyének mennyire lettek jóváhagyva vagy elutasítva hitelkérelmükkel.A vizualizációból látható, hogy bizonyos jövedelem típusok és végzettségek esetén magasabb a jóváhagyott hitelképességi arány, míg más esetekben alacsonyabb. A magasabb végzettséggel rendelkezők és bizonyos jövedelem típusok esetén nagyobb eséllyel jóváhagyott a hitelkérelem.')
        
#pleda5 
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