# st.set_page_config(layout="wide")

from st_app_sections import tracker,apresentacao,snapshot
import pandas as pd
from PIL import Image
import streamlit as st












st.sidebar.markdown("<h1 style='text-align: center; '> Escolinha do TFT </h1>", unsafe_allow_html=True)
# image = Image.open('assets/baixados.jpg')


# st.sidebar.image(image)
section = st.sidebar.selectbox(
    "Ir para:",
    (
    'Apresentação da escolinha',
    'Tracker',
    "Snapshot",
       )
    )


if section == 'Apresentação da escolinha':
    apresentacao()
elif section == 'Tracker':
    tracker()
elif section == "Grupos da Rodada atual":
    snapshot()
