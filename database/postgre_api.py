import psycopg as pg

from icecream import ic # FOR DEBUG ONLY
from main import env_vars
from misc.constants import constants


async def db_connect():
    # Подключиться к существующей базе данных/создать базу данных
    with pg.connect(**env_vars.get_db_auth()) as conn:
        with conn.cursor() as cur:
            cur.execute(constants["create_table_query"])
            conn.commit()


async def db_backup():
    # Создает бэкап всей базы данных
    with pg.connect(**env_vars.get_db_auth()) as conn:
        pass

