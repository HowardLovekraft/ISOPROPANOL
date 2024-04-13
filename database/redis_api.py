import redis.asyncio as redis
import redis.exceptions
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from misc.printers import state_printer


async def connect(env_vars, printer) -> tuple[RedisStorage | MemoryStorage, str]:
    try:
        client = redis.Redis(host=env_vars.get_host(),
                             port=env_vars.get_redis_port(),
                             decode_responses=True)

        res = client.ping()
        if not res:
            print("REDIS FAILED TO PING")
        await client.aclose()  # Чтобы закрыть соединение с Redis
        storage = RedisStorage(redis=client)
        db_type = "REDIS"

    except redis.exceptions.ConnectionError:
        print(state_printer("REDIS", printer.max_len, "NOT INITIALIZED"))
        storage = MemoryStorage()
        db_type = "MEMORY STORAGE"

    return storage, db_type
