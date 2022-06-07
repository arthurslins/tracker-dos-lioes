# st.set_page_config(layout="wide")

from st_app_sections import tracker,apresentacao
import pandas as pd
from PIL import Image
import streamlit as st












st.sidebar.markdown("<h1 style='text-align: center; '> Escolinha do TFT </h1>", unsafe_allow_html=True)
st.sidebar.image("assets/logo2_2.png", use_column_width=True)
section = st.sidebar.selectbox(
    "Ir para:",
    (
    'Apresentação do Tracker',
    'Tracker'   
     )
    )


if section == 'Apresentação do Tracker':
    apresentacao()
elif section == 'Tracker':
    tracker()
# elif section == "Grupos da Rodada atual":
#     snapshot()
