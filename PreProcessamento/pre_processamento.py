# Import packages
import pandas as pd

def treat_file(df):
    
    # Remove as linhas com a descrição de curso específica
    df = df.drop(df[(df['Modalidade'] == 'FIC' )| (df['Modalidade'] == 'Proeja FIC Fundamental')].index)

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

