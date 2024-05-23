# Import packages
import pandas as pd

features = [
    "Ano Letivo de Previsão de Conclusão", "Ano de Ingresso", "Campus", "Cidade", "Código Curso",
    "Data da Colação", "Data da Defesa do TCC", "Data de Conclusão de Curso", "Data de Integralização",
    "Data de Matrícula", "Deficiência", "Descrição do Curso", "Estado", "Etnia/Raça/Cor",
    "Forma de Ingresso", "Modalidade", "Percentual de Progresso", "Período Letivo de Integralização",
    "Período de Ingresso", "Sexo", "Situação no Curso", "Tipo de Escola de Origem", "Turno",
    "Prática Profissional Pendente", "Colação de Grau Pendente", "Atividades Complementares Pendente",
    "Carga-Horária de TCC Pendente", "Carga-Horária de Prática Profissional Pendente", "Registro de TCC Pendente",
    "Carga-Horária de Seminário Pendente", "Carga-Horária Eletiva Pendente", "Carga-Horária Optativa Pendente",
    "Carga-Horária Obrigatória Pendente", "Registro do ENADE"
]

def treat_file(df):
    
    # Remove as linhas com a descrição de curso específica
    df = df.drop(df[(df['Modalidade'] == 'FIC' )| (df['Modalidade'] == 'Proeja FIC Fundamental')].index)

    df = df[features]

    df['Modalidade'] = df['Modalidade'].str.split('/').str[0]

    # def ajustar_cidade(cidade):
    #     if cidade == 'BIRIGUI':
    #         return 'Birigui'
    #     elif cidade == '-' or '':
    #         return '-'
    #     else:
    #         return 'Outra cidade'

    # df['Cidade'] = df['Cidade'].apply(ajustar_cidade)

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

    return df

