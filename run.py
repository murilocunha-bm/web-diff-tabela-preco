#!.venv/bin/python3
# -*- coding: utf-8 -*-

from os import path, abort
if not path.exists('./.env'):
    print(f'\nArquivo .env não encontrado. Por favor, verifique o arquivo de parâmetros obrigatórios.')
    abort()

from dotenv import load_dotenv
load_dotenv()
#
from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run()
