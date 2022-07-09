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

ENCODING_ALGORITHM: str = "HS256"

SECRET_KEY: str = secrets.token_urlsafe(32)
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

JWT_AUTH_PATH: str = "/auth-jwt"
GOOGLE_AUTH_PATH: str = "/auth-google"
GOOGLE_AUTH_URL: str = "http://127.0.0.1:8000" + GOOGLE_AUTH_PATH

GOOGLE_CLIENT_ID :str = config("GOOGLE_CLIENT_ID", cast=str)
GOOGLE_CLIENT_SECRET :str = config("GOOGLE_CLIENT_SECRET", cast=str)

POSTGRES_USER: str = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD: Secret = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str, default="db")
POSTGRES_PORT: str = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB: str = config("POSTGRES_DB", cast=str)

DB_DEFAULT: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL: DatabaseURL = config("DATABASE_URL", cast=DatabaseURL, default=DB_DEFAULT)
