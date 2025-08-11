# Import packages
import pandas as pd

features = [
    "Ano Letivo de Previsão de Conclusão", "Ano de Ingresso", "Campus", "Cidade", 
    "Data da Colação", "Data da Defesa do TCC", "Data de Conclusão de Curso",
    "Data de Matrícula", "Deficiência", "Descrição do Curso", "Estado", "Etnia/Raça/Cor",
    "Forma de Ingresso", "Modalidade", "Percentual de Progresso", 
    "Período de Ingresso", "Sexo", "Situação no Curso", "Tipo de Escola de Origem", "Turno",
    "Prática Profissional Pendente", "Colação de Grau Pendente", "Atividades Complementares Pendente",
    "Carga-Horária de TCC Pendente", "Carga-Horária de Prática Profissional Pendente", "Registro de TCC Pendente",
    "Carga-Horária de Seminário Pendente", "Carga-Horária Eletiva Pendente", "Carga-Horária Optativa Pendente",
    "Carga-Horária Obrigatória Pendente", "Registro do ENADE"
]

def treat_file(df, cidade_origem):
    
    df = df[features]

    df['Modalidade'] = df['Modalidade'].str.split('/').str[0]

    def ajustar_cidade(cidade):
        if cidade.upper() == cidade_origem.upper():
            return cidade_origem
        elif cidade == '-' or '':
            return '-'
        else:
            return 'Outra cidade'

    df['Cidade'] = df['Cidade'].apply(ajustar_cidade) if cidade_origem is not '' else df['Cidade']


    def ajustar_situacao(situacao_curso):
        if situacao_curso == 'Matrícula Vínculo Institucional':
            return 'Matriculado'
        elif situacao_curso == 'Concluído':
            return 'Formado'
        else:
            return situacao_curso

    df['Situação no Curso'] = df['Situação no Curso'].apply(ajustar_situacao)

    def ajustar_genero(genero):
        if genero == 'M':
            return 'Homem'
        elif genero == 'F':
            return 'Mulher'

    df['Sexo'] = df['Sexo'].apply(ajustar_genero)

    df = df.rename(columns={
        'Sexo' : 'Gênero'
    })

    df['Descrição do Curso'] = df['Descrição do Curso'].str.title()

    def categorize_forma_ingresso(text):
        text = text.lower()
        if 'ampla concorrência' in text:
            return 'Ampla Concorrência'
        elif ('escolas públicas' in text or 'ep' in text or 'escola pública' in text) and 'renda' in text and ('ppi' in text or 'pretos' in text or 'etnia' in text) and ('pcd' in text or 'deficiência' in text):
            if 'independente da renda' in text or 'independente de renda' in text:
                return 'Escola Pública + PPI + PCD'
            return 'Escola Pública + Renda + PPI + PCD'
        elif ('escolas públicas' in text or 'ep' in text or 'escola pública' in text) and 'renda' in text and ('ppi' in text or 'pretos' in text or 'etnia' in text):
            if 'independente da renda' in text or 'independente de renda' in text:
                return 'Escola Pública + PPI'
            return 'Escola Pública + Renda + PPI'
        elif ('escolas públicas' in text or 'ep' in text or 'escola pública' in text) and 'renda' in text and ('pcd' in text or 'deficiência' in text):
            if 'independente da renda' in text or 'independente de renda' in text:
                return 'Escola Pública + PCD'
            return 'Escola Pública + Renda + PCD'
        elif ('escolas públicas' in text or 'ep' in text or 'escola pública' in text) and 'renda' in text:
            if 'independente da renda' in text or 'independente de renda' in text:
                return 'Escola Pública'
            return 'Escola Pública + Renda'
        elif ('escolas públicas' in text or 'ep' in text or 'escola pública' in text) and ('ppi' in text or 'pretos' in text or 'etnia' in text) and ('pcd' in text or 'deficiência' in text):
            return 'Escola Pública + PPI + PCD'
        elif ('escolas públicas' in text or 'ep' in text or 'escola pública' in text) and ('ppi' in text or 'pretos' in text or 'etnia' in text):
            return 'Escola Pública + PPI'
        elif ('escolas públicas' in text or 'ep' in text or 'escola pública' in text) and ('pcd' in text or 'deficiência' in text):
            return 'Escola Pública + PCD'
        elif 'escolas públicas' in text or 'ep' in text or 'escola pública' in text:
            return 'Escola Pública'
        elif 'transferência' in text:
            return 'Transferência'
        else:
            return 'Outros'
    
    # Dividir as modalidades conforme as categorias
    df['Forma de Ingresso'] = df['Forma de Ingresso'].apply(categorize_forma_ingresso)

    return df

