import analises_graficas as graphs
import streamlit as st
import pandas as pd
import utils
import os


st.set_page_config(page_title='Analise Evasao Escolar', layout='wide')

df = utils.carrega_dados()

cursos_com_matriculados = df[df['Situacao no Curso'] == 'Matriculado']['Descricao do Curso'].unique()
cursos_com_matriculados = [curso for curso in cursos_com_matriculados if curso != 'ESPECIALIZACAO EM ENSINO DE CIENCIAS DA NATUREZA E MATEMATICA']
df_cursos = df[df['Descricao do Curso'].isin(cursos_com_matriculados)]
cursos_ordenados = sorted(df_cursos['Descricao do Curso'].unique())

cursos_ordenados = sorted(df_cursos['Descricao do Curso'].unique())

for curso in cursos_ordenados:
    if st.sidebar.button(curso):
        st.session_state['curso_selecionado'] = curso
        st.session_state['pagina_atual'] = 'Curso'
        st.experimental_rerun()

if 'curso_selecionado' in st.session_state:
    curso = st.session_state['curso_selecionado']
    df = df[df['Descricao do Curso'] == curso]
else:
    curso = 'BACHARELADO EM ENGENHARIA DE COMPUTACAO'
    df = df[df['Descricao do Curso'] == curso]

with st.container():
    col1, col2 = st.columns([1, 12])  

    with col1:
        current_dir = os.path.dirname(__file__)
        img_path = os.path.join(current_dir, '../assets/logoIF.png')
        st.image(img_path, width=70)  

    with col2:
        st.title('Análise de Evasão Escolar')
        st.subheader(curso)

    st.write('\n\n\n\n')

with st.container():
    if int(df['Ano de Ingresso'].min()) != int(df['Ano de Ingresso'].max()):
        ano_inicio, ano_fim = st.slider(
        "Selecione o intervalo de busca",
        min_value=int(df['Ano de Ingresso'].min()),  
        max_value=int(df['Ano de Ingresso'].max()),  
        value=(int(df['Ano de Ingresso'].min()), int(df['Ano de Ingresso'].max()))
        )
        df_filtrado = df[(df['Ano de Ingresso'] >= ano_inicio) & (df['Ano de Ingresso'] <= ano_fim)]
    else:
        df_filtrado = df

with st.container():
    col1, col2 = st.columns([5, 4])
    
    with col1:
        fig1 = graphs.grafico_totalAlunos_evasao(df_filtrado)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = graphs.grafico_perfil_evasão(df_filtrado)
        st.plotly_chart(fig2, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns([5, 4])
    
    with col1:
        fig1 = graphs.grafico_barras_situacao_curso(graphs.adicionar_faixa_progresso(df_filtrado.copy()), 'Faixa de Progresso', 'Evasao', 'Total de Evasões por percentual de progresso')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        option = st.selectbox(
        "Selecione um ano de ingresso especifico para ver a situação no curso",
        (sorted(df['Ano de Ingresso'].unique().tolist())),
        index=None)
        if option != None:
            df_filtra_anoIngresso = df[df['Ano de Ingresso'] == option]
        else: 
            df_filtra_anoIngresso = df
        fig2 = graphs.grafico_perfil_curso(df_filtra_anoIngresso, 'Situacao no Curso')
        st.plotly_chart(fig2, use_container_width=True)

with st.container():
    col1, col2 = st.columns([5, 4])
    
    with col1:
        fig1 = graphs.grafico_formacao_prazo(df_filtrado, 'Ano de Ingresso', 'Formado', 'Total de Alunos Formados por Ano de Ingresso')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = graphs.grafico_barras_situacao_curso(df_filtrado, 'Ano de Ingresso', 'Matriculado', 'Total de Alunos Matriculados por Ano de Ingresso')
        st.plotly_chart(fig2, use_container_width=True)

with st.container():
    df_filtrado = df[df['Situacao no Curso'] == 'Matriculado']
    
    # Título acima das colunas
    st.markdown('### Perfil dos Alunos Matriculados no Curso')

    # Criação das colunas
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    # Primeira Coluna: Gráfico por Sexo
    with col1:
        fig1 = graphs.grafico_perfil_curso(df_filtrado, 'Genero')
        st.plotly_chart(fig1, use_container_width=True)
    
    # Segunda Coluna: Gráfico por Etnia/Raça/Cor
    with col2:
        fig2 = graphs.grafico_perfil_curso(df_filtrado, 'Etnia/Raca/Cor')
        st.plotly_chart(fig2, use_container_width=True)

    # Terceira Coluna: Gráfico por Tipo de Escola de Origem
    with col3:
        fig3 = graphs.grafico_perfil_curso(df_filtrado, 'Tipo de Escola de Origem')
        st.plotly_chart(fig3, use_container_width=True)

    # Quarta Coluna: Gráfico por Cidade
    with col4:
        fig4 = graphs.grafico_perfil_curso(df_filtrado, 'Cidade')
        st.plotly_chart(fig4, use_container_width=True)

with st.container():
    df_filtrado = df[df['Situacao no Curso'] == 'Formado']
    
    # Título acima das colunas
    st.markdown('### Perfil dos Alunos Formados no Curso')

    # Criação das colunas
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    # Primeira Coluna: Gráfico por Sexo
    with col1:
        fig1 = graphs.grafico_perfil_curso(df_filtrado, 'Genero')
        st.plotly_chart(fig1, use_container_width=True)
    
    # Segunda Coluna: Gráfico por Etnia/Raça/Cor
    with col2:
        fig2 = graphs.grafico_perfil_curso(df_filtrado, 'Etnia/Raca/Cor')
        st.plotly_chart(fig2, use_container_width=True)

    # Terceira Coluna: Gráfico por Tipo de Escola de Origem
    with col3:
        fig3 = graphs.grafico_perfil_curso(df_filtrado, 'Tipo de Escola de Origem')
        st.plotly_chart(fig3, use_container_width=True)

    # Quarta Coluna: Gráfico por Cidade
    with col4:
        fig4 = graphs.grafico_perfil_curso(df_filtrado, 'Cidade')
        st.plotly_chart(fig4, use_container_width=True)


