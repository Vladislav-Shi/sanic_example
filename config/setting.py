from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    DEBUG: bool = True
    APP_NAME: str

    SECRET_KEY: str
    TOKEN_TTL: int = 7200  # 2 часа

    HOST: str = 'http://localhost'
    PORT: int = 8000

    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DATABASE: str

    ADMIN_NAME: str
    ADMIN_PASS: str

    class Config:
        env_file = Path(BASE_DIR, 'config', 'env')
        dotenv.load_dotenv(env_file)

    def create_database_config(self) -> dict:
        return {
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {
                        'host': self.PG_HOST,
                        'port': self.PG_PORT,
                        'database': self.PG_DATABASE,
                        'user': self.PG_USER,
                        'password': self.PG_PASSWORD
                    },
                }
            },
            'apps': {
                'models': {
                    'models': ['app.database', 'aerich.models'],
                    'default_connection': 'default'
                }
            }
        }


config = Setting()
TORTOISE_CONFIG = config.create_database_config()
