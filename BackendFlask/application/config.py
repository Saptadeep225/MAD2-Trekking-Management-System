import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTANCE_PATH = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_PATH, exist_ok=True)


class Config:
    SECRET_KEY = "trekking-secret-key"
    JWT_SECRET_KEY = "trekking-jwt-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(INSTANCE_PATH, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery configuration
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    # Cache configuration
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300

    # Mail configuration
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    SENDER_EMAIL = "admin@trek.com"
    SENDER_PASSWORD = ""
