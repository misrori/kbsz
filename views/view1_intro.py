import streamlit as st
from data import load_data
import pandas as pd
import plotly.express as px
import numpy as np
pd.set_option("display.float_format", "{:,.0f}".format)



@st.fragment
def display_full_data():

    data = load_data()
    #with 0 floating FloatingPoint but keep ,
    #pd.set_option("display.float_format", "{:,.0f}".format)

    #data['nettoOsszegHUF'] = data['nettoOsszegHUF'].apply(lambda x: f"{x:,.0f}")
    #data['nettoOsszeg'] = data['nettoOsszeg'].apply(lambda x: f"{x:,.0f}")
    #data['bruttoOsszeg'] = data['bruttoOsszeg'].apply(lambda x: f"{x:,.0f}")
    #data['tartalekkeretOsszeg'] = data['tartalekkeretOsszeg'].apply(lambda x: f"{x:,.0f}")




    data.sort_values('nettoOsszegHUF', ascending=False, inplace=True)

    #st.write("Az alábbi táblázat tartalmazza az összes közbeszerzési adatot:")
    data['nettoOsszegHUF'] = data['nettoOsszegHUF'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    data['nettoOsszeg'] = data['nettoOsszeg'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    data['bruttoOsszeg'] = data['bruttoOsszeg'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    
    # show just the date
    data['tam_dont_datum'] = data['tam_dont_datum'].dt.date




    # rename the columnsto nicely hungarian string to show rename
    data = data.rename(columns={'vezetoAjanlatkero': 'Ajánlatkérő', 
                                'nyertes': 'Nyertes', 
                                'nyertes_tipus': 'Nyertes típus',
                                'szerzodesTargya': 'Szerződés tárgya',
                                'nettoOsszegHUF': 'Nettó összeg (Ft)', 
                                'nettoOsszeg': 'Nettó összeg', 
                                'bruttoOsszeg': 'Bruttó összeg', 
                                'ekrAzonosito': 'EKR azonosító', 
                                'megelozoBeszerzesNev': 'Megelőző beszerzés neve', 
                                'szerzodesKelte': 'Szerződés kelte', 
                                'allapotaNev': 'Állapota neve', 
                                'szerzodesek_szama': 'Szerződések száma', 
                                'hatalyossagKezdete': 'Hatalyosság kezdete', 
                                'hatalyossagVege': 'Hatalyosság vége', 
                                'bruttoOsszegDevizaneme': 'Bruttó összeg devizaneme', 
                                'nettoOsszegDevizaneme': 'Nettó összeg devizaneme', 
                                'tartalekkeretOsszeg': 'Tartalékkeret összeg', 
                                'tartalekkeretOsszegDevizaneme': 'Tartalékkeret összeg devizaneme', 
                                'tipusaNev': 'Típus neve', 
                                'uniosForrasbolFinanszirozott': 'Uniós forrásból finanszírozott', 
                                'voltAlvallalkozoja': 'Volt alvállalkozója',
                                'tam_dont_datum': 'Támogatási döntés dátuma',
                                'year_month': 'Év-hónap',
                                'ajanlatkerok_szama': 'Ajánlatkérők száma',
                                'ajanlat_tevok_szama': 'Ajánlattevők száma',
                                'tamogatas_aranya': 'Támogatás aránya',
                                'nyertes_adoszama': 'Nyertes adószáma',
                                'megbizo_adoszama': 'Megbízó adószáma',
                                'link': 'Link'})  
    # order
    important_cols = ['Ajánlatkérő', 'Nyertes', 'Nettó összeg (Ft)', 'Szerződés tárgya', 'Nyertes típus']
    # add the columns to the front
    data = data.reindex(columns=important_cols + [col for col in data.columns if col not in important_cols])
    # add the link column


    
    st.data_editor(
        data,
        column_config={
            "Link": st.column_config.LinkColumn(
                "Link",
                help="more info",
                display_text="Részletek",
            ),
        },
        hide_index=True,
    )



    st.write(f"📊 A teljes adatbázis mérete: {data.shape[0]} sor, {data.shape[1]:,.0f} oszlop.".replace(',', ' '))

display_full_data()