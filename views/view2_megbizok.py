import streamlit as st
from data import load_data
import plotly.express as px
import pandas as pd
pd.set_option("display.float_format", "{:,.0f}".format)



@st.fragment
def display_megbizok():
    st.title("Megbízók")

    data = load_data()

    grouped_df= (
        data
        .groupby('vezetoAjanlatkero', as_index=False)
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
    fig = px.bar(grouped_df, y='vezetoAjanlatkero', x='megitelt_tamogatas',
                labels={'vezetoAjanlatkero': 'Ajánlatkérő', 'megitelt_tamogatas': 'Megítélt összeg (milliárd Ft)'},
                title='Megítélt összeg megbízónként', orientation='h' )

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title=' ',
        xaxis_title='Megítélt összeg (milliárd Ft)',  # corrected here to align with label changes
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
    plot2 = fig

    st.write("Az alábbi ábra a megbízókat mutatja, rangsorolva az összes megbízás összege alapján.")
    st.plotly_chart(plot2)



    megbizok_df= (   
        data
        .groupby('vezetoAjanlatkero')
        .agg(
            nyertesek_szama = ('vezetoAjanlattevo', 'nunique'),
            szerzodesek_szama = ('ekrAzonosito', 'count'),
            osszes_megbizas_osszege = ('nettoOsszegHUF', 'sum'),
            
        )
        .sort_values('osszes_megbizas_osszege', ascending=False)
        .reset_index()
    )


    megbizok_df['osszes_megbizas_osszege'] = megbizok_df['osszes_megbizas_osszege'] / 1000000

    megbizok_df.rename(columns={'vezetoAjanlatkero': 'Megbízó', 
                                'nyertesek_szama': 'Nyertesek száma', 
                                'szerzodesek_szama': 'Szerződések száma', 
                                'osszes_megbizas_osszege': 'Összes megbízás összege (millió Ft)'}, 
                                inplace=True)
    st.dataframe(megbizok_df.style.format({"Összes megbízás összege (millió Ft)": lambda x: f"{x:,.0f}".replace(",", " "),
                                           "Nyertesek száma": lambda x: f"{x:,.0f}".replace(",", " "),
                                           "Szerződések száma": lambda x: f"{x:,.0f}".replace(",", " ")}))

display_megbizok()


