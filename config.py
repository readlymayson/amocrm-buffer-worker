"""
Настройки скрипта для работы с amoCRM.
Перед запуском заполните все обязательные поля.

Секреты загружаются из .env файла (см. .env.example).
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# --- Данные интеграции (из AmoMarket -> Создать интеграцию) ---
CLIENT_ID = os.getenv('AMOCRM_CLIENT_ID', '4e675dd4-c21b-42cd-a524-32c52eaf2a87')  # Integration ID (Client ID)
CLIENT_SECRET = os.getenv('AMOCRM_CLIENT_SECRET')  # Secret key — ТОЛЬКО из .env!
REDIRECT_URI = os.getenv('AMOCRM_REDIRECT_URI', 'https://efrolov-dev.ru/amocrm-auth')  # Redirect URL

# ── Проверка наличия критичного секрета ──
if not CLIENT_SECRET:
    print("=" * 60)
    print("❌ AMOCRM_CLIENT_SECRET не задан!")
    print()
    print("Создайте файл .env в директории amocrm-buffer-worker")
    print("на основе .env.example и укажите ваш Secret key:")
    print()
    print("    cp .env.example .env")
    print("    # отредактируйте .env, вставьте свой CLIENT_SECRET")
    print()
    print("Без Client Secret авторизация в amoCRM невозможна.")
    print("=" * 60)
    sys.exit(1)

# --- ID воронки и этапов ---
PIPELINE_ID = 10591630         # Воронка «Реактивация»
BUFFER_STATUS_ID = 83527594    # Этап «В выборке» (откуда забираем)
TARGET_STATUS_ID = 83527598    # Этап «Реактивация» (куда перемещаем)

# --- Параметры выборки ---
LIMIT = 1               # Сколько сделок обрабатывать за один запуск

# --- Временное окно графика работы (МСК, UTC+3) ---
MSK_OFFSET_HOURS = 3
WORK_START_HOUR = 10    # Начало рабочего окна (10:00 МСК)
WORK_END_HOUR = 20      # Конец рабочего окна (20:00 МСК)

# --- Файл для хранения токенов ---
TOKENS_FILE = "tokens.json"

# --- Домены amoCRM ---
OAUTH_DOMAIN = "www.amocrm.ru"           # Домен для страницы авторизации (OAuth)
API_DOMAIN = "sweetshot63.amocrm.ru"     # Поддомен для API и обмена токена
