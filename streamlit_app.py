import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import plotly.express as px


st.set_page_config(page_title='Hitelkártya jogosultságot meghatározó tényezők', page_icon='📊')
st.title('📊 Hitelkártya jogosultságot meghatározó tényezők')
  
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

df['Nem'] = df['Gender'].replace({0: 'Férfi', 1: 'Nő'})

# Displaying gender distribution using a count bar chart
st.header('Egyének nem szerinti eloszlása')
gender_chart = alt.Chart(df).mark_bar().encode(
    alt.X('Nem:N', title='Nem'),
    alt.Y('count()', title='Number of Applicants'),
    tooltip=['Nem:N', 'count()']
).properties(
    title='Gender Distribution',
    width=700,
    height=400
).interactive()
st.altair_chart(gender_chart, use_container_width=True)

st.markdown('Hitelkártya jogosultsági szempontból a nemek eloszlásának szemléltetése az elemzésben segítséget nyújt abban, hogy meglássuk, mely nemek képviselői jelentkeznek gyakrabban hitelkártyákért. Ez a tudás lehetővé teszi a pénzintézetek számára, hogy jobban megértsék és célzottabban alakítsák ki a hitelkártya ajánlataikat és marketing stratégiáikat, figyelembe véve a nemek közötti pénzügyi szokások és igények különbségeit.')

df['Hitelképesség'] = df['Target'].replace({0: 'Elutasított', 1: 'Jóváhagyott'})

st.header('Hitelképesség szerinti eloszlása')
st.subheader('Hitelképesség változó, amely azt jelzi, hogy az egyén jogosult-e hitelkártyára vagy sem (pl. Igen/Nem, 1/0).')
target_chart = alt.Chart(df).mark_bar().encode(
    alt.X('Hitelképesség:N', title='Hitelképesség'),
    alt.Y('count()', title='Number of Applicants'),
    tooltip=['Hitelképesség:N', 'count()']
).properties(
    title='Hitelképesség eloszlása',
    width=700,
    height=400
).interactive()
st.altair_chart(target_chart, use_container_width=True)

st.title('A változok közötti kapcsolatok tanulmányozása')

#2

st.header("Végzettség és hitelképesség összefüggése")

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

st.markdown('Az alábbi vizualizáció egy csoportosított oszlopdiagram, amely bemutatja, hogyan oszlik meg a hitelképesség a különböző végzettségi szintek között. Az ábra célja, hogy rávilágítson arra, milyen hatással van a végzettség szintje a hitelkérelmek jóváhagyására vagy elutasítására.A diagramról egyértelműen látszik, hogy a magasabb végzettséggel rendelkező egyének, például az egyetemi vagy felsőfokú végzettséggel rendelkező személyek, jelentősen nagyobb arányban kapják meg a hitelkártya-igénylésük jóváhagyását. Ezzel szemben azok, akik alacsonyabb végzettséggel rendelkeznek, gyakrabban találkoznak hitelkérelmük elutasításával. A különböző végzettségi kategóriákhoz tartozó egyének számát az oszlopok magassága mutatja')

st.header("Jövedelem típus és hitelképesség összefüggése")

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

# kodreszlet 3

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
                     color_discrete_map={'Jóváhagyott': 'green', 'Elutasított': 'red'},
                     height=700,
                     width=900
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
                     color_discrete_map={'Jóváhagyott': 'green', 'Elutasított': 'red'},
                     height=700,
                     width=900
                    )

st.plotly_chart(fig2)
st.markdown('Az ábra azt mutatja, hogyan függ össze a jövedelem típusa és a végzettség a hitelképességgel. A diagram csoportos oszlopdiagram formájában ábrázolja, hogy az egyes jövedelem típusok és végzettségek szerint hány egyént jelöltek meg hitelképességi státusszal. A színek különbsége azt jelzi, hogy az egyének mennyire lettek jóváhagyva vagy elutasítva hitelkérelmükkel.A vizualizációból látható, hogy bizonyos jövedelem típusok és végzettségek esetén magasabb a jóváhagyott hitelképességi arány, míg más esetekben alacsonyabb. A magasabb végzettséggel rendelkezők és bizonyos jövedelem típusok esetén nagyobb eséllyel jóváhagyott a hitelkérelem. Azok az egyének, akik magasabb jövedelemmel rendelkeznek és jobb végzettséggel bírnak stabilabb hitelképességgel rendelkeznek.')
st.subheader('Következtetések')
st.markdown('Az elemzésből nyert vizualizációk alapján látszik, hogy a hitelképességet több tényező is befolyásolja, köztük a végzettség, a jövedelem típusa, a családi állapot, az évek a foglalkozásban és a lakóhely típusa.A magasabb végzettséggel rendelkező egyének, mint például az egyetemi vagy felsőfokú végzettséggel rendelkezők, nagyobb arányban kapják meg a hitelkártya-igénylésük jóváhagyását. Az alacsonyabb végzettséggel rendelkezők gyakrabban találkoznak hitelkérelmük elutasításával. Ez arra utal, hogy a pénzügyi intézmények magasabb kockázatot látnak az alacsonyabb végzettségű egyének esetében, míg a magasabb végzettségűek stabilabb pénzügyi hátteret és nagyobb fizetőképességet sugallnak.Azok az egyének, akik stabil és magasabb jövedelemmel rendelkeznek, valamint magasabb végzettséggel bírnak, jelentősen jobb hitelképességgel rendelkeznek. A pénzügyi intézmények valószínűleg biztonságosabb befektetésként tekintenek ezekre az egyénekre, mivel nagyobb eséllyel tudják kezelni pénzügyi kötelezettségeiket.Az adatokból kiderül, hogy a házas családos emberek hitelképessége gyakran jobb, mint az egyedülállóké vagy élettársakkal élőké. Ez valószínűleg annak köszönhető, hogy a házasok gyakran stabilabb pénzügyi háttérrel és felelősségtudattal rendelkeznek.A hosszabb munkaviszony általában kedvező hatással van a hitelképességre. Azok, akik hosszabb ideje dolgoznak egy munkahelyen, valószínűleg stabilabb jövedelemmel és pénzügyi háttérrel rendelkeznek, ami pozitívan befolyásolja a hitelkérelmük sikerességét. A nagyvárosokban élők esetében jobb lehet a hitelképesség, mivel magasabb jövedelmi szint és stabilitás tapasztalható. A vidéki területeken élők esetében a hitelképesség alacsonyabb lehet, ami a jövedelmi szintek és gazdasági lehetőségek különbségeiből adódhat.')
