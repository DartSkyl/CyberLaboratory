import os
from dotenv import load_dotenv, find_dotenv
import logging

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

MODEL_URI = os.getenv('model_uri')
FOLDER_ID = os.getenv('folder_id')
TG_TOKEN = os.getenv('TG_TOKEN')
MAX_TOKENS = int(os.getenv('max_tokens'))
TOKEN_REFRESH = int(os.getenv('token_refresh'))

logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format="%(asctime)s %(levelname)s %(message)s"
)
logging.getLogger().setLevel(logging.INFO)
