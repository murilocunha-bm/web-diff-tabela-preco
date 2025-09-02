#!.venv/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
from datetime import datetime
from os import getenv
#
# biblioteca propria do sistema
from app.models.bd.sqlserver_conn import SQLServerConnection
from app.controllers.loggers import logger


def pegar_precos_vigentes_bd(sql_tabela_precos, nome_xlsx_destino):
    """Função para pegar os preços vigentes do banco de dados."""

    SERVER = getenv('SQLSERVER_HOST')
    DATABASE = getenv('SQLSERVER_DATABASE')
    USERNAME = getenv('SQLSERVER_USER')
    PASSWORD = getenv('SQLSERVER_PASSWORD')

    # Conectar ao banco de dados sql server
    bd = SQLServerConnection(SERVER, DATABASE, USERNAME, PASSWORD)
    
    # Escolher entre conexao PyODBC ou SQLAlchemy - Pandas é melhor com SQLAlchemy
    # conn = bd.conectar_odbc()
    conn = bd.conectar_sqlalchemy()
    
    if conn:
        logger.info(f'Montando tabela precos vigentes...')
    
        # Fazer SELECT
        df = pd.read_sql(sql_tabela_precos, conn)
        df.columns = [
            'CodigoEmpresa',
            'TabelaPreco',
            'Codigo',
            'ValidadeInicial',
            'Produtos',
            'R$',
            'PercToleranciaParaMais',
            'ValorToleranciaParaMais',
        ]
        df = df.astype(
            {
                'CodigoEmpresa': int,
                'TabelaPreco': str,
                'Codigo': int,
                'ValidadeInicial': 'datetime64[ns]',
                'Produtos': str,
                'R$': float,
                'PercToleranciaParaMais': float,
                'ValorToleranciaParaMais': float,
            }
        )
        # df['ValidadeInicial'] = df['ValidadeInicial'].dt.date
        # print(df.head())  # Mostra as primeiras linhas da tabela
        
        if not df.empty:
            validade_inicial = df.iloc[0, 3]    # primeira linha e coluna ValidadeInicial
            logger.info(f'👉🏻 Validade inicial da tabela {datetime.strftime(validade_inicial, '%d/%m/%Y')}')
            df.to_excel(nome_xlsx_destino, index=False)
            logger.info(f'📂 Preco vigente gravado em: {nome_xlsx_destino}')
        else:
            logger.info(f'❌ Nenhum registro de preços anterior encontrado. Verifique a data inicial da tabela')

    else:
        logger.info(f'💀 - Erro ao conectar ao banco de dados')
        df = pd.DataFrame()

    bd.fechar_conexao()
    return df
