import pandas as pd
from datetime import datetime, date
from os import path, getenv
#
from app.controllers.loggers import logger
from app.controllers.util import apagar_arquivos_criados_antes
from constants import MAPA_TABELA_CUSTOS_SP, CSV_CUSTOS


def criar_csv_custos(xls_filename: str):
    for tab in MAPA_TABELA_CUSTOS_SP:
        xlsx_custo = xls_filename
        
        if path.exists(xlsx_custo):
            sheet_custo = tab['nome_sheet']
            nome_colunas = tab['nome_colunas'],
            linhas_pular = tab['linhas_pular']
            colunas_ler = tab['colunas_ler']
            linhas_ler = tab['linhas_ler']

            try:
                df = pd.read_excel(
                    xlsx_custo,
                    sheet_name = sheet_custo,           # Nome da Sheet a ler os dados
                    skiprows = linhas_pular,            # Pula as linhas especificadas
                    usecols = colunas_ler,              # Ou use nomes das colunas: ['Coluna1', 'Coluna2']
                    nrows = linhas_ler,                 # Lê apenas as próximas linhas especificadas
                )
                
                df.columns = nome_colunas[0]

                df = df.sort_values('Codigo')

                df = df[ ['Codigo', 'Custo'] ]
                df.dropna(how='all', axis=0, inplace=True)  # apaga linhas em branco
                df = df[ df['Custo'] > 0 ]
            
                df['Custo'] = df['Custo'].round(2)
                
                df.insert(0, "Data", date.today().strftime('%d/%m/%Y'))

                df = df.astype(
                    {
                        'Codigo': int,
                        'Custo': float,
                    }
                )
                
                if 'df_total' in locals():
                    df_total = pd.concat([df_total, df], ignore_index=True)
                else:
                    df_total = df


            except Exception as e:
                logger.error(f'❌ Erro ao criar CSV de custos. {e.args}')
                return pd.DataFrame()
        
        else:
            logger.error(f'❌ Arquivo de composição do custo nao encontrado: {xlsx_custo}')
            return pd.DataFrame()

    if ('df_total' in locals()) and not df_total.empty:
        logger.info(f'Número de linhas do CSV: {len(df_total)}')
        df_total.to_csv(CSV_CUSTOS, sep=',', index=False)
        logger.info(f'💲 CSV de custos gravados com sucesso: {CSV_CUSTOS}')
        return df_total
    else:
        logger.error(f'❌ CSV de custos vazio')
        return pd.DataFrame()


def lancar_csv_custos():
    logger.info(f'Iniciando sistema')

    logger.info(f'Apagando arquivos de resultado criados antes...')
    arquivos_apagar = [CSV_CUSTOS]
    apagar_arquivos_criados_antes(arquivos_apagar)

    logger.info(f'Iniciando criação de csv de custos para SP...')
    result = criar_csv_custos(csv_filename=CSV_CUSTOS)

    logger.info(f'Processamento concluído')

    return result
