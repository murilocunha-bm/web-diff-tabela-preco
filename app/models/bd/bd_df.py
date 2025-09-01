#!.venv/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
from datetime import datetime
from os import getenv
#
# biblioteca propria do sistema
from app.models.bd.sqlserver_conn import SQLServerConnection


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
        print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Montando tabela precos vigentes...")
    
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
        # print(df.head())  # Mostra as primeiras linhas da tabela
        
        if not df.empty:
            validade_inicial = df.iloc[0, 3]    # primeira linha e coluna ValidadeInicial
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 👉🏻 Validade inicial da tabela {validade_inicial}")
            df.to_excel(nome_xlsx_destino, index=False)
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 📂 Preco vigente gravado em: {nome_xlsx_destino}")
        else:
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ Nenhum registro de preços anterior encontrado. Verifique a data inicial da tabela")

    else:
        print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 💀 - Erro ao conectar ao banco de dados.")
        df = pd.DataFrame()

    bd.fechar_conexao()
    return df
