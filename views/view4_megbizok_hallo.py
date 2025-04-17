import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import numpy as np 
from data import load_data


st.fragment()
def megbizok_hallo():

    data = load_data()  
    # 📌 Streamlit felület
    st.title("📊 Interaktív Megbízási Hálózat")
    st.write("A csomópontok mérete a kimenő pénz összegét mutatja, míg a kapcsolatok vastagsága a pénzmozgás nagyságát.")
    st.write("A csomópontokra kattintva részletes információkat kaphatunk a kiutalt és beérkező összegekről.")

    # 📌 Választható csomópontok száma
    num_nodes = st.slider("Hány csomópontot jelenítsünk meg?", min_value=10, max_value=1000, value=200, step=10)
    # ad start button
    start_button = st.button("Start")
    if start_button:

        # 📌 Adatok aggregálása
        edges = (
            data
            .groupby(['vezetoAjanlatkero', 'nyertes'], as_index=False)
            .agg(
                megitelt_tamogatas=('nettoOsszegHUF', 'sum'),
                weight=('ekrAzonosito', 'count')
            )
            .sort_values(by='megitelt_tamogatas', ascending=False)
            .head(num_nodes)
            .reset_index()
        )

        # 📌 Kiutalt (OUT) és beérkező (IN) pénz összegyűjtése
        node_money_out = edges.groupby("vezetoAjanlatkero")["megitelt_tamogatas"].sum().to_dict()
        node_money_in = edges.groupby("nyertes")["megitelt_tamogatas"].sum().to_dict()

        # 📌 Maximális értékek skálázáshoz
        max_money_out = max(node_money_out.values(), default=1)
        max_money_in = max(node_money_in.values(), default=1)
        max_edge_value = max(edges["megitelt_tamogatas"], default=1)

        # 📌 Hálózat létrehozása
        G = nx.DiGraph()

        for _, row in edges.iterrows():
            G.add_edge(row["vezetoAjanlatkero"], row["nyertes"], weight=row["weight"], money=row["megitelt_tamogatas"])

        # 📌 Pyvis hálózat beállítása
        net = Network(height="1200px", width="100%", directed=True, notebook=False)
        net.toggle_physics(True)

        for node in set(edges["vezetoAjanlatkero"]).union(edges["nyertes"]):
            money_sent = node_money_out.get(node, 0)  # Kiutalt pénz
            money_received = node_money_in.get(node, 0)  # Beérkező pénz
            size = max(10, (money_sent / max_money_out) * 50)  # Kiutalt pénz skálázott mérete, min 10

            # 📌 Címke frissítése: kiutalt + beutalt pénz
            title = (f"{node}\n"
                    f"📤 Kiutalt: {(money_sent/1_000_000):,.0f} millió Ft\n".replace(",", " ") +
                    f"📥 Beérkező: {(money_received/1_000_000):,.0f} millió Ft".replace(",", " ")
                    )

            net.add_node(node, title=title, size=size, color="blue")

        for source, target, attrs in G.edges(data=True):
            edge_thickness = max(1, (np.sqrt(attrs["money"]) / np.sqrt(max_edge_value)) * 10)

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


megbizok_hallo()