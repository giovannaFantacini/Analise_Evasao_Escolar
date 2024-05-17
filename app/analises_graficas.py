import plotly.express as px
import pandas as pd

cores_descricao_curso = {
    'TECNICO EM INFORMATICA INTEGRADO AO ENSINO MEDIO': '#4CAF50',  # Verde
    'TECNOLOGIA EM SISTEMAS PARA INTERNET': '#CDDC39',  # Lima
    'TECNICO EM AUTOMACAO INDUSTRIAL': '#FFEB3B',  # Amarelo
    'BACHARELADO EM ENGENHARIA DE COMPUTACAO': '#FFC107',  # Âmbar
    'TECNOLOGIA EM MECATRONICA INDUSTRIAL': '#FF9800',  # Laranja
    'LICENCIATURA EM FISICA': '#FF5722',  # Laranja Escuro
    'TECNICO EM ADMINISTRACAO': '#795548',  # Marrom
    'TECNICO EM MANUTENCAO E SUPORTE EM INFORMATICA': '#9E9E9E',  # Cinza
    'LICENCIATURA EM MATEMATICA': '#607D8B',  # Azul Cinza
    'TECNICO EM COMERCIO INTEGRADO AO ENSINO MEDIO NA MODALIDADE DE JOVENS E ADULTOS': '#E91E63',  # Rosa
    'TECNICO EM ADMINISTRACAO INTEGRADO AO ENSINO MEDIO': '#9C27B0',  # Roxo
    'TECNICO EM AUTOMACAO INDUSTRIAL INTEGRADO AO ENSINO MEDIO': '#673AB7',  # Roxo Profundo
    'ESPECIALIZACAO EM ENSINO DE CIENCIAS DA NATUREZA E MATEMATICA': '#3F51B5'  # Índigo
}

cores_situacao_curso = {
    'Matriculado': '#009688',  # Turquesa
    'Evasao': '#C7282A',  # Vermelho
    'Cancelado': '#E91E63',  # Rosa
    'Formado': '#9C27B0',  # Roxo
    'Matricula Vinculo Institucional': '#673AB7',  # Roxo Profundo
    'Concluido': '#3F51B5',  # Índigo
    'Cancelamento Compulsorio': '#2196F3',  # Azul
    'Jubilado': '#03A9F4',  # Azul Claro
    'Transferido Interno': '#00BCD4',  # Ciano
    'Trancado Voluntariamente': '#009688',  # Turquesa
    'Cancelamento por Desligamento': '#4CAF50',  # Verde
    'Transferido Externo': '#8BC34A',  # Verde Claro
    'Cancelamento por Duplicidade': '#CDDC39',  # Lima
    'Trancado': '#FFEB3B',  # Amarelo,
    'Total Alunos' : '#379936'
}

cores_classificacoes = {
    'Homem': '#1565C0',  # Azul Profundo
    'Mulher': '#AD1457',  # Rosa Escuro
    'Birigui': '#2E7D32',  # Verde Escuro
    'Outra cidade': '#CDDC39',  # Verde Lima Claro
    'Publica': '#FF7043',  # Vermelho Coral
    'Privada': '#6A1B9A',  # Roxo Escuro
    'Branca': '#4DD0E1',  # Azul Claro
    'Parda': '#5D4037',  # Marrom Escuro
    'Não declarado': '#808000',  # Verde Oliva
    'Amarela': '#F57F17',  # Amarelo Escuro
    'Preta': '#3E2723',  # Preto Café
    'Indigena': '#BF360C'  # Vermelho Terracota
}
cores_gradiente = {
    '#005A5B',  
    '#00796B',         
    '#00897B',  
    '#009688',       
    '#33A9A5',       
    '#66BBB9',  
    '#99CDCD'
}


# Função para criar o gráfico de barras com duas colunas sendo uma de total de alunos e uma de evasão
def grafico_totalAlunos_evasao(df):
    tabela_frequencias = df.groupby(['Ano de Ingresso', 'Situacao no Curso']).size().unstack(fill_value=0)
    tabela_frequencias['Total Alunos'] = tabela_frequencias.sum(axis=1)
    
    # Resetar o índice
    tabela_frequencias = tabela_frequencias.reset_index()

    # Plotar o gráfico de barras
    fig = px.bar(tabela_frequencias, 
                 x='Ano de Ingresso', 
                 y=['Total Alunos', 'Evasao'],
                 barmode='group', 
                 text_auto=True,
                 title='Total de Alunos e Evasão por Ano de Ingresso',
                 color_discrete_map= {
                                  'Total Alunos': cores_situacao_curso['Total Alunos'],
                                  'Evasao': cores_situacao_curso['Evasao']
                              })
    
    # Remover a label do eixo X
    fig.update_xaxes(title_text='', showticklabels=True, dtick=1)

    # Remover a label do eixo Y e os valores dos ticks
    fig.update_yaxes(title_text='', showticklabels=False)

    # Atualizar layout para mostrar os rótulos melhor
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
        legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=1.02,  
            xanchor="right",
            x=1  
        ),
        legend_title_text='',  # Remove legend title
        showlegend=True
    )
    fig.update_layout(autosize=True)
    
    return fig

# Função calcula a taxa de evasão por curso ou modalidade
def taxa_evasao(df, curso_selecionado=None, modalidade_selecionada=None):

    if curso_selecionado:
        df = df[df['Descricao do Curso'] == curso_selecionado]
    if modalidade_selecionada:
        df = df[df['Modalidade'] == modalidade_selecionada]

    evasion_df = df[df['Situacao no Curso'] == 'Evasao']

    # Conta o número de evasões por curso
    evasion_counts = evasion_df['Descricao do Curso'].value_counts()

    # Conta o número total de alunos por curso
    total_counts = df['Descricao do Curso'].value_counts()

    # Calcula a taxa de evasão
    evasion_rates = (evasion_counts / total_counts).sort_values(ascending=False) * 100

    return evasion_rates

# Grafico de pizza que mostra as taxas de evasão por curso
def grafico_cursos_maior_evasão(df, modalidade_selecionada=None):
   
    if modalidade_selecionada:
        evasion_rates_df = taxa_evasao(df,modalidade_selecionada = modalidade_selecionada).reset_index()
    else:
        evasion_rates_df = taxa_evasao(df).reset_index()

    evasion_rates_df.columns = ['Descricao do Curso', 'Taxa de Evasão']

    # Plotting the donut chart using Plotly Express
    fig = px.pie(evasion_rates_df,
                values='Taxa de Evasão',
                names='Descricao do Curso',
                hole=0.4,
                title='Cursos com maior Taxa de Evasão',
                color_discrete_sequence=[cores_descricao_curso[curso] for curso in evasion_rates_df['Descricao do Curso']])
    
    fig.update_layout(
        margin=dict(t=60, l=0, r=0, b=120),  
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,  
            xanchor="center",
            x=0.5
        ),
        autosize=True,
        legend_title=dict(font=dict(size=10)),
        legend_font=dict(size=10)
    )

    fig.update_traces(textinfo='percent', textfont_size=12)
    
    return fig

#Grafico de barras para mostrar a situação dos alunos no curso, seja formado, matriculado, etc
def grafico_barras_situacao_curso(df, x, y, title):

    tabela_frequencias = df.groupby([x, 'Situacao no Curso']).size().unstack(fill_value=0)
    tabela_frequencias = tabela_frequencias.reset_index()
    tabela_frequencias = tabela_frequencias[tabela_frequencias[y] > 0]

    cor_situacao = cores_situacao_curso.get(y, '#000000')

    fig = px.bar(tabela_frequencias, 
                 x=x, 
                 y=y,
                 text_auto=True,
                 title=title,
                 color_discrete_sequence=[cor_situacao]
                )

    # Remover a label do eixo X
    fig.update_xaxes(title_text='', showticklabels=True, dtick=1)

    # Remover a label do eixo Y e os valores dos ticks
    fig.update_yaxes(title_text='', showticklabels=False)

    # Atualizar layout para mostrar os rótulos melhor
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(showlegend=True, legend_title_text='')

    fig.update_layout(autosize=True)
    
    return fig

def grafico_formacao_prazo(df, x, y, title):
    # Conversão e verificação das colunas de data
    df['Data de Conclusao de Curso'] = pd.to_datetime(df['Data de Conclusao de Curso'], format='%d/%m/%Y', errors='coerce')
    df['Ano Letivo de Previsao de Conclusao'] = df['Ano Letivo de Previsao de Conclusao'].astype(int)

    # Adiciona uma nova coluna para indicar se a formatura foi dentro ou após o prazo
    df['Dentro do Prazo'] = df.apply(lambda row: 'Dentro do Prazo' if row['Data de Conclusao de Curso'].year <= row['Ano Letivo de Previsao de Conclusao'] else 'Fora do Prazo', axis=1)

    # Filtra apenas alunos formados
    df_formados = df[df['Situacao no Curso'] == y]
    tabela_frequencias = df_formados.groupby([x, 'Dentro do Prazo']).size().unstack(fill_value=0).reset_index()

    # Cria o gráfico de barras
    fig = px.bar(tabela_frequencias, 
                 x=x, 
                 y=tabela_frequencias.columns[1:],  # Colunas resultantes do unstack
                 barmode='group',
                 text_auto=True,
                 title=title,
                 labels={'value':'Total de Alunos', 'variable':'Status de Conclusão'},
                 color_discrete_map={'Dentro do Prazo': '#D1C4E9', 'Fora do Prazo': '#4A148C'}  # Cores especificadas para cada status
                )
    
    fig.update_xaxes(title_text='', showticklabels=True, dtick=1)
    fig.update_yaxes(title_text='', showticklabels=False)
    fig.update_layout(
        legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=1.02,  
            xanchor="right",
            x=1  
        ),
        legend_title_text='',  # Remove legend title
        showlegend=True
    )
    fig.update_layout(autosize=True)

    return fig

#Grafico para mostrar o total de alunos por modalidade
def grafico_total_alunos_modalidade(df):
    enrolled_df = df[df['Situacao no Curso'] == 'Matriculado']
    enrolled_counts = enrolled_df['Modalidade'].value_counts().reset_index()
    enrolled_counts.columns = ['Modalidade', 'Total Matriculados']


    # Mapear cada modalidade para uma cor no gradiente
    cores_modalidade = {mod: cor for mod, cor in zip(enrolled_counts['Modalidade'], cores_gradiente)}

    # Plotar o gráfico de barras com Plotly Express usando as cores do gradiente
    fig = px.bar(
        enrolled_counts,
        x='Modalidade',
        y='Total Matriculados',
        title='Total de Alunos Matriculados por Modalidade em 2024',
        text_auto=True,
        color='Modalidade',
        color_discrete_map=cores_modalidade
    )

    # Remover legendas e rótulos desnecessários
    fig.update_layout(showlegend=False, xaxis_title='', yaxis_title='', yaxis_showticklabels=False)

    # Ajustar layout geral
    fig.update_traces(marker=dict(line=dict(color='#000000', width=1), opacity=0.8))
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    fig.update_layout(autosize=True)

    return fig

def calcula_metricas_evasao(df):
    evasion_df = df[df['Situacao no Curso'] == 'Evasao']

    def maior_porcentagem(coluna):
        # Calcula a porcentagem para cada atributo na coluna
        porcentagens = (evasion_df[coluna].value_counts(normalize=True) * 100)
        # Encontra o valor máximo e o atributo correspondente
        max_porcentagem = porcentagens.max()
        max_atributo = porcentagens.idxmax()
        return (max_atributo, max_porcentagem)

    # Dicionário para armazenar os resultados
    resultados = {
        'Genero': maior_porcentagem('Genero'),
        'Tipo de Escola de Origem': maior_porcentagem('Tipo de Escola de Origem'),
        'Etnia/Raca/Cor': maior_porcentagem('Etnia/Raca/Cor'),
        'Cidade': maior_porcentagem('Cidade')
    }
    return resultados

def grafico_perfil_evasão(df):
    resultados = calcula_metricas_evasao(df)
    # Preparando os dados para o gráfico
    categorias = []
    porcentagens = []
    textos = []

    for categoria, (nome, pct) in resultados.items():  
        categorias.append(categoria)
        porcentagens.append(pct) 
        textos.append(f"{nome}\n{pct:.2f}%")

    # Criando o DataFrame
    data = pd.DataFrame({
        'Categoria': categorias,
        'Porcentagem': porcentagens,
        'Texto': textos
    })

    # Criando o gráfico de bolhas
    fig = px.scatter(data, 
                    x="Categoria", 
                    y=[1]*len(data),  # Cria uma coluna com todos os valores como 1 para alinhar horizontalmente
                    size="Porcentagem", 
                    color="Categoria",
                    text="Texto",  # Adiciona o texto das categorias nas bolhas
                    size_max=100,
                    )

    # Ajustando detalhes do layout
    fig.update_layout(
        title="Perfil dos alunos que evadiram",
        xaxis_title="",
        yaxis_title="",
        yaxis=dict(showticklabels=False), 
        xaxis=dict(showticklabels=True),
        showlegend=False,  # Esconde a legenda padrão
    )

    # Ajusta os detalhes dos marcadores (bolhas)
    fig.update_traces(
        textposition='middle center',
        marker=dict(line=dict(width=2, color='DarkSlateGrey')),
        textfont_size=14,
        mode='markers+text'
    )
    
    fig.update_layout(autosize=True)

    return fig 

def adicionar_faixa_progresso(df):
    df['Percentual de Progresso'] = df['Percentual de Progresso'].str.replace(',','.').astype(float)
    bins = [0, 25, 50, 75, 100]
    labels = ['0-25%', '25-50%', '50-75%', '75-100%']
    df['Faixa de Progresso'] = pd.cut(df['Percentual de Progresso'], bins=bins, labels=labels, include_lowest=True)
    return df

def grafico_perfil_curso(df, value):
    counts = df[value].value_counts().reset_index()
    counts.columns = [value, 'Total']

    cores = None
    if value == 'Situacao no Curso':
        cores = {situacao: cores_situacao_curso[situacao] for situacao in counts[value] if situacao in cores_situacao_curso}
    elif value in ['Genero', 'Etnia/Raca/Cor', 'Cidade', 'Tipo de Escola de Origem']:
        cores = {categoria: cores_classificacoes[categoria] for categoria in counts[value] if categoria in cores_classificacoes}
    
    fig = px.pie(counts, 
                 values='Total', 
                 names=value, 
                 title=f'{value}',
                 color=value, 
                 color_discrete_map=cores) 
    
    return fig
