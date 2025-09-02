import logging
from logging.handlers import TimedRotatingFileHandler
import sys


# Nome do arquivo de log
LOG_FILE = "logs.log"
web_log = []

# Criar logger principal
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ===== Handler para Console =====
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# ===== Handler para Arquivo Rotativo Diário =====
file_handler = TimedRotatingFileHandler(
    LOG_FILE,             # Nome do arquivo base
    when="midnight",      # Roda todo dia à meia-noite
    interval=1,           # Intervalo de rotação (1 dia)
    backupCount=7,        # Quantos dias manter
    encoding="utf-8"
)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# ===== Handler para Lista dos logs E exibicao destas na pagina web =====
class ListHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        log_entry = self.format(record)     # aplica o formato configurado
        self.log_list.append(log_entry)

log_messages = []                           # lista que vai receber os logs
list_handler = ListHandler(log_messages)    # cria o handler que salva na lista
list_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(list_handler)
logger.setLevel(logging.INFO)


# ===== Teste de log =====
# logger.info("Monitoramento iniciado 🚀")
# logger.warning("Isso é um aviso")
# logger.error("Isso é um erro")
