import pandas as pd
from datetime import datetime, date
from os import path


def carregar_tabela(
        xlsx_preco_novo:str,
        xlsx_sheet: str,
        nome_colunas,
        linhas_pular: int,
        colunas_ler:str,
        linhas_ler: int
        ):
    try:
        df = pd.read_excel(
            xlsx_preco_novo,
            sheet_name = xlsx_sheet,            # Nome da Sheet a ler os dados
            skiprows = linhas_pular,            # Pula as linhas especificadas
            usecols = colunas_ler,              # Ou use nomes das colunas: ['Coluna1', 'Coluna2']
            nrows = linhas_ler,                 # Lê apenas as próximas linhas especificadas
        )
        
        # Na tabela de Sertaozinho a Qtde nao é usada, entao, na planilha essa informacao nao vem.
        # Para nao causar erro ou ter q criar uma nova funcao, decidiu-se criar a coluna Qtde na mao!
        if len(df.columns) < len(nome_colunas[0]):
            df['Qtde'] = 1

        df.columns = nome_colunas[0]

        # df = df.drop(['del01', 'del02', 'del03'], axis=1)         # apagar coluna pelo nome
        df = df[['Codigo', 'Produtos', 'PesoCaixa', 'R$', 'Qtde']]  # extrair apenas as colunas q interessa

        df = df.dropna(subset=['Codigo'])
        df = df[ ( (df['Qtde'] > 0) ) ]     # nao esqueca dos parenteses
        # df = df[ ( df['Codigo'].notna() & (df['Codigo'].astype(str).str.strip() != '') ) ]  # Codigo nao vazio E se apagar todos os espacos em branco, nao pode ser vazio

        # df['R$'] = pd.to_numeric(df['R$'], errors='coerce')
        df = df[ ( (df['R$'] != 0) ) ]     # nao esqueca dos parenteses


        df.dropna(subset=['Codigo', 'Produtos', 'R$'], axis=0, inplace=True)    # apaga linhas q o codigo ou produtos esteja em branco 
        # df.dropna(how='all', axis=1, inplace=True)                            # apaga colunas em branco

        for col in ['PesoCaixa']:                                               # deixando somente numero nas colunas específicas
            df[col] = df[col].astype(str).str.extract(r'(\d+(?:[.,]\d+)?)')[0]  # o ZERO final é necessario pq o EXTRACT retorna um dataframe
            df[col] = df[col].str.replace(',', '.').astype(float)

        df = df.astype(
            {
                'Codigo': int,
                'Produtos': str,
                'PesoCaixa': float,
                'R$': float,
                'Qtde': float,
            }
        )

        for col in ['R$']:                        
            df[col] = df[col].round(2)      # arredondar em duas casas decimais

        df = df.sort_values(by='Codigo', ascending=True)            # Ordena pela coluna
 
        return df
    
    except Exception as e:
        print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ Não foi possível carregar a tabela de preços. {e.args}")
        raise 


def montar_tabela_unica(filename: str, mapa_precos_novos:list, nome_xlsx_destino:str):
    """Montar uma tabela única com os dados de várias tabelas."""   

    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] Montando tabela unica de precos...")

    # Carrega as tabelas
    for tab in mapa_precos_novos:
        xlsx_preco_novo = filename
        
        if path.exists(xlsx_preco_novo):
            sheet_preco_novo = tab['nome_sheet']
            nome_colunas = tab['nome_colunas'],
            linhas_pular = tab['linhas_pular']
            colunas_ler = tab['colunas_ler']
            linhas_ler = tab['linhas_ler']
            
            df = carregar_tabela(
                xlsx_preco_novo=xlsx_preco_novo,
                xlsx_sheet=sheet_preco_novo,
                nome_colunas=nome_colunas,
                linhas_pular=linhas_pular,
                colunas_ler=colunas_ler,
                linhas_ler=linhas_ler
            )

        else:
            print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] ❌ Arquivo de precos novos nao encontrado: {xlsx_preco_novo}")
            df = pd.DataFrame()

        if 'df_todos' in locals():
            df_todos = pd.concat([df_todos, df], ignore_index=True)
        else:
            df_todos = df
    
    print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 📃 Concluído tabela unica de precos novos.")

    if not df_todos.empty:
        # Salva o DataFrame em um arquivo Excel para comferencia manual
        df_todos.to_excel(nome_xlsx_destino, index=False)
        print(f"[ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ] 📂 Preco novo gravado em: {nome_xlsx_destino}")

    return df_todos
    