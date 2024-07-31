import analises_graficas as graphs
import streamlit as st
import pandas as pd
import utils
import os

st.set_page_config(page_title='Analise Evasao Escolar', layout='wide')

if 'uploaded_df' in st.session_state:
    df_selecionado = st.session_state['uploaded_df']
    df = df_selecionado
else:
    df = utils.carrega_dados()


with st.container():
    col1, col2 = st.columns([1, 12])  

    with col1:
        current_dir = os.path.dirname(__file__)
        img_path = os.path.join(current_dir, 'assets/logoIF.png')
        st.image(img_path, width=70)  

    with col2:
        st.title('Análise de Evasão Escolar')

    st.write('\n\n\n\n')

with st.container():
    ano_inicio, ano_fim = st.slider(
    "Selecione o intervalo de busca",
    min_value=int(df['Ano de Ingresso'].min()),  
    max_value=int(df['Ano de Ingresso'].max()),  
    value=(int(df['Ano de Ingresso'].min()), int(df['Ano de Ingresso'].max()))
)
    df_filtrado = df[(df['Ano de Ingresso'] >= ano_inicio) & (df['Ano de Ingresso'] <= ano_fim)]

with st.container():
    col1, col2 = st.columns([1,1])
    
    with col1:
        fig1 = graphs.grafico_totalAlunos_evasao(df_filtrado)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = graphs.grafico_comparativo_evasao(df_filtrado, 'Etnia/Raça/Cor')
        st.plotly_chart(fig2, use_container_width=True)

with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        fig1 = graphs.grafico_comparativo_evasao(df_filtrado, 'Tipo de Escola de Origem')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = graphs.grafico_comparativo_evasao(df_filtrado, 'Gênero')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col3:
        fig3 = graphs.grafico_comparativo_evasao(df_filtrado, 'Cidade')
        st.plotly_chart(fig3, use_container_width=True)

with st.container():
    col1, col2 = st.columns([1,1])
    
    with col1:
        option = st.selectbox(
        "Selecione uma modalidade especifica para comparar a taxa de evasão entre cursos",
        (df['Modalidade'].unique().tolist()),
        index=None)
        if option != None:
            df_filtra_modalidade = df_filtrado[df['Modalidade'] == option]
        else: 
            df_filtra_modalidade = df_filtrado
        fig1 = graphs.grafico_cursos_maior_evasao(df_filtra_modalidade)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = graphs.grafico_total_alunos_modalidade(df)
        st.plotly_chart(fig2, use_container_width=True)
        
        


with st.container():
    df_filtrado = df[df['Situação no Curso'] == 'Matriculado']
    
    # Título acima das colunas
    st.markdown('### Perfil dos Alunos Matriculados na Instituição')

    # Criação das colunas
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    # Primeira Coluna: Gráfico por Sexo
    with col1:
        fig1 = graphs.grafico_perfil_curso(df_filtrado, 'Gênero')
        st.plotly_chart(fig1, use_container_width=True)
    
    # Segunda Coluna: Gráfico por Etnia/Raça/Cor
    with col2:
        fig2 = graphs.grafico_perfil_curso(df_filtrado, 'Etnia/Raça/Cor')
        st.plotly_chart(fig2, use_container_width=True)

    # Terceira Coluna: Gráfico por Tipo de Escola de Origem
    with col3:
        fig3 = graphs.grafico_perfil_curso(df_filtrado, 'Tipo de Escola de Origem')
        st.plotly_chart(fig3, use_container_width=True)

    # Quarta Coluna: Gráfico por Cidade
    with col4:
        fig4 = graphs.grafico_perfil_curso(df_filtrado, 'Cidade')
        st.plotly_chart(fig4, use_container_width=True)