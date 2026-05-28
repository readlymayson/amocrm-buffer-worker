"""
Настройки скрипта для работы с amoCRM.
Перед запуском заполните все обязательные поля.
"""

# --- Данные интеграции (из AmoMarket -> Создать интеграцию) ---
CLIENT_ID = "4e675dd4-c21b-42cd-a524-32c52eaf2a87"          # Integration ID (Client ID)
CLIENT_SECRET = "AXUOXwoawEV1Yowq1wBtL6XxxfBWZ7kXk4Ohd3j3aU3PoZvvXqKdODh4PDyV50A4"      # Secret key
REDIRECT_URI = "https://efrolov-dev.ru/amocrm-auth"  # Redirect URL, указанный при регистрации

# --- ID воронки и этапов ---
PIPELINE_ID = 10591630         # Воронка «Реактивация»
BUFFER_STATUS_ID = 83527594    # Этап «В выборке» (откуда забираем)
TARGET_STATUS_ID = 83527598    # Этап «Реактивация» (куда перемещаем)

# --- Параметры выборки ---
LIMIT = 10              # Сколько сделок обрабатывать за один запуск (10 или 50)

# --- Файл для хранения токенов ---
TOKENS_FILE = "tokens.json"

# --- Домены amoCRM ---
OAUTH_DOMAIN = "www.amocrm.ru"           # Домен для страницы авторизации (OAuth)
API_DOMAIN = "sweetshot63.amocrm.ru"     # Поддомен для API и обмена токена
