import os
from dotenv import load_dotenv, find_dotenv
import logging

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

YC_API_KEY_ID = os.getenv('YC_API_KEY_ID')
YC_API_KEY = os.getenv('YC_API_KEY')
YC_IAM_TOKEN = os.getenv('YC_IAM_TOKEN')
MODEL_URI = os.getenv('model_uri')
FOLDER_ID = os.getenv('folder_id')
TG_TOKEN = os.getenv('TG_TOKEN')

# logging.basicConfig(
#     filename='bot.log',
#     filemode='a',
#     format="%(asctime)s %(levelname)s %(message)s"
# )
# logging.getLogger().setLevel(logging.ERROR)
