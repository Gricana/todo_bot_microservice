import os

# Bot credentials
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = os.environ.get("BOT_USERNAME")

# Thirt-party APIs
DJANGOAPI_URL = os.environ.get("DJANGOAPI_URL", 'http://localhost:8080/')
FASTAPI_URL = os.environ.get("FASTAPI_URL", 'http://localhost:8090/')

# Bot storage
REDIS_HOST = os.environ.get("REDIS_HOST", 'redis')
REDIS_PORT = os.environ.get("REDIS_PORT", '6379')

# Task date format
DATE_FORMAT = '%d.%m.%Y %H:%M'

# Time zone settings
USER_TZ = "Europe/Moscow"
SERVER_TZ = "America/Adak"
