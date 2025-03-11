import streamlit as st
from data import load_data


st.title("📊 Közbeszerzési elemzés")  

st.markdown(  
    """Ebben az alkalmazásban a közbeszerzések adatait elemzem, egységesített és könnyen összehasonlítható formában.  

## Az adatok forrása az [Elektronikus Közbeszerzési Rendszer]('https://ekr.gov.hu/ekr-szerzodestar/hu/szerzodesLista') honlapja.
    
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