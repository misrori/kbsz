import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import numpy as np
from data import load_data



st.fragment()
def display_egyeni_hallo():

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
        full_filtered_data = data[
            data['vezetoAjanlatkero'].isin(additional_companies) | data['nyertes'].isin(additional_companies)
        ]

        # 📌 Adatok aggregálása
        edges = (
            full_filtered_data
            .groupby(['vezetoAjanlatkero', 'nyertes'], as_index=False)
            .agg(
                megitelt_tamogatas=('nettoOsszegHUF', 'sum'),
                weight=('ekrAzonosito', 'count')
            )
            .sort_values(by='megitelt_tamogatas', ascending=False)
            .reset_index()
        )

        # 📌 Kiutalt (OUT) és beérkező (IN) pénz összegyűjtése
        node_money_out = edges.groupby("vezetoAjanlatkero")["megitelt_tamogatas"].sum().to_dict()
        node_money_in = edges.groupby("nyertes")["megitelt_tamogatas"].sum().to_dict()

        # 📌 Maximális értékek skálázáshoz
        max_money_out = max(node_money_out.values(), default=1)
        max_money_in = max(node_money_in.values(), default=1)
        max_edge_weight = max(edges["weight"], default=1)

            # 📌 Hálózat létrehozása
        G = nx.DiGraph()

        for _, row in edges.iterrows():
            G.add_edge(row["vezetoAjanlatkero"], row["nyertes"], weight=row["weight"], money=row["megitelt_tamogatas"])

        # 📌 Pyvis hálózat beállítása
        net = Network(height="1200px", width="100%", directed=True, notebook=False)

        net.toggle_physics(True)

        # Kiválasztott cégek
        selected_set = set(selected_companies)

        for node in set(edges["vezetoAjanlatkero"]).union(edges["nyertes"]):
            money_sent = node_money_out.get(node, 0)  # Kiutalt pénz
            money_received = node_money_in.get(node, 0)  # Beérkező pénz
            if size_option == "Kiutalt pénz":
                size = max(10, (money_sent / max_money_out) * 50)  # Kiutalt pénz skálázott mérete
            else:
                size = max(10, (money_received / max_money_in) * 50)  # Befolyó pénz skálázott mérete

            # 📌 Címke frissítése: kiutalt + beutalt pénz
            title = (f"{node}\n"
            f"📤 Kiutalt: {(money_sent/1_000_000):,.0f} millió Ft\n".replace(",", " ") +
            f"📥 Beérkező: {(money_received/1_000_000):,.0f} millió Ft".replace(",", " ")
            )

            # Ha a cég szerepel a kiválasztott cégek között, piros színt kap
            color = "red" if node in selected_set else "blue"

            net.add_node(node, title=title, size=size, color=color)

        # 📌 Élek vastagságának beállítása pénzmozgás alapján
        for source, target, attrs in G.edges(data=True):
            # Pénzmozgás alapján vastagság: arányosítjuk a pénzmozgással
            edge_thickness = max(1, (attrs["money"] / max(attrs["money"] for _, _, attrs in G.edges(data=True))) * 10)

            # Eredmény hozzáadása
            net.add_edge(
                source, target,
                value=edge_thickness,
                title=f"Kapcsolatok száma: {attrs['weight']}\nÖsszeg: {(attrs['money']/1_000_000):,.0f} millió Ft".replace(",", " ")
            )

        # 📌 Gráf HTML-be exportálása
        net.save_graph("graph.html")


        with open("graph.html", "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, width=1900, height=1200, scrolling=True)


display_egyeni_hallo()