from dotenv import load_dotenv
from starlette.config import Config
from starlette.datastructures import Secret
from databases import DatabaseURL

load_dotenv()

config = Config(".env")

PROJECT_NAME = "Employee Knowladge Quiz"
VERSION = "0.0.2"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DATABASE_NAME = config("POSTGRES_DATABASE_NAME", cast=str)
DB_DEFAULT = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE_NAME}"
DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=DB_DEFAULT
)