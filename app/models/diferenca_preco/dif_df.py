#!.venv/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
from datetime import datetime
from os import remove, path
#
from app.models.diferenca_preco.excel_df import montar_tabela_unica
from app.models.bd.bd_df import pegar_precos_vigentes_bd
from constants import SQL_TB_LITORAL, SQL_TB_ST01, SQL_TB_SP02, SQL_TB_SP03
from constants import MAPA_TABELA_PRECO_NOVO_SP2
from constants import XLS_PRECO_NOVO_LITORAL, XLS_PRECO_NOVO_ST, XLS_PRECO_NOVO_SP2, XLS_PRECO_NOVO_SP3
from constants import XLS_PRECO_VIGENTE_LITORAL, XLS_PRECO_VIGENTE_ST, XLS_PRECO_VIGENTE_SP2, XLS_PRECO_VIGENTE_SP3
from constants import XLS_DIFERENCA_LITORAL, XLS_DIFERENCA_ST, XLS_DIFERENCA_SP2, XLS_DIFERENCA_SP3


def apagar_arquivos_criados_antes(arquivos_apagar):
    for arquivo in arquivos_apagar:
        if path.isfile(arquivo):
            remove(arquivo)
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 🗑 Arquivo {arquivo} excluído com sucesso.")
        else:
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ Arquivo {arquivo} não encontrado.")


def encontrar_diferencas_tabelas_precos(etapas: dict, preco_novo_filename: str):
    
    
    for etapa in etapas:
        print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Tabela de precos: {preco_novo_filename}...")
        df_precos_novos = montar_tabela_unica(
            filename=preco_novo_filename,
            mapa_precos_novos=etapa[0],
            nome_xlsx_destino=etapa[1],
        )
        if not df_precos_novos.empty:
            df_precos_vigentes = pegar_precos_vigentes_bd(
                sql_tabela_precos=etapa[2], 
                nome_xlsx_destino=etapa[3]
            )
            if not df_precos_vigentes.empty:
                result = encontrar_diferencas_precos(
                    nome_xlsx_diferenca=etapa[4],
                    df_antigo=df_precos_novos,
                    df_novo=df_precos_vigentes,
                    col_ligacao='Codigo',
                    col_diferenca='R$'
                )
                if not result.empty:
                    return result
                else:
                    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 🤷‍♂️ Nenhuma diferença de preços encontrada")
                    return pd.DataFrame()

        else:
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ Tabela de preços novos vazia. Verifique os dados.")
            return pd.DataFrame()
        

def encontrar_diferencas_precos(
        nome_xlsx_diferenca: str,
        df_antigo:pd.DataFrame,
        df_novo:pd.DataFrame,
        col_ligacao:str,
        col_diferenca:str
    ) -> pd.DataFrame:
    
    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Procurando diferencas...")

    df_diferenca_precos = pd.merge(
        df_antigo, 
        df_novo, 
        on=col_ligacao, 
        how='inner', 
        suffixes=('_novo', '_vigente')
    )

    # Filtra apenas onde os valores de R$ são diferentes (considerando NaN)
    df_diferentes = df_diferenca_precos[
        df_diferenca_precos[col_diferenca + '_novo'] != df_diferenca_precos[col_diferenca + '_vigente']
    ]
    # # Para considerar NaN como diferença
    # df_diferentes = df_diferenca_precos[
    #     (df_diferenca_precos['R$_novo'] != df_diferenca_precos['R$_vigente']) |
    #     (df_diferenca_precos['R$_novo'].isna() != df_diferenca_precos['R$_vigente'].isna())
    # ]

    col_desejadas = [
        'Codigo',
        'Produtos_vigente',
        'R$_vigente',
        'Produtos_novo',
        'R$_novo',
    ]
    print(df_diferentes[col_desejadas])
    
    # Seleciona apenas as colunas desejadas do DataFrame original. Copy cria uma cópia independente
    df_resultado = df_diferentes[col_desejadas].copy()

    df_resultado.to_excel(nome_xlsx_diferenca, index=False)
    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Preco diferente gravado em: {nome_xlsx_diferenca}")

    return df_resultado

def main(xls_preco_novo: str):
    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Apagando arquivos de resultado criados antes...")
    arquivos_apagar = [
        XLS_PRECO_NOVO_ST, XLS_PRECO_NOVO_SP2, XLS_PRECO_NOVO_SP3, XLS_PRECO_NOVO_LITORAL,
        XLS_PRECO_VIGENTE_ST, XLS_PRECO_VIGENTE_SP2, XLS_PRECO_VIGENTE_SP3, XLS_PRECO_VIGENTE_LITORAL,
        XLS_DIFERENCA_ST, XLS_DIFERENCA_SP2, XLS_DIFERENCA_SP3, XLS_DIFERENCA_LITORAL,
    ]
    apagar_arquivos_criados_antes(arquivos_apagar)

    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Iniciando o processamento da tabela de preços...")
    etapas = (
        # (MAPA_TABELA_PRECO_NOVO_LITORAL, XLS_PRECO_NOVO_LITORAL, SQL_TB_LITORAL, XLS_PRECO_VIGENTE_LITORAL, XLS_DIFERENCA_LITORAL,),
        # (MAPA_TABELA_PRECO_NOVO_ST, XLS_PRECO_NOVO_ST, SQL_TB_ST01, XLS_PRECO_VIGENTE_ST, XLS_DIFERENCA_ST,),
        (MAPA_TABELA_PRECO_NOVO_SP2, XLS_PRECO_NOVO_SP2, SQL_TB_SP02, XLS_PRECO_VIGENTE_SP2, XLS_DIFERENCA_SP2,),
        # (MAPA_TABELA_PRECO_NOVO_SP3, XLS_PRECO_NOVO_SP3, SQL_TB_SP03, XLS_PRECO_VIGENTE_SP3, XLS_DIFERENCA_SP3,),
    )
    result = encontrar_diferencas_tabelas_precos(etapas, xls_preco_novo)

    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Concluída análise de preços novos")

    return result
