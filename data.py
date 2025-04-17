import streamlit as st
import pandas as pd
import pickle

# read data into a pandas DataFrame with cache
@st.cache_data
def load_data():
    # read pickle
    with open("all_data.pkl", "rb") as f:
        df = pickle.load(f)

    df['szerzodesKelte'].replace('20218.11.14.', '2018.11.14.')
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
    
    # the biggest amout is false
    #ekr_azonmosito ==SZ0031506 divide with 1000
    df.loc[df['ekrAzonosito'] == 'SZ0031506', 'nettoOsszegHUF'] = df.loc[df['ekrAzonosito'] == 'SZ0031506', 'nettoOsszegHUF'] / 1000
    df.loc[df['ekrAzonosito'] == 'SZ0031506', 'nettoOsszeg'] = df.loc[df['ekrAzonosito'] == 'SZ0031506', 'nettoOsszeg'] / 1000

    # remove ekr SZ0035255
    df = df[df['ekrAzonosito'] != 'SZ0035255']

    df['tam_dont_datum'] = pd.to_datetime(df['szerzodesKelte'], format='mixed', errors='coerce')
    # convert to datetime
    #egyeduli nyertes in nyertes tipus to egyedűli nyertes
    df['nyertes_tipus'] = df['nyertes_tipus'].replace('egyeduli nyertes', 'egyedüli nyertes')

    df.drop(columns=['szerzodesek_szama'], inplace=True)
    df.drop(columns=['id'], inplace=True)
    df.sort_values('nettoOsszegHUF', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

