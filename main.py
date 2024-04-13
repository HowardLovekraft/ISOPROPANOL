import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from misc.printers import StatePrinter
from env.env_reader import EnvReader

env_vars = EnvReader("env/venv.env")
i18n = I18n(path="locales",
            default_locale="ru",
            domain="messages")
i18n_middleware = SimpleI18nMiddleware(i18n)
printer = StatePrinter(max_len=14)

import database.postgre_api as postgre_db # requires env_vars
import database.redis_api as storage_db # requires env_vars
from handlers import buckshot


async def main() -> None:
    # Connect to PostgreSQL
    await postgre_db.db_connect()
    print(printer.print_status("DB"))

    # Connect to Redis/MemoryStorage (built-in aiogram fsm)
    storage = await storage_db.connect(env_vars, printer)
    dp = Dispatcher(storage=storage[0])
    dp.include_routers(buckshot.router)
    print(printer.print_status(storage[1]))

    # Connect to Telegram API
    bot = Bot(token=EnvReader.get_bot_token())
    await bot.delete_webhook()
    print(printer.print_status("BOT"))

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped by Ctrl-C")