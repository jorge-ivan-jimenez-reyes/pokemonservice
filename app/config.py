import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pokemon_user:pokemon_pass@db:5432/pokemon_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "pokemon_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pokemon_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "pokemon_db") 