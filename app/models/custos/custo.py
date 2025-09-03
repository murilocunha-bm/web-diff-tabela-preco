import pandas as pd
from datetime import datetime, date
from os import path


def criar_csv_custos(mapa_custos: list, csv_filename: str):
    for tab in mapa_custos:
        if path.exists(tab['nome_xlsx']):
            xlsx_custo = tab['nome_xlsx']
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
                
                df.insert(0, "data", date.today().strftime('%d/%m/%Y'))

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
                print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ Erro ao criar CSV de custos. {e.args}")
                raise
        
        else:
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ Arquivo de composição do custo nao encontrado: {tab['nome_xlsx']}")

    if ('df_total' in locals()) and not df_total.empty:
        df_total.to_csv(csv_filename, sep=',', index=False)
        print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 💲 CSV de custos gravados com sucesso: {csv_filename}")
    else:
        print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ CSV de custos vazio")