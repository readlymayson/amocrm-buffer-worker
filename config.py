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
CLIENT_ID = os.getenv('AMOCRM_CLIENT_ID')  # Integration ID (Client ID) — из .env!
CLIENT_SECRET = os.getenv('AMOCRM_CLIENT_SECRET')  # Secret key — ТОЛЬКО из .env!
REDIRECT_URI = os.getenv('AMOCRM_REDIRECT_URI')  # Redirect URL — из .env!

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
PIPELINE_ID = 0                 # ID воронки — замените на свой
BUFFER_STATUS_ID = 0            # ID этапа «Буфер» — замените на свой
TARGET_STATUS_ID = 0            # ID целевого этапа — замените на свой

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
API_DOMAIN = "your-subdomain.amocrm.ru"  # Поддомен для API — замените на свой
