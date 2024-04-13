import dotenv
import os
from icecream import ic # FOR DEBUG ONLY!

class EnvReader:
    """
    Class for reading variables from .env file
    """
    def __init__(self, path):
        dotenv.load_dotenv(dotenv_path=path)

    @staticmethod
    def get_bot_token():
        return os.getenv("BOT_TOKEN")

    @staticmethod
    def get_host():
        return os.getenv("DB_HOST")

    @staticmethod
    def get_db_auth():
        """
        Returns data for PostgreSQL's auth from .env file
        :returns: dict with name, username, password, host and port
        """
        params = {
            "password": os.getenv("DB_PASS"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "host": EnvReader.get_host(),
            "port": os.getenv("DB_PORT")
        }
        return params

    @staticmethod
    def get_redis_port():
        return os.getenv("REDIS_PORT")
