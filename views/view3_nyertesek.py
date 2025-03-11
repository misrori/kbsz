import streamlit as st
from data import load_data
import plotly.express as px
import pandas as pd


# Load the CSV data into a DataFrame

@st.fragment
def display_megbizok():
    st.title("Nyertesek")
    data = load_data()


    grouped_df= (
        data
        .groupby('vezetoAjanlattevo', as_index=False)
        .agg(
            megitelt_tamogatas=('nettoOsszegHUF', 'sum'),
            number_of_projects=('ekrAzonosito', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=False)
        .head(30)
        .sort_values(by='megitelt_tamogatas', ascending=True)
        .reset_index()
    )

    grouped_df['megitelt_tamogatas'] = (grouped_df['megitelt_tamogatas'] / 1_000_000_000).round(2)
    fig = px.bar(grouped_df, y='vezetoAjanlattevo', x='megitelt_tamogatas',
                labels={'vezetoAjanlattevo': 'Nyertes', 'megitelt_tamogatas': 'Megítélt összeg (milliárd Ft)'},
                title='Megítélt összeg nyertesenként', orientation='h' )

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title=' ',
        xaxis_title='Megítélt összeg (milliárd Ft)',  # updated here to align with previous changes
        height=900,
        xaxis=dict(
            tickformat=',',  
        )
    )
    fig.update_traces(
    text=grouped_df['megitelt_tamogatas'], 
    textposition='inside', 
    texttemplate='%{text:.0f}',
    )
    plot3 = fig

    st.write("Az alábbi ábra a nyerteseket mutatja, rangsorolva az összes megbízás összege alapján.")
    st.plotly_chart(plot3)



    megbizottak_df = (
        data
        .groupby('vezetoAjanlattevo')
        .agg(
            megbizok_szama = ('vezetoAjanlatkero', 'nunique'),
            szerzodesek_szama = ('ekrAzonosito', 'count'),
            osszes_megbizas_osszege = ('nettoOsszegHUF', 'sum'),
            
        )
        .sort_values('osszes_megbizas_osszege', ascending=False)
        .reset_index()

    )



    megbizottak_df['osszes_megbizas_osszege'] = megbizottak_df['osszes_megbizas_osszege'] / 1_000_000

    megbizottak_df.rename(columns={'vezetoAjanlattevo': 'Nyertes', 
                                'megbizok_szama': 'Megbízók száma', 
                                'szerzodesek_szama': 'Szerződések száma', 
                                'osszes_megbizas_osszege': 'Összes megbízás összege (millió Ft)'}, 
                                inplace=True)
    st.dataframe(megbizottak_df.style.format({"Összes megbízás összege (millió Ft)": lambda x: f"{x:,.0f}".replace(",", " "),
                                           "Megbízók száma": lambda x: f"{x:,.0f}".replace(",", " "),
                                           "Szerződések száma": lambda x: f"{x:,.0f}".replace(",", " ")}))




display_megbizok()


