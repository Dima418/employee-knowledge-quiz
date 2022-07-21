import secrets
from dotenv import load_dotenv
from starlette.config import Config
from starlette.datastructures import Secret
from databases import DatabaseURL


load_dotenv()

config = Config(".env")

PROJECT_NAME: str = "Employee Knowledge Quiz"
VERSION: str = "0.0.4"
API_PREFIX: str = "/api"
BACKEND_CORS_ORIGINS: list[str] = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]
TEST_SERVER_HOST: str = "http://localhost:8080"

ENCODING_ALGORITHM: str = "HS256"
SECRET_KEY: str = secrets.token_urlsafe(32)
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 # 1 hour
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day

TEST_USER_EMAIL: str = config("TEST_USER_EMAIL", cast=str)
FIRST_SUPERUSER_EMAIL: str = config("FIRST_SUPERUSER_EMAIL", cast=str)
FIRST_SUPERUSER_PASSWORD: str = config("FIRST_SUPERUSER_PASSWORD", cast=str)

POSTGRES_USER: str = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD: Secret = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str, default="db")
POSTGRES_PORT: str = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB: str = config("POSTGRES_DB", cast=str)
DB_DEFAULT: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL: DatabaseURL = config("DATABASE_URL", cast=DatabaseURL, default=DB_DEFAULT)

TEST_POSTGRES_USER: str = config("TEST_POSTGRES_USER", cast=str)
TEST_POSTGRES_PASSWORD: Secret = config("TEST_POSTGRES_PASSWORD", cast=Secret)
TEST_POSTGRES_HOST: str = config("TEST_POSTGRES_HOST", cast=str, default="db")
TEST_POSTGRES_PORT: str = config("TEST_POSTGRES_PORT", cast=str, default="5432")
TEST_POSTGRES_DB: str = config("TEST_POSTGRES_DB", cast=str)
TEST_DB_DEFAULT: str = f"postgresql://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@{TEST_POSTGRES_HOST}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}"
TEST_DATABASE_URL: DatabaseURL = config("TEST_DATABASE_URL", cast=DatabaseURL, default=TEST_DB_DEFAULT)
