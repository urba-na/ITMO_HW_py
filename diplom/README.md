# Service Desk

Веб-приложение Service Desk, разработанное на Flask, предназначено для регистрации, обработки и сопровождения пользовательских заявок.

## Функциональные возможности

В приложении реализованы следующие возможности:

- регистрация и авторизация пользователей;
- разграничение прав доступа по ролям: пользователь, инженер, администратор;
- создание заявок;
- просмотр и обработка заявок;
- назначение исполнителя;
- изменение статуса заявки;
- добавление комментариев к заявкам;
- контроль сроков обработки заявок (SLA);
- ведение журнала изменений;
- фильтрация и сортировка заявок;
- e‑mail‑уведомления при регистрации и изменении статуса заявки (через тестовый SMTP‑сервис Mailtrap);
- административное управление пользователями (роль, подтверждение, сброс пароля, редактирование e‑mail).

## Технологии

Проект разработан с использованием следующих технологий:

- Python 3
- Flask
- Flask-Login
- Flask-Mail
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- python-dotenv
- Bootstrap 5
- Jinja2
- Mailtrap (Email Sandbox для тестовой отправки писем)

Полный список зависимостей и используемых версий приведён в файле `requirements.txt`.

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/urba-na/ITMO_HW_py.git
cd ITMO_HW_py/diplom
```
### 2. Создание виртуального окружения
macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Настройка переменных окружения

Создайте файл  .env  в корневой папке проекта и укажите необходимые параметры, например:

SECRET_KEY=your_secret_key
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=admin123
DEFAULT_ADMIN_EMAIL=admin@example.com
MAIL_SERVER=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER=no-reply@example.com

### 5. Запуск приложения
```bash
python3 app.py / python app.py
```
После запуска приложение будет доступно по адресу:
http://127.0.0.1:5000

Также для запуска из под Windows подготовлен exe файл
Архив ServiceDeskWindows

## Структура проекта
.
├── app.py
├── main.py (для exe)
├── config.py
├── extensions.py
├── models.py
├── routes.py
├── requirements.txt
├── templates/
├── static/
└── README.md

