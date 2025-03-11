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

    data['tam_dont_datum'] = pd.to_datetime(data['szerzodesKelte'], format='mixed')

    data['year_month'] = data['tam_dont_datum'].dt.to_period('M')
    grouped_df = (
        data
        .groupby(['year_month'], as_index=False)
        .agg(
            megitelt_tamogatas=('nettoOsszegHUF', 'sum'),
            number_of_projects=('ekrAzonosito', 'count')
        )
        .reset_index()
    )
    grouped_df['megitelt_tamogatas'] = (grouped_df['megitelt_tamogatas'] / 1_000_000_000).round(2)
    grouped_df['year_month'] = grouped_df['year_month'].astype(str)

    fig = px.bar(
        grouped_df,
        x='year_month',
        y='megitelt_tamogatas',
        title='',
        labels={'year_month': 'Dátum', 'megitelt_tamogatas': 'Megítélt összeg (milliárd Ft)'},
        barmode='group'
    )

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title=' ',
        yaxis_title='Megítélt összeg (milliárd Ft)',
        legend_title=' ',
        height=800,
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=1.02, 
            xanchor="center",
            x=0.5, 
            title_font=dict(size=12), 
            font=dict(size=10)

        )
    )


    st.title('📊 Adatok')
    st.write("Az alábbi ábra a megítélt közbeszerzések összegét mutatja havonta.")
    st.plotly_chart(fig)

    st.write("Az alábbi táblázat tartalmazza az összes közbeszerzési adatot:")
    data['nettoOsszegHUF'] = data['nettoOsszegHUF'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    data['nettoOsszeg'] = data['nettoOsszeg'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    data['bruttoOsszeg'] = data['bruttoOsszeg'].apply(lambda x: f"{x:,}".replace(",", " ").replace(".0", ""))
    # show just the date
    data['tam_dont_datum'] = data['tam_dont_datum'].dt.date

 
    # rename the columnsto nicely hungarian string to show to the user vezetoAjanlatkero, vezetoAjanlattevo, szerzodesTargya, nettoOsszegHUF, nettoOsszeg, bruttoOsszeg, id, ekrAzonosito, megelozoBeszerzesNev, szerzodesKelte, allapotaNev, szerzodesek_szama, hatalyossagKezdete, hatalyossagVege, bruttoOsszegDevizaneme, nettoOsszegDevizaneme, tartalekkeretOsszeg, tartalekkeretOsszegDevizaneme, tipusaNev, uniosForrasbolFinanszirozott, voltAlvallalkozoja, link do it with rename
    data = data.rename(columns={'vezetoAjanlatkero': 'Ajánlatkérő', 
                                'vezetoAjanlattevo': 'Ajánlattevő', 
                                'szerzodesTargya': 'Szerződés tárgya',
                                'nettoOsszegHUF': 'Nettó összeg (HUF)', 
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
                                'link': 'Link'})  

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