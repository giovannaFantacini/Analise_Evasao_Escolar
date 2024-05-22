import streamlit as st
import pandas as pd
import PreProcessamento.pre_processamento
import os
import PreProcessamento


# Configurações da página
st.set_page_config(page_title='Analise Evasao Escolar', layout='wide')

with st.container():
    col1, col2 = st.columns([1, 12])

    with col1:
        current_dir = os.path.dirname(__file__)
        img_path = os.path.join(current_dir, '../assets/logoIF.png')
        st.image(img_path, width=70)  

    with col2:
        st.title('Análise de Evasão Escolar')
        st.subheader('Insira seu arquivo para a análise')

    st.write('\n\n\n\n')

with st.container():
    uploaded_file = st.file_uploader("Escolha o arquivo", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        df_treated = PreProcessamento.pre_processamento.treat_file(df)
        st.session_state['uploaded_df'] = df_treated
    
    if 'uploaded_df' in st.session_state:
        df = st.session_state['uploaded_df']
        st.dataframe(df)

        if st.button('Remover arquivo'):
            del st.session_state['uploaded_df']
            st.experimental_rerun()
        
        