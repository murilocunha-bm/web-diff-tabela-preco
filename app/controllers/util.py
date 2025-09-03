from os import path, remove
from app.controllers.loggers import logger


def apagar_arquivos_criados_antes(arquivos_apagar):
    for arquivo in arquivos_apagar:
        if path.isfile(arquivo):
            remove(arquivo)
            logger.info(f'🗑 Arquivo {arquivo} excluído com sucesso')
        else:
            logger.info(f'❌ Arquivo {arquivo} não encontrado')
