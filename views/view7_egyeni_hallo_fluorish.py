import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import numpy as np
from data import load_data
import os
import json

def generate_network_html(data, template_path, output_path):
    """
    Generate a network visualization HTML file from a template and data.
    
    Args:
        data: List of dictionaries containing network data
        template_path: Path to the HTML template file
        output_path: Path to write the output HTML file
    """
    # Convert data to JSON string
    data_json = json.dumps(data, ensure_ascii=False, indent=4)
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Replace the placeholder with the actual data
    output_content = template_content.replace('/* PLACEHOLDER_FOR_DATA */', data_json)
    
    # Write the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"Generated network visualization at: {output_path}")


st.fragment()
def export_egyeni_hallo():

    # 📌 Data betöltése
    data = load_data()
    # 📌 Streamlit felület
    st.title("📊 Interaktív Megbízási Hálózat")
    st.write("Az alábbi ábra a kiválasztott cégek közbeszerzéseit és kapcsolatait mutatja.")


    # 📌 Legördülő lista a cégek kiválasztására
    sorted_companies = pd.concat([
        pd.Series(data['vezetoAjanlatkero'].unique()),  # Átalakítjuk Series típusra
        pd.Series(data['nyertes'].unique())  # Átalakítjuk Series típusra
    ]).unique()  # Minden cég az ajánlatkérők és ajánlattevők oszlopából

    # 📌 Kiválasztott cégek
    selected_companies = st.multiselect("Válassz cégeket:", sorted_companies, default="Nemzeti Kommunikációs Hivatal")


    # 📌 Választható nód méret: kiutalt vagy befolyó pénz
    size_option = st.selectbox("Válaszd meg a csomópontok méretét:", ["Kiutalt összeg", "Befolyó összeg"])

    # 📌 Közvetlen kapcsolatok vagy plusz réteg hozzáadása
    direct_connections_only = st.checkbox("Plusz egy réteg", value=True)


    # 📌 Start gomb
    start_button = st.button("Start")

    if start_button:
        # 📌 Adatok szűrése a kiválasztott cégekre
        filtered_data = data[
            data['vezetoAjanlatkero'].isin(selected_companies) | data['nyertes'].isin(selected_companies)
        ]

        if direct_connections_only==False:
            # 📌 Ha csak közvetlen kapcsolatok szükségesek, akkor csak az adott cégek közvetlen kapcsolatai
            additional_companies = selected_companies
        else:
            # 📌 További cégek hozzáadása, melyek kapcsolódnak a kiválasztott cégekhez
            additional_companies = set(filtered_data['vezetoAjanlatkero']).union(filtered_data['nyertes'])

        # 📌 Adatok újra szűrése, hogy a kiválasztott cégek és azok kapcsolatai kerüljenek be
        network_df = data[
            data['vezetoAjanlatkero'].isin(additional_companies) | data['nyertes'].isin(additional_companies)
        ]


        network_df = network_df[['vezetoAjanlatkero', 'nyertes', 'nettoOsszegHUF', 'ekrAzonosito']]
        # gorup by and create the data
        network_df = (network_df.groupby(['vezetoAjanlatkero', 'nyertes'], as_index=False)
        .agg(
            osszeg=('nettoOsszegHUF', 'sum'),
            palyazatokSzama=('ekrAzonosito', 'count')
        )
        .sort_values(by='osszeg', ascending=False)
        .reset_index(drop=True)
        )

        # rename column vezetoAjanlatkero to megbizo
        network_df.rename(columns={'vezetoAjanlatkero': 'megbizo', 'nyertes': 'megbizott'}, inplace=True)
           

        if len(network_df) > 0:
            # generate network with the template
            template_path = '/templates/network_template.html'
            output_path = 'temp_network.html'
            generate_network_html(network_df.to_dict('records'), template_path, output_path)

#            if os.path.exists(output_path):
#                with open(output_path, 'r', encoding='utf-8') as f:
#                    html_content = f.read()
#                components.html(html_content, height=800, width=1200)
#            else:
#                st.warning("Nincs elérhető hálózati vizualizáció.")

            # download the output file
            with open(output_path, 'rb') as f:
                st.download_button(
                    label="Letöltés",
                    data=f,
                    file_name="network_visualization.html",
                    mime="text/html"
                )



   
        else:
            st.warning("Nincsenek kapcsolatok a kiválasztott cégek között.")
    else:
        st.warning("Kérlek válassz cégeket és kattints a 'Start' gombra.")




         

export_egyeni_hallo()