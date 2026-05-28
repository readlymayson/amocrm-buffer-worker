"""
Скрипт первичной авторизации в amoCRM (получение Access Token + Refresh Token).

Использование:
  1. Заполните CLIENT_ID, CLIENT_SECRET и REDIRECT_URI в config.py.
  2. Запустите скрипт: python3 setup_auth.py
  3. Откройте ссылку в браузере, авторизуйтесь в amoCRM.
  4. Браузер перенаправит на Redirect URL с параметром ?code=...
  5. Скопируйте этот код из адресной строки и вставьте в консоль.
  6. Токены будут сохранены в tokens.json.
"""

import json
import time

import requests
import config

AUTH_URL = f"https://{config.API_DOMAIN}/oauth2/access_token"


def exchange_code(code: str) -> dict | None:
    """Обменивает авторизационный код на пару токенов."""
    payload = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
    }

    response = requests.post(AUTH_URL, json=payload)
    if response.status_code != 200:
        print(f"[setup] Ошибка обмена кода: {response.status_code} {response.text}")
        return None

    tokens = response.json()
    tokens["expires_at"] = int(time.time()) + tokens.get("expires_in", 86400)

    with open(config.TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

    print(f"[setup] ✅ Токены сохранены в {config.TOKENS_FILE}")
    print(f"[setup] Access Token:    {tokens['access_token'][:40]}...")
    print(f"[setup] Refresh Token:   {tokens['refresh_token'][:40]}...")
    print(f"[setup] Истекает через:  {tokens.get('expires_in', '?')} сек")
    return tokens


def main():
    print("=" * 50)
    print("Первичная авторизация в amoCRM")
    print("=" * 50)

    if not config.CLIENT_ID or not config.CLIENT_SECRET or not config.REDIRECT_URI:
        print("[setup] ❌ Заполните CLIENT_ID, CLIENT_SECRET и REDIRECT_URI в config.py")
        return

    auth_link = (
        f"https://{config.OAUTH_DOMAIN}/oauth?client_id={config.CLIENT_ID}"
        f"&redirect_uri={config.REDIRECT_URI}"
    )
    print(f"\n[setup] Перейдите по ссылке и авторизуйтесь:\n{auth_link}\n")

    code = input("[setup] Вставьте код из адресной строки (параметр code): ").strip()

    if not code:
        print("[setup] ❌ Код не получен. Завершение.")
        return

    exchange_code(code)


if __name__ == "__main__":
    main()
