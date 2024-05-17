import pandas as pd
import streamlit as st
@st.cache_data
def carrega_dados():
    current_dir = os.path.dirname(__file__)
    df_path = os.path.join(current_dir, 'RelatorioAlunos2024Clear.xlsx')
    df = pd.read_excel(df_path, header=0)
    return df
