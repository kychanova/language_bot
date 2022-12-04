import os
import logging
import asyncio
from glob import glob
from importlib.machinery import SourceFileLoader

import aioredis

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
print(f"{os.environ.get('TOKEN')=}")
# from database import init_database
from database.alchemy_db_init import init_db
init_db()
from sch_test import load_from_to_db, train_words_in_time

# from handlers import article_handlers
# from handlers import general_handlers

# TOKEN = os.environ.get('TOKEN')
# logging.info(f'{TOKEN=}')
# print(f'{TOKEN=}')
with open('config.yml', 'r') as file:
   config_data = yaml.safe_load(file)


async def main():
    logging.basicConfig(level=logging.INFO)
    TOKEN = os.environ.get('TOKEN')
    bot = Bot(token=TOKEN, parse_mode='HTML')

    redis = aioredis.Redis(host=f"{config_data.get('redis_host')}", port=6279)
    storage = RedisStorage(redis=redis)
    #storage = MemoryStorage()
    # modules = glob('bot/handlers/*.py')
    # logging.info(f'{modules=}')
    modules = glob('./handlers/*.py')
    logging.info(f'{modules=}')
    imported_modules = list(map(lambda pathname: SourceFileLoader(pathname, path=pathname).load_module(), modules))
    logging.info(f'{imported_modules=}')
    dp = Dispatcher(bot=bot, storage=storage)

    for module in imported_modules:
        dp.include_router(module.router)
    # dp.include_router(article_handlers.router)
    # dp.include_router(general_handlers.router)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_from_to_db, "cron", hour=3, args=(bot, dp))
    scheduler.add_job(load_from_to_db, "interval", hours=3, args=(bot, dp))
    scheduler.start()
    # await load_from_to_db(bot, dp)
    logging.info('there was made main variables')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
