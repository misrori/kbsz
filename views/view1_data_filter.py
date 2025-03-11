import streamlit as st
from data import load_data
import pandas as pd
import numpy as np

pd.set_option("display.float_format", "{:,.0f}".format)

@st.fragment
def display_filter_data():
    data = load_data()
    data['tam_dont_datum'] = pd.to_datetime(data['szerzodesKelte'], format='mixed')
    
    # Szűrők beállítása három oszlopban
    col1, col2 = st.columns(2)
    
    with col1:
        ajanlatkero_filter = st.multiselect("Válasszon ajánlatkérőt:", sorted(data['vezetoAjanlatkero'].dropna().unique().tolist()), placeholder="Válassz a ajánlat kérőt!")

    with col2:
        ajanlattevo_filter = st.multiselect("Válasszon ajánlattevőt:", sorted(data['vezetoAjanlattevo'].dropna().unique().tolist()),  placeholder="Válassz ajánlat tevőt!")
    
    osszeg_filter = st.checkbox('Szűrés nettó összeg alapján')
    if osszeg_filter:

        min_osszeg, max_osszeg = st.slider("Nettó összeg (millio Ft):",value=(0, 10_000), min_value= int(data['nettoOsszegHUF'].min()),max_value=90_000 ,  step=10)
        min_osszeg = min_osszeg * 1_000_000
        max_osszeg = max_osszeg * 1_000_000
    
    # Szűrés alkalmazása
    if ajanlatkero_filter:
        data = data[data['vezetoAjanlatkero'].isin(ajanlatkero_filter)]
    
    if ajanlattevo_filter:
        data = data[data['vezetoAjanlattevo'].isin(ajanlattevo_filter)]
    
    if osszeg_filter:
        data = data[(data['nettoOsszegHUF'] >= min_osszeg) & (data['nettoOsszegHUF'] <= max_osszeg)]
    
    # Adatok formázása
    data['nettoOsszegHUF'] = data['nettoOsszegHUF'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    data['nettoOsszeg'] = data['nettoOsszeg'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    data['bruttoOsszeg'] = data['bruttoOsszeg'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    
    st.write("Az alábbi táblázat tartalmazza a szűrt közbeszerzési adatokat:")

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

    st.write("📊 A szűrt adatbázis mérete: ", data.shape)

display_filter_data()
