import requests
from adaptadorHTTP import MongoLoggerAdapter

client_banco = requests.Session()

mongo_logger = MongoLoggerAdapter()
client_banco.mount("http://", mongo_logger)
client_banco.mount("https://", mongo_logger)