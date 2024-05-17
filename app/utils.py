import pandas as pd

@st.cache_data
def carrega_dados():
    df_path = '../RelatorioAlunos2024Clear.xlsx'
    df = pd.read_excel(df_path, header=0)
    return df
