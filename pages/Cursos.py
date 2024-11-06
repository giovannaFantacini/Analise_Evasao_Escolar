import analises_graficas as graphs
import streamlit as st
import pandas as pd
import utils as utils
import os
from datetime import datetime


st.set_page_config(page_title='Analise Evasao Escolar', layout='wide')

button_style = """
<style>
    div.stButton > button {
        display: block;
        width: 100%;
        text-align: left;
        border: none;
        background: none;
        color: inherit;
        padding: 0;
        font: inherit;
        cursor: pointer;
        outline: inherit;
    }
</style>
"""

st.markdown(button_style, unsafe_allow_html=True)

if 'uploaded_df' in st.session_state:
    df_selecionado = st.session_state['uploaded_df']
    df = df_selecionado
else:
    df = utils.carrega_dados()

cursos_com_matriculados = df[df['Situação no Curso'] == 'Matriculado']['Descrição do Curso'].unique()
cursos_com_mais_de_um_ano = []
for curso in cursos_com_matriculados:
    anos_ingresso = df[df['Descrição do Curso'] == curso]['Ano de Ingresso'].unique()
    if len(anos_ingresso) > 1:
        cursos_com_mais_de_um_ano.append(curso)
df_cursos = df[df['Descrição do Curso'].isin(cursos_com_mais_de_um_ano)]
cursos_ordenados = sorted(df_cursos['Descrição do Curso'].unique())

for curso in cursos_ordenados:
    if st.sidebar.button(curso):
        st.session_state['curso_selecionado'] = curso
        st.session_state['pagina_atual'] = 'Curso'
        st.experimental_rerun()

if 'curso_selecionado' in st.session_state:
    curso = st.session_state['curso_selecionado']
    df = df[df['Descrição do Curso'] == curso]
else:
    curso = cursos_ordenados[0]
    df = df[df['Descrição do Curso'] == curso]

with st.container():
    col1, col2, col3 = st.columns([1, 10,5])  

    with col1:
        st.write('\n\n\n\n\n\n')
        current_dir = os.path.dirname(__file__)
        img_path = os.path.join(current_dir, '../assets/logoIF.png')
        st.image(img_path, width=70)  

    with col2:
        st.title('Análise de Evasão Escolar')
        st.subheader(curso)

    with col3:
        num_alunos = len(df[df['Situação no Curso'] == 'Matriculado'])
        st.markdown(f"""
            <div style="text-align: center;">
                <h1>{num_alunos}</h1>
                <p>Total de Alunos Matriculados</p>
            </div>
            """, unsafe_allow_html=True)
    
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
    col1, col2 = st.columns([1, 1])
    
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
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig1 = graphs.grafico_barras_situacao_curso(graphs.adicionar_faixa_progresso(df_filtrado.copy()), 'Faixa de Progresso', 'Evasão', 'Total de Evasões por percentual de progresso')
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
        fig2 = graphs.grafico_perfil_curso(df_filtra_anoIngresso, 'Situação no Curso')
        st.plotly_chart(fig2, use_container_width=True)

with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig1 = graphs.grafico_formacao_prazo(df_filtrado, 'Ano de Ingresso', 'Formado', 'Total de Alunos Formados por Ano de Ingresso')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = graphs.grafico_barras_situacao_curso(df_filtrado, 'Ano de Ingresso', 'Matriculado', 'Total de Alunos Matriculados por Ano de Ingresso')
        st.plotly_chart(fig2, use_container_width=True)

if df['Modalidade'].iloc[0] != "Técnico Integrado":
    with st.container():
        col1, col2 = st.columns([1, 1])

        with col1:
            fig1 = graphs.grafico_tempo_extra_alunos(df_filtrado)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            ano_atual = datetime.now().year
            option = st.selectbox(
            "Selecione um ano de previsão de conclusão para ver as pendências dos alunos",
            (sorted([ano for ano in df['Ano Letivo de Previsão de Conclusão'].unique() if ano < ano_atual])),
            index=None)
            if option != None:
                df_filtra_ano = df[df['Ano Letivo de Previsão de Conclusão'] == option]
            else: 
                df_filtra_ano = df
            fig2 = graphs.grafico_pendencias(df_filtra_ano)
            st.plotly_chart(fig2, use_container_width=True)

with st.container():
    col1, col2 = st.columns([1, 1])

    with col1:
        fig, df_taxa = graphs.grafico_taxa_evasao_formaIngresso(df_filtrado)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_10_data = df_taxa.sort_values(by="taxa_evasao", ascending=False).head(10)
        top_10_data["Total de Alunos"] = top_10_data["Ingressaram"]
        top_10_data["Total de Evasão"] = top_10_data["Evadiram"]
        top_10_data["Taxa de Evasão"] = top_10_data["taxa_evasao"]

        top_10_data.reset_index(drop=True, inplace=True)

        st.subheader("Top 10 Taxas de Evasão")
        st.table(top_10_data[['Forma de Ingresso', "Total de Alunos", "Total de Evasão", "Taxa de Evasão"]].style.format({
            "Total de Alunos": "{:.2f}", "Total de Evasão": "{:.2f}", "Taxa de Evasão": "{:.2f}"}))


with st.container():
    df_filtrado = df[df['Situação no Curso'] == 'Matriculado']
    
    # Título acima das colunas
    st.markdown('### Perfil dos Alunos Matriculados no Curso')

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

with st.container():
    df_filtrado = df[df['Situação no Curso'] == 'Formado']
    
    # Título acima das colunas
    st.markdown('### Perfil dos Alunos Formados no Curso')

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


