# ⭐️ SleekCode Reviews Bot (@sleekcodereviews_bot)

Телеграм-бот для приёма отзывов клиентов на **Python 3** с использованием **aiogram 3.x** и асинхронной базы данных **SQLite** (`aiosqlite`).

---

## 🚀 Особенности и возможности

1. **Поддержка любого текста и премиум эмодзи**:
   - При написании отзыва сохраняются любые кастомные/премиум эмодзи пользователя и исходное форматирование.
2. **Интерактивная оценка**:
   - После отправки текста бот предлагает удобную клавиатуру снизу с выбором рейтинга от 1 до 5 звёзд (`⭐ 1` ... `⭐⭐⭐⭐⭐ 5`).
3. **Точный формат уведомления админа**:
   ```text
   Новый отзыв!

   (сообщение пользователя)
   (сколько звёзд в emoji)

   @(юз того кто написал отзыв)
   ```
4. **Многофункциональная админ-панель** (`/admin`):
   - 📊 **Детальная статистика**: общее число пользователей, отзывов, средний балл, распределение по оценкам (1-5) с прогресс-баром, количество отзывов за сегодня.
   - 💬 **Прямой ответ пользователю**: отправка ответа на отзыв прямо в Telegram через бота с цитированием отзыва клиента.
   - 📝 **Модерация и просмотр отзывов**: удобная пагинация, фильтрация по оценкам (все / 5★ / 4★ / 1-3★), удаление нежелательных отзывов.
   - 📢 **Публикация в публичный канал**: отправка проверенных отзывов в ваш канал с красивым оформлением в один клик.
   - 📢 **Массовая рассылка**: рассылка текста, картинок, видео, стикеров и эмодзи всем пользователям бота с предпросмотром и защитой от флуда.
   - 🚫 **Управление чёрным списком**: бан/разбан спамеров и неадекватных пользователей по ID или кнопкой из карточки отзыва.
   - 📥 **Экспорт в CSV**: выгрузка всей базы отзывов в файл `.csv` с кодировкой UTF-8-BOM (открывается сразу в Excel без проблем со шрифтами).
5. 🛡️ **Rate Limiting & Throttling Middleware**:
   - Автоматическая защита от спам-кликов по инлайн-кнопкам и флуда текстовыми сообщениями.
   - При частых кликах пользователь получает интерактивный alert: *«⏳ Слишком много нажатий! Пожалуйста, не спешите»*.
   - Администраторы бота обладают иммунитетом от ограничений.
6. 🚨 **Sentry / GlitchTip + Мгновенные алерты админам в Telegram**:
   - Автоматический сбор необработанных исключений и багов в Sentry / GlitchTip.
   - Мгновенная отправка красивого алерта в личные сообщения всем администраторам с типом ошибки, данными пользователя, контекстом и блоком `<pre><code>traceback</code></pre>`.
7. 🌐 **Поддержка Webhook (aiohttp + Nginx / Caddy SSL)**:
   - Возможность переключения между `BOT_MODE=polling` (для локальной разработки) и `BOT_MODE=webhook` (для продакшена с минимальной задержкой).
   - Встроенный healthcheck эндпоинт `/health` для систем мониторинга и Docker.
   - Проверка безопасности запросов через `X-Telegram-Bot-Api-Secret-Token`.

---

## 🛠️ Установка и запуск

### 1. Клонирование / переход в папку проекта
```bash
cd "@sleekcodereviews_bot - отзывы сликкод"
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл `.env` в корневой папке (на основе `.env.example`):
```env
# Токен бота, полученный у @BotFather
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# ID администраторов через запятую (например, один ID или несколько)
ADMIN_IDS=123456789,987654321

# (Необязательно) Username или ID канала для публикации отзывов
REVIEWS_CHANNEL_ID=@sleekcode_reviews

# Режим запуска: polling или webhook
BOT_MODE=polling

# Настройки для режима webhook (при BOT_MODE=webhook)
WEBHOOK_URL=https://reviews.yourdomain.com
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET_TOKEN=super_secret_token_12345
WEBAPP_HOST=0.0.0.0
WEBAPP_PORT=8080

# Интервал троттлинга в секундах
RATE_LIMIT_SECONDS=0.7

# (Необязательно) Sentry / GlitchTip DSN
SENTRY_DSN=
```

### 4. Запуск бота

**В режиме Polling (по умолчанию):**
```bash
python bot.py
```

**В режиме Webhook:**
1. Укажите в `.env` параметр `BOT_MODE=webhook`, а также ваш домен `WEBHOOK_URL=https://reviews.yourdomain.com`.
2. Запустите бота:
```bash
python bot.py
```

---

## 🌐 Настройка Webhook с SSL (Nginx / Caddy)

### Вариант А: Настройка через Caddy (автоматический бесплатный SSL Let's Encrypt)
Caddyfile:
```caddy
reviews.yourdomain.com {
    reverse_proxy 127.0.0.1:8080
}
```

### Вариант Б: Настройка через Nginx + Certbot
Файл конфигурации `/etc/nginx/sites-available/bot`:
```nginx
server {
    server_name reviews.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/reviews.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/reviews.yourdomain.com/privkey.pem;
}
```

Проверить доступность сервера можно в браузере или через curl:
```bash
curl https://reviews.yourdomain.com/health
# Ответ: {"status": "ok", "service": "sleekcode-reviews-bot", "mode": "webhook"}
```

---

## 📁 Структура проекта

```
.
├── .env.example              # Пример файла переменных окружения со всеми настройками
├── .gitignore                # Игнорируемые файлы Git
├── requirements.txt          # Зависимости Python (aiogram, aiosqlite, sentry-sdk и др.)
├── bot.py                    # Главный файл запуска (поддержка Polling и Webhook aiohttp)
├── config.py                 # Загрузка и валидация конфигурации из .env
├── utils.py                  # Утилиты форматирования, звёзд и парсинга
├── database/
│   ├── __init__.py
│   └── db.py                 # Асинхронные методы работы с SQLite
├── handlers/
│   ├── __init__.py
│   ├── user.py               # Обработчики для пользователей (/start, /review, оценка)
│   ├── admin.py              # Админ-панель, модерация, статистика, рассылка
│   └── errors.py             # Глобальный перехват ошибок, Sentry и Telegram-алерты админам
├── middlewares/
│   ├── __init__.py
│   └── throttling.py         # Rate Limiting & Throttling middleware против флуда и спама
├── keyboards/
│   ├── __init__.py
│   ├── user_kb.py            # Клавиатуры пользователя (оценка 1-5, отмена)
│   └── admin_kb.py           # Инлайн-клавиатуры админ-панели
└── states/
    ├── __init__.py
    ├── user_states.py        # FSM состояния пользователя
    └── admin_states.py       # FSM состояния администратора
```
