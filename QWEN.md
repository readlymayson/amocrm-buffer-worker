# amoCRM Buffer Worker — QWEN Context

## Project Overview

Автономный Python-скрипт для перемещения сделок из этапа **«Буфер»** в целевой этап в amoCRM. Запускается по расписанию через Cron.

**Основной workflow:**
1. Проверить/обновить OAuth2 Access Token (`auth.py`)
2. Получить сделки из этапа «Буфер» (GET `/api/v4/leads`, сортировка по дате asc)
3. Если буфер пуст — завершить
4. Переместить найденные сделки в целевой этап (PATCH `/api/v4/leads`)

**Технологии:**
- Python 3 (no framework, standalone scripts)
- `requests` — единственная зависимость
- amoCRM API v4 (REST, JSON)
- OAuth2 (authorization code grant + refresh token)

## Architecture

```
worker.py                 # Точка входа (Cron) — получает токен, читает сделки, перемещает
├── auth.py               # OAuth2: загрузка/сохранение токенов, refresh
├── config.py             # Константы: ID интеграции, ID этапов, лимит, домены
├── setup_auth.py         # Первичная авторизация (однократный запуск вручную)
├── tokens.json           # Хранилище токенов (gitignored, создаётся setup_auth.py)
└── amocrm-auth.html      # Статическая страница-заглушка для Redirect URL
```

### Module Roles

- **`config.py`** — все настройки в одном месте: клиентские ID/секреты, pipeline_id, status_id, лимит выборки, домены OAuth и API.
- **`auth.py`** — управление жизненным циклом токенов. Загружает из `tokens.json`, проверяет expiry (с 5-минутным запасом), автоматически обновляет через refresh token и сохраняет новую пару.
- **`worker.py`** — основная бизнес-логика. Использует `auth.get_valid_token()`, затем два запроса к API: GET (выборка) → PATCH (перемещение). При ошибках завершается с `sys.exit(1)`.
- **`setup_auth.py`** — интерактивный скрипт. Генерирует ссылку для OAuth, принимает code из адресной строки, обменивает на токены. Запускается однократно вручную.

## Key Conventions

### Code Style
- Python 3 typing: используются нативные типы (`dict | None`, `list[dict]`, `list[int]`, `bool`, `str`).
- Docstrings: reStructuredText-стиль с секциями `Args:` и `Returns:`.
- Имена: `snake_case` для функций и переменных, `UPPER_CASE` для констант.
- Вывод в stdout через `print()` с префиксом `[module]` (например `[worker]`, `[auth]`, `[setup]`).

### Error Handling
- Никаких `try/except` в верхнем уровне — коды ответов проверяются через `response.status_code`.
- При ошибке API — вывести код и тело ответа, вернуть `None` или `False`.
- `worker.py` завершается `sys.exit(1)` при фатальных ошибках (нет токена, ошибка API).

### Auth Flow Details
- Токены хранятся в `tokens.json` с полем `expires_at` (абсолютный Unix timestamp).
- `auth.py` проверяет запас в 300 секунд (5 минут) до фактического истечения.
- Refresh token используется для автоматического продления — `worker.py` не требует ручного вмешательства.

## Building and Running

### Установка зависимостей
```bash
pip install requests
```

### Первичная авторизация (однократно)
```bash
python3 setup_auth.py
# → открыть ссылку в браузере, авторизоваться, вставить code из URL
```

### Ручной запуск (тестирование)
```bash
python3 worker.py
```

### Cron
```bash
# каждые 30 минут
*/30 * * * * cd /path/to/project && python3 worker.py >> worker.log 2>&1
```

## Testing

**Проект не содержит тестов.** При добавлении тестов:
- Использовать `pytest` (де-факто стандарт для Python-проектов без явного фреймворка).
- Мокать HTTP-запросы (`responses` или `pytest-httpserver`).
- Размещать тесты в `tests/`.

## Security

- `tokens.json` содержит Access Token и Refresh Token — **не коммитить**.
- Добавлен в `.gitignore`.
- Доступ к папке рекомендуется ограничить через chmod.
- `config.py` содержит клиентский секрет — не публиковать репозиторий публично.

## Files at a Glance

| File | Purpose |
|---|---|
| `worker.py` | Точка входа по Cron |
| `auth.py` | OAuth2 авторизация с автообновлением |
| `config.py` | Настройки интеграции и этапов |
| `setup_auth.py` | Первичная OAuth2 авторизация |
| `tokens.json` | Хранилище токенов (автосоздаётся, gitignored) |
| `amocrm-auth.html` | Страница для Redirect URI |
| `README.md` | Документация |
| `QWEN.md` | **Этот файл — контекст для Qwen Code** |
