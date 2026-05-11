import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

default_db_path = os.path.join(INSTANCE_DIR, 'service_desk.db')

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    f"sqlite:///{default_db_path}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD')
DEFAULT_USER_PASSWORD = os.getenv('DEFAULT_USER_PASSWORD')

MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

required_vars = {
    'SECRET_KEY': SECRET_KEY,
    'DEFAULT_ADMIN_PASSWORD': DEFAULT_ADMIN_PASSWORD,
    'DEFAULT_USER_PASSWORD': DEFAULT_USER_PASSWORD
}

missing = [key for key, value in required_vars.items() if not value]

if missing:
    raise ValueError(
        f'Не заданы обязательные переменные окружения: {", ".join(missing)}'
    )
