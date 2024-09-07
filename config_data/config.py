import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены, т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('admin_panel', "Войти в админку"),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_TO_PYTHON = os.path.normpath(os.path.join(BASE_DIR, "venv/Scripts/python.exe"))
STATIC_PATH = os.path.normpath(os.path.join(BASE_DIR, "static"))
ADMIN_ID = os.getenv('ADMIN_ID')
ALLOWED_USERS = [int(ADMIN_ID),]

API_URL = os.getenv("API_URL")
MEDIA_URL = os.getenv("MEDIA_URL")
API_TOKEN_INSTANCE = os.getenv("API_TOKEN_INSTANCE")
ID_INSTANCE = os.getenv("ID_INSTANCE")
ADMIN_ID_WHATSAPP = os.getenv("ADMIN_ID_WHATSAPP")
