from pathlib import Path
from urllib.parse import urljoin

from dotenv import load_dotenv
from envparse import env

load_dotenv(env('DOTENV_FILE', default=None))


BASE_DIR = Path(__file__).resolve().parent.parent

BOT_TOKEN = env('BOT_TOKEN')

BACKEND_API_URL = env('BACKEND_API_URL', default='https://droppy-backend.vercel.app/')
TELEGRAM_AUTH_TOKEN = env('TELEGRAM_AUTH_TOKEN')
AUTH_REQUEST_RESPONSE_METHOD = env('AUTH_REQUEST_RESPONSE_METHOD', default='telegram_auth_request_response')
AUTH_GET_URL_METHOD = env('AUTH_GET_URL_METHOD', default='telegram_auth_get_url')

TELEGRAM_AUTH_REQUEST_RESPONSE_URL = urljoin(BACKEND_API_URL, AUTH_REQUEST_RESPONSE_METHOD)
TELEGRAM_AUTH_GET_URL_URL = urljoin(BACKEND_API_URL, AUTH_GET_URL_METHOD)
