import streamlit as st
import pandas as pd
import PreProcessamento.pre_processamento
import os
import PreProcessamento
import utils

# Configurações da página
st.set_page_config(page_title='Analise Evasao Escolar', layout='wide')

lista_estados = utils.carrega_estados()
lista_estados_siglas = [""] + [estado["sigla"] for estado in utils.carrega_estados()]

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
    st.write('Aqui educadores de Instituições que usam o sistema unificado de Administração Pública - SUAP, poderão inserir o relatorio gerado no sistema para que os graficos sejam gerados de acordo com as informações de sua instituição.')
    st.write('Para inserir as infomrações da sua instituição gere o arquivo no formato csv ou xlsx com os seguintes campos: ')
    st.write('1. Ano Letivo de Previsão de Conclusão')
    st.write('2. Ano de Ingresso')
    st.write('3. Campus')
    st.write('4. Cidade')
    st.write('5. Código Curso')
    st.write('6. Data da Colação')
    st.write('7. Data da Defesa do TCC')
    st.write('8. Data de Conclusão de Curso')
    st.write('9. Data de Integralização')
    st.write('10. Data de Matrícula')
    st.write('11. Deficiência')
    st.write('12. Descrição do Curso')
    st.write('13. Estado')
    st.write('14. Etnia/Raça/Cor')
    st.write('15. Forma de Ingresso')
    st.write('16. Modalidade')
    st.write('17. Percentual de Progresso')
    st.write('18. Período Letivo de Integralização')
    st.write('19. Período de Ingresso')
    st.write('20. Sexo')
    st.write('21. Situação no Curso')
    st.write('22. Tipo de Escola de Origem')
    st.write('23. Turno')
    st.write('24. Prática Profissional Pendente')
    st.write('25. Colação de Grau Pendente')
    st.write('26. Atividades Complementares Pendente')
    st.write('27. Carga-Horária de TCC Pendente')
    st.write('28. Carga-Horária de Prática Profissional Pendente')
    st.write('29. Registro de TCC Pendente')
    st.write('30. Carga-Horária de Seminário Pendente')
    st.write('31. Carga-Horária Eletiva Pendente')
    st.write('32. Carga-Horária Optativa Pendente')
    st.write('33. Carga-Horária Obrigatória Pendente')
    st.write('34. Registro do ENADE')

    # Seleciona o estado
    estado_selecionado = st.selectbox(
        'Selecione o estado de origem da instituição:',
        lista_estados_siglas
    )

    # Encontra o ID do estado selecionado com base na sigla
    estado_selecionado = next((estado for estado in lista_estados if estado["sigla"] == estado_selecionado), None)
    estado_id = estado_selecionado["id"] if estado_selecionado else None

    # Carrega os municípios do estado selecionado se houver um ID válido
    lista_municipios = utils.carrega_municipios_por_estado(estado_id) if estado_id else []

    cidade = st.selectbox(
        'Além disso, também é necessário selecionar a cidade de origem da instituição:',
        lista_municipios,
    )
    


with st.container():
    uploaded_file = st.file_uploader("Escolha o arquivo", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        if not cidade:
            st.warning("Por favor, selecione a cidade de origem da instituição para continuar o processamento.")
        else:
            if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
    
            df_treated = PreProcessamento.pre_processamento.treat_file(df, cidade)
            st.session_state['uploaded_df'] = df_treated
    
    if 'uploaded_df' in st.session_state:
        df = st.session_state['uploaded_df']
        st.dataframe(df)

        if st.button('Remover arquivo'):
            del st.session_state['uploaded_df']
            st.experimental_rerun()
        
        