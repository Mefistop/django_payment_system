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
payments_system/
├── manage.py
├── payments_system/
│   ├── init .py
│   ├── settings.py          # Настройки проекта
│   ├── urls.py              # Главный маршрутизатор URL-адресов
│   ├── wsgi.py              # Конфигурация WSGI
│   └── asgi.py              # Конфигурация ASGI
├── payments/
│   ├── migrations/          # Миграции базы данных
│   ├── init .py
│   ├── admin.py             # Регистрация моделей в админке
│   ├── apps.py              # Конфигурация приложения
│   ├── models.py            # Модели Django
│   ├── serializers.py       # Сериализаторы DRF
│   ├── tests.py             # Тесты
│   ├── views.py             # Представления (views)
│   └── urls.py              # Маршруты URL для приложения
├── requirements.txt         # Зависимости проекта
└── README.md                # Документация проекта
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Mefistop/django_payment_system.git 
   ```
2. Создайте виртуальное окружение:
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/MacOS
    venv\Scripts\activate     # Для Windows
   ```
3. Установите зависимости:
   ```bash
    pip install -r requirements.txt 
   ```
4. Примените миграции:
    ```bash
   python manage.py migrate
   ```
5. Запустите сервер:
    ```bash
    python manage.py runserver
    ```
   
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