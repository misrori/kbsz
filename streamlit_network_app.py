import streamlit as st
import pandas as pd
import json
import os
from network_generator import generate_network_html

# Set page config
st.set_page_config(layout="wide", page_title="Közbeszerzési Hálózat", page_icon="📊")

st.title("Közbeszerzési Hálózati Vizualizáció")

# Sample data input - in a real app, you might load this from a file or database
if "network_data" not in st.session_state:
    st.session_state.network_data = [
        {"megbizo": "Állami Fejlesztési Központ", "megbizott": "Nagy Építő Kft.", "osszeg": 150000000, "palyazatokSzama": 2},
        {"megbizo": "Állami Fejlesztési Központ", "megbizott": "Gyors Projekt Zrt.", "osszeg": 85000000, "palyazatokSzama": 1},
        {"megbizo": "Városi Önkormányzat A", "megbizott": "Helyi Szolgáltató Bt.", "osszeg": 12000000, "palyazatokSzama": 5},
        # Add more entries as needed
    ]

# Data editor
with st.expander("Adatok szerkesztése"):
    edited_data = st.data_editor(
        pd.DataFrame(st.session_state.network_data),
        num_rows="dynamic",
        column_config={
            "megbizo": "Megbízó",
            "megbizott": "Megbízott",
            "osszeg": st.column_config.NumberColumn("Összeg (Ft)"),
            "palyazatokSzama": st.column_config.NumberColumn("Pályázatok száma", min_value=1, step=1),
        },
    )
    
    # Update session state when data is edited
    if st.button("Adatok frissítése"):
        st.session_state.network_data = edited_data.to_dict('records')
        st.success("Adatok frissítve!")

# Generate the visualization
if st.button("Hálózati vizualizáció generálása") or "generated_html" not in st.session_state:
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "templates", "network_template.html")
    output_path = os.path.join(base_dir, "temp_network.html")
    
    # Generate HTML
    generate_network_html(st.session_state.network_data, template_path, output_path)
    
    # Read the generated HTML
    with open(output_path, 'r', encoding='utf-8') as f:
        st.session_state.generated_html = f.read()
    
    # Clean up temporary file
    os.remove(output_path)

# Display the visualization
st.components.html(st.session_state.generated_html, height=700)

# Export options
with st.expander("Exportálási lehetőségek"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.download_button(
            "Letöltés HTML fájlként",
            data=st.session_state.generated_html,
            file_name="kozbeszerzes_halozat.html",
            mime="text/html"
        ):
            st.success("HTML fájl letöltve!")
    
    with col2:
        if st.download_button(
            "Adatok letöltése JSON formátumban",
            data=json.dumps(st.session_state.network_data, ensure_ascii=False, indent=4),
            file_name="kozbeszerzes_adatok.json",
            mime="application/json"
        ):
            st.success("JSON fájl letöltve!")
