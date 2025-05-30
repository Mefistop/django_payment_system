# Payments System - Django Interview

## Описание

Этот проект представляет собой backend-сервис для обработки webhook-ов от банка и 
управления балансами организаций. Сервис принимает входящие платежи, проверяет их на дубликаты, 
обновляет балансы организаций и предоставляет API для получения текущего баланса по ИНН.

## Технологии

- Python 3.12
- Django 5.2.1
- djangorestframework 3.16.0

## Функциональность 

1. **POST /api/webhook/bank/**:
   - Принимает данные о платеже в формате JSON.
   - Проверяет уникальность операции по `operation_id`.
   - Обновляет баланс организации по ИНН.
   - Логирует изменения баланса.

2. **GET /api/organizations/<inn>/balance/**:
   - Возвращает текущий баланс организации по её ИНН.
         
## Структура проекта 
```text
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Dockerfile для сборки образа
├── .env                        # Переменные окружения
├── payment_system              # Основной каталог проекта
│   ├── create_superuser.py     # Скрипт для создания суперпользователя
│   ├── db.sqlite3              # Локальная SQLite база данных (опционально)
│   ├── entrypoint.sh           # Скрипт для запуска приложения
│   ├── manage.py               # Утилита Django
│   ├── payments                # Приложение для обработки платежей
│   │   ├── admin.py            # Регистрация моделей в админке
│   │   ├── apps.py             # Конфигурация приложения
│   │   ├── models.py           # Модели Django
│   │   ├── serializers.py      # Сериализаторы DRF
│   │   ├── tests.py            # Тесты
│   │   ├── urls.py             # Маршруты URL для приложения
│   │   └── views.py            # Представления (views)
│   └── payment_system          # Настройки проекта
│       ├── settings.py         # Настройки Django
│       ├── urls.py             # Главный маршрутизатор URL-адресов
│       └── wsgi.py             # Конфигурация WSGI
├── README.MD                   # Документация проекта
└── requirements.txt            # Зависимости проекта
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Mefistop/django_payment_system.git 
   ```
### Запуск без использования Docker
1. Создайте виртуальное окружение:
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/MacOS
    venv\Scripts\activate     # Для Windows
   ```
2. Установите зависимости:
   ```bash
    pip install -r requirements.txt 
   ```
3. Примените миграции:
    ```bash
   python manage.py migrate
   ```
4. Установите настройки базы данных в payment_system.settings.py (раскомментируйте при необходимости)
   ```text
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```
4. Запустите сервер:
    ```bash
    python manage.py runserver
    ```
### Запуск c использованием Docker

Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные окружения:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=blog_password
DB_HOST=db
DB_PORT=5432
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com
```
Замените your-secret-key на случайную строку (например, используйте Django Secret Key Generator ).

Установите настройки базы данных в payment_system.settings.py (раскомментируйте при необходимости)
   ```text
      DATABASES = {
          "default": {
              "ENGINE": "django.db.backends.postgresql",
              "NAME": os.getenv("DB_NAME", "snippet_db"),  # имя базы данных
              "USER": os.getenv("DB_USER", "admin"),  # имя пользователя
              "PASSWORD": os.getenv("DB_PASSWORD", "admin"),  # пароль
              "HOST": os.getenv("DB_HOST", "db"),  # или IP-адрес сервера базы данных
              "PORT": os.getenv("DB_PORT", "5432"),  # порт
          },
      }
   ```

Выполните командy:
```bash
    docker compose up --build
```

Это создаст и запустит контейнеры для Django, PostgreSQL. После завершения сборки проект будет доступен по адресу:
```http
http://localhost:8000/
```

**Автоматические миграции и создание суперпользователя**

**Во время запуска Docker автоматически выполняет следующие действия**:

- Применяет миграции базы данных.
- Создает суперпользователя (если он еще не существует) с данными, указанными в переменных окружения:
  - `DJANGO_SUPERUSER_USERNAME`
  - `DJANGO_SUPERUSER_PASSWORD`
  - `DJANGO_SUPERUSER_EMAIL` (опционально)
- Собирает статические файлы.
   
## API
1. POST /api/webhook/bank/ 
Принимает данные о платеже в формате JSON. 
Заголовки запроса: 
```http
Content-Type: application/json
```
Пример тела запроса:
```json
    {
    "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
    "amount": 145000,
    "payer_inn": "1234567890",
    "document_number": "PAY-328",
    "document_date": "2024-04-27T21:00:00Z"
    }
```
Возможные ответы:
 - 200 OK : Платеж успешно обработан или уже был обработан ранее.
```json
{
    "message": "Payment processed successfully"
}
```
 - 400 Bad Request : Некорректные данные в запросе.
```json
{
    "error": "Invalid data"
}
```
2. GET /api/organizations/<inn>/balance/ 

Возвращает текущий баланс организации по её ИНН. 
Пример запроса: 
```http
GET /api/organizations/1234567890/balance/
```
Возможные ответы: 

 - 200 OK : Баланс успешно найден.
```json
{
    "inn": "1234567890",
    "balance": 145000.00
}
```
 - 404 Not Found : Организация с указанным ИНН не найдена.
```json
{
    "error": "Organization not found"
}
```
Пример запроса через cURL: 

 - POST /api/webhook/bank/ : 
   ```bash
    curl -X POST http://127.0.0.1:8000/api/webhook/bank/ \
    -H "Content-Type: application/json" \
    -d '{
        "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
        "amount": 145000,
        "payer_inn": "1234567890",
        "document_number": "PAY-328",
        "document_date": "2024-04-27T21:00:00Z"
    }'
   ```
 - GET /api/organizations/<inn>/balance/ :
   ```bash
    curl -X GET http://127.0.0.1:8000/api/organizations/1234567890/balance/
   ```
## Логирование изменений баланса 

Каждое изменение баланса логируется в таблицу BalanceLog. Это позволяет отслеживать историю изменений баланса организаций. Лог содержит следующие данные:
 - Предыдущий баланс (previous_balance).
 - Новый баланс (new_balance).
 - Ссылка на соответствующий платеж (payment).

##  Автор 

- Автор проекта: Байков Петр.
- Контакты: petr.bajjkov@rambler.ru 