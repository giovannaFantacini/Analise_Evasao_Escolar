import streamlit as st
import pandas as pd
import utils
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests

# Função para ler a URL de configuração do MongoDB
def ler_url(config_file):
    with open(config_file, 'r') as file:
        url = file.readline().strip()
    return url

DATABASE_NAME = 'Historico'
COLLECTION_NAME = 'HistoricoSuap'

# Função para carregar dados do MongoDB
@st.cache_data
def carrega_dados(uploaded_file=None):
    if uploaded_file is not None:
        # Se um arquivo foi carregado, use-o
        df = uploaded_file
    else:
        # # Diretório atual e caminho do arquivo de configuração
        # current_dir = os.path.dirname(__file__)
        # config_path = os.path.join(current_dir, '../config.txt')

        # # Ler URL de configuração
        # url = ler_url(config_path)

        url = st.secrets["DB_URL"]

        # Conectar ao MongoDB
        client = MongoClient(url, server_api=ServerApi('1'))
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Carregar os dados da coleção em um DataFrame
        cursor = collection.find()
        df = pd.DataFrame(list(cursor))

        # Fechar a conexão
        client.close()

    return df

def carrega_estados():
    estados_brasileiros = [
    {"id": 12, "sigla": "AC", "nome": "Acre"},
    {"id": 27, "sigla": "AL", "nome": "Alagoas"},
    {"id": 13, "sigla": "AM", "nome": "Amazonas"},
    {"id": 16, "sigla": "AP", "nome": "Amapá"},
    {"id": 29, "sigla": "BA", "nome": "Bahia"},
    {"id": 23, "sigla": "CE", "nome": "Ceará"},
    {"id": 53, "sigla": "DF", "nome": "Distrito Federal"},
    {"id": 32, "sigla": "ES", "nome": "Espírito Santo"},
    {"id": 52, "sigla": "GO", "nome": "Goiás"},
    {"id": 21, "sigla": "MA", "nome": "Maranhão"},
    {"id": 31, "sigla": "MG", "nome": "Minas Gerais"},
    {"id": 50, "sigla": "MS", "nome": "Mato Grosso do Sul"},
    {"id": 51, "sigla": "MT", "nome": "Mato Grosso"},
    {"id": 15, "sigla": "PA", "nome": "Pará"},
    {"id": 25, "sigla": "PB", "nome": "Paraíba"},
    {"id": 26, "sigla": "PE", "nome": "Pernambuco"},
    {"id": 22, "sigla": "PI", "nome": "Piauí"},
    {"id": 41, "sigla": "PR", "nome": "Paraná"},
    {"id": 33, "sigla": "RJ", "nome": "Rio de Janeiro"},
    {"id": 24, "sigla": "RN", "nome": "Rio Grande do Norte"},
    {"id": 43, "sigla": "RS", "nome": "Rio Grande do Sul"},
    {"id": 11, "sigla": "RO", "nome": "Rondônia"},
    {"id": 14, "sigla": "RR", "nome": "Roraima"},
    {"id": 42, "sigla": "SC", "nome": "Santa Catarina"},
    {"id": 28, "sigla": "SE", "nome": "Sergipe"},
    {"id": 35, "sigla": "SP", "nome": "São Paulo"},
    {"id": 17, "sigla": "TO", "nome": "Tocantins"}
    ]


    return estados_brasileiros

@st.cache_data
def carrega_municipios_por_estado(estado_id):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado_id}/municipios"

    response = requests.get(url)
    data = response.json()

    # Gerar lista de nomes dos municípios
    municipios_nomes = [item["nome"] for item in data]
    return municipios_nomes
