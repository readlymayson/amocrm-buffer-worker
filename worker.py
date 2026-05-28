"""
Основной скрипт перемещения сделок из этапа «Буфер» в целевой этап.

Логика:
  1. Проверить/обновить Access Token.
  2. Запросить порцию сделок из этапа «Буфер» (самые старые первыми).
  3. Если сделок нет — завершить работу.
  4. Переместить найденные сделки в целевой этап одним PATCH-запросом.

Запускается по Cron. Пример crontab (каждые 30 минут):
  */30 * * * * cd /path/to/project && python3 worker.py >> worker.log 2>&1
"""

import sys
import requests
import config
from auth import get_valid_token

API_BASE = f"https://{config.API_DOMAIN}/api/v4"


def get_leads_from_buffer(token: str) -> list[dict] | None:
    """GET /api/v4/leads — получает сделки из этапа «Буфер».

    Args:
        token: Валидный Access Token.

    Returns:
        Список сделок или None при ошибке.
    """
    url = f"{API_BASE}/leads"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "filter[statuses][0][pipeline_id]": config.PIPELINE_ID,
        "filter[statuses][0][status_id]": config.BUFFER_STATUS_ID,
        "sort[created_at]": "asc",
        "limit": config.LIMIT,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"[worker] Ошибка GET /leads: {response.status_code} {response.text}")
        return None

    data = response.json()
    return data.get("_embedded", {}).get("leads", [])


def move_leads_to_target(token: str, lead_ids: list[int]) -> bool:
    """PATCH /api/v4/leads — перемещает указанные сделки в целевой этап.

    Args:
        token: Валидный Access Token.
        lead_ids: Список ID сделок для перемещения.

    Returns:
        True при успехе, False при ошибке.
    """
    url = f"{API_BASE}/leads"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = [
        {
            "id": lid,
            "status_id": config.TARGET_STATUS_ID,
        }
        for lid in lead_ids
    ]

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"[worker] Ошибка PATCH /leads: {response.status_code} {response.text}")
        return False

    updated = response.json().get("_embedded", {}).get("leads", [])
    print(f"[worker] Успешно перемещено {len(updated)} сделок: ID {[l['id'] for l in updated]}")
    return True


def main():
    print("=" * 50)
    print("[worker] Запуск обработчика буфера amoCRM")
    print(f"[worker] Лимит: {config.LIMIT} сделок за запуск")

    # Шаг 1. Авторизация
    token = get_valid_token()
    if not token:
        print("[worker] Нет валидного токена. Завершение.")
        sys.exit(1)

    # Шаг 2. Запрос сделок из буфера
    leads = get_leads_from_buffer(token)
    if leads is None:
        print("[worker] Ошибка при получении сделок. Завершение.")
        sys.exit(1)

    if not leads:
        print("[worker] Буфер пуст. Завершение.")
        return

    lead_ids = [lead["id"] for lead in leads]
    print(f"[worker] Найдено {len(leads)} сделок в буфере: ID {lead_ids}")

    # Шаг 3. Перемещение
    success = move_leads_to_target(token, lead_ids)
    if not success:
        print("[worker] Ошибка при перемещении сделок.")
        sys.exit(1)

    print("[worker] Завершено успешно.")


if __name__ == "__main__":
    main()
