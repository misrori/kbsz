import streamlit as st
from data import load_data
import pandas as pd
import plotly.express as px



st.title("📊 Közbeszerzési elemzés")  

st.markdown(  
    """Ebben az alkalmazásban a közbeszerzések adatait elemzem, egységesített és könnyen összehasonlítható formában.  

## Az adatok forrása az [Elektronikus Közbeszerzési Rendszer]('https://ekr.gov.hu/ekr-szerzodestar/hu/szerzodesLista') honlapja.
"""
)  

@st.fragment
def display_main_numbers():
    data = load_data()
    st.header("Fő mutatószámok")

    col1, col2, col3, col4 = st.columns(4)

    # Összes pályázat
    with col1:
        st.metric("Összes pályázat", data['ekrAzonosito'].nunique())

    # Összes kifizetett összeg
    with col2:
        if 'nettoOsszegHUF' in data.columns:
            total_amount = data['nettoOsszegHUF'].sum()
            st.metric("Összes kifizetés (HUF)", f"{total_amount:,.0f}".replace(",", " "))

    # Ajánlattevők száma
    with col3:
        if 'ajanlat_tevok_szama' in data.columns:
            avg_bidders = data['ajanlat_tevok_szama'].mean()
            st.metric("Átlagos ajánlattevők száma", f"{avg_bidders:.2f}")

    # Átlagos szerződés összeg
    with col4:
        if 'nettoOsszegHUF' in data.columns:
            avg_amount = data['nettoOsszegHUF'].mean()
            st.metric("Átlagos szerződés összeg (HUF)", f"{avg_amount:,.0f}".replace(",", " "))


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


    st.write("Az alábbi ábra a megítélt közbeszerzések összegét mutatja havonta.")
    st.plotly_chart(fig)



# same pie chart by value calculated from nettoosszeghuf

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Uniós forrásból finanszírozott projektek (nettó összeg)")
        
        if 'uniosForrasbolFinanszirozott' in data.columns and 'nettoOsszegHUF' in data.columns:
            unios_counts = data.groupby('uniosForrasbolFinanszirozott')['nettoOsszegHUF'].sum().reset_index()
            unios_counts.columns = ['Uniós forrás', 'Összeg']
            unios_counts['Uniós forrás'] = unios_counts['Uniós forrás'].map({True: 'Igen', False: 'Nem'})
            
            fig = px.pie(
                unios_counts,
                values='Összeg',
                names='Uniós forrás',
                title="Uniós forrásból finanszírozott projektek aránya (nettó összeg)"
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Szerződés típusai (nettó összeg)")
        
        if 'tipusaNev' in data.columns and 'nettoOsszegHUF' in data.columns:
            type_counts = data.groupby('tipusaNev')['nettoOsszegHUF'].sum().reset_index()
            type_counts.columns = ['Típus', 'Összeg']
            
            fig = px.pie(
                type_counts,
                values='Összeg',
                names='Típus',
                title="Szerződések típus szerinti megoszlása (nettó összeg)"
            )
            # format the values in the pie chart
            fig.update_traces(textinfo='percent+label', textfont_size=12)
            fig.update_layout(title_font_size=20)   
            st.plotly_chart(fig, use_container_width=True)


display_main_numbers()



st.markdown(
    """      
## 🔍 Hogyan készült az adatbázis?  


✔️ **Minden közbeszerzés értékét forintra váltottam**, ha az eredetileg más devizában szerepelt.  
&nbsp;&nbsp;&nbsp;➝ Az átváltás mindig **az adott napi árfolyamon** történt, amikor a közbeszerzést kihirdették.  

✔️ **Bruttóból nettó számítás**  
&nbsp;&nbsp;&nbsp;➝ Ha az összeg nettóban volt megadva,akkor azt vettem figyelembe.  

➝ Ha az összeg bruttóban volt megadva, **a 27%-os áfát levonva nettósítottam** (osztva 1,27-tel).  

## 📈 Mit találsz itt?  

📌 **Egységes pénzügyi adatok** minden közbeszerzésről.  
📌 **Automatikusan átváltott értékek**, hogy könnyebb legyen az összehasonlítás.  
📌 **Tisztított és struktúrált információk**, a pontos elemzés érdekében.  

🔎 **Böngéssz az adatok között, és fedezd fel az érdekességeket!** 🚀  
"""
)  



