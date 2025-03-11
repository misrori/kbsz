import streamlit as st

st.set_page_config(layout="wide", page_title="Csak a közpénz", page_icon="📊")
# set the sidebar side width to 10%


# --- INTRO ---
home_page = st.Page(
    "views/view0_intro.py",
    title="Kezdőlap",
    icon=":material/account_circle:",
    default=True,
)


# --- INTRO ---
full_data_intro_page = st.Page(
    "views/view1_intro.py",
    title="Teljes adatbázis",
    icon=":material/account_circle:",
)


# --- data ---
filtered_data_intro_page = st.Page(
    "views/view1_data_filter.py",
    title="Szűrt adatbázis",
    icon=":material/account_circle:",
)

# --- DATA ---
data_page_megbizok = st.Page(
    "views/view2_megbizok.py",
    title="Megbízók",
    icon=":material/table:",
)

# --- DATA ---
data_page_nyertesek = st.Page(
    "views/view3_nyertesek.py",
    title="Nyertesek",
    icon=":material/table:",
)

# --- Network ---
network_page_megbizok = st.Page(
    "views/view4_megbizok_hallo.py",
    title="Megbízók hálózata",
    icon=":material/bar_chart:",
)

# --- Network ---
network_page_nyertesek = st.Page(
    "views/view5_nyertesek_hallo.py",
    title="Nyertesek hálózata",
    icon=":material/bar_chart:",
)

# --- Network ---
network_page_egyeni = st.Page(
    "views/view6_egyeni_hallo.py",
    title="Egyéni hálózat",
    icon=":material/bar_chart:",
)

# --- NAVIGATION SETUP ---
pg = st.navigation(
    {   'Kezdőlap': [home_page],
        "Adatok": [full_data_intro_page, filtered_data_intro_page,  data_page_megbizok, data_page_nyertesek], 
        "Hálózat": [network_page_megbizok, network_page_nyertesek, network_page_egyeni],
    }
)

# --- SHARED ON ALL PAGES ---
st.logo(
    'https://i.ibb.co/XZpg7FX0/bin.png',
    #link="https://goldhandfinance.streamlit.app/",
    size="large"
)

#st.sidebar.markdown("Made with ❤️")

# --- RUN NAVIGATION ---
pg.run()
