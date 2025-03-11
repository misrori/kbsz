import streamlit as st
import pandas as pd

# read data into a pandas DataFrame with cache
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    df['szerzodesKelte'] = df['szerzodesKelte'].replace('20218.11.14.', '2018.11.14.')
    df['szerzodesKelte'] = df['szerzodesKelte'].replace('0201.07.19.', '2019.06.20.')
    # if starts with 02 replace the fist two characret to 20
    df['szerzodesKelte'] = df['szerzodesKelte'].str.replace(r'^02', '20', regex=True)
    # drop szerzodesek_szama column
    df['link'] = df['id'].apply(lambda x: f'https://ekr.gov.hu/ekr-szerzodestar/hu/szerzodes/{x}')
    #df['nettoOsszegHUF'] = round(df['nettoOsszegHUF']/1000000, 0)
    df['nettoOsszegHUF'] = round(df['nettoOsszegHUF'],0)
    df['nettoOsszeg'] = round(df['nettoOsszeg'],0)
    df['bruttoOsszeg'] = round(df['bruttoOsszeg'],0)
    df['tartalekkeretOsszeg'] = round(df['tartalekkeretOsszeg'],0)    
    df.drop(columns=['szerzodesek_szama'], inplace=True)
    df.drop(columns=['id'], inplace=True)
    df.sort_values('nettoOsszegHUF', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

