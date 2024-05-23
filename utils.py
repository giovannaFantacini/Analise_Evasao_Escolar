import streamlit as st
import pandas as pd
import utils
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Função para ler a URL de configuração do MongoDB
def ler_url(config_file):
    with open(config_file, 'r') as file:
        url = file.readline().strip()
    return url

DATABASE_NAME = 'TCC'
COLLECTION_NAME = 'BaseSuap'

# Função para carregar dados do MongoDB
@st.cache_data
def carrega_dados(uploaded_file=None):
    if uploaded_file is not None:
        # Se um arquivo foi carregado, use-o
        df = uploaded_file
    else:
        # # Diretório atual e caminho do arquivo de configuração
        # current_dir = os.path.dirname(__file__)
        # config_path = os.path.join(current_dir, 'config.txt')

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
