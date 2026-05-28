"""
Модуль авторизации OAuth2 для amoCRM.
Поддерживает:
- Загрузку токенов из файла
- Автоматическое обновление Access Token через Refresh Token
- Сохранение новой пары токенов обратно в файл
"""

import json
import time
import requests
import config

TOKEN_URL = f"https://{config.API_DOMAIN}/oauth2/access_token"


def load_tokens() -> dict | None:
    """Загружает токены из JSON-файла."""
    try:
        with open(config.TOKENS_FILE, "r") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_tokens(tokens: dict) -> None:
    """Сохраняет токены в JSON-файл."""
    with open(config.TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    print(f"[auth] Токены сохранены в {config.TOKENS_FILE}")


def refresh_access_token(refresh_token: str) -> dict | None:
    """Обновляет Access Token через Refresh Token.

    Args:
        refresh_token: Текущий Refresh Token.

    Returns:
        Новая пара токенов или None при ошибке.
    """
    payload = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": config.REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, json=payload)
    if response.status_code != 200:
        print(f"[auth] Ошибка обновления токена: {response.status_code} {response.text}")
        return None

    tokens = response.json()
    # amoCRM возвращает expires_in в секундах; сохраняем абсолютное время смерти
    tokens["expires_at"] = int(time.time()) + tokens.get("expires_in", 86400)
    save_tokens(tokens)
    return tokens


def get_valid_token() -> str | None:
    """Возвращает валидный Access Token, обновляя его при необходимости.

    Returns:
        Access Token (строка) или None в случае ошибки.
    """
    tokens = load_tokens()
    if not tokens:
        print("[auth] Файл токенов не найден. Запустите setup_auth.py для первичной авторизации.")
        return None

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_at = tokens.get("expires_at", 0)

    # Если токен ещё жив (с запасом в 5 минут)
    if access_token and int(time.time()) < expires_at - 300:
        return access_token

    if not refresh_token:
        print("[auth] Refresh Token отсутствует. Запустите setup_auth.py заново.")
        return None

    print("[auth] Access Token истёк, обновляем...")
    new_tokens = refresh_access_token(refresh_token)
    if new_tokens:
        return new_tokens.get("access_token")
    return None
