import secrets
from dotenv import load_dotenv
from starlette.config import Config
from starlette.datastructures import Secret
from databases import DatabaseURL

load_dotenv()

config = Config(".env")

PROJECT_NAME = "Employee Knowledge Quiz"
VERSION = "0.0.4"
API_PREFIX = "/api"

SECRET_KEY: str = secrets.token_urlsafe(32)
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
ACCESS_TOKEN_URL: str = "/signin/access-token"

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_HOST = config("POSTGRES_HOST", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DB_DEFAULT = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL = config("DATABASE_URL", cast=DatabaseURL, default=DB_DEFAULT)
