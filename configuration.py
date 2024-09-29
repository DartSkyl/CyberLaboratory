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
ADMIN_ID = int(os.getenv('admin_id'))

DB_INFO = (
    os.getenv("db_user"),
    os.getenv("db_pass"),
    os.getenv("db_name"),
    os.getenv("db_host"))

PG_URI = f"postgresql+psycopg2://{DB_INFO[0]}:{DB_INFO[1]}@{DB_INFO[3]}/{DB_INFO[2]}"

logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format="%(asctime)s %(levelname)s %(message)s"
)
logging.getLogger().setLevel(logging.INFO)
