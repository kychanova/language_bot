import logging
import os
from datetime import date

import asyncio
import yaml
from aiogram.methods import SendMessage
from dotenv import load_dotenv
from aiogram.fsm.storage.base import StorageKey
from aiogram.client.bot import Bot

from utils.training_func import defs_trainer
from custom_classes.Word import Word
from forms.WordForm import WordForm
from utils.handler_utils import make_word_train_task, add_words, train_words


# dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
TOKEN = os.environ.get('TOKEN')
BOT_ID = int(os.environ.get('BOT_ID'))
print(f'{TOKEN=}')
with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file)

from database.PostgreSQL import get_users_chats, insert_user_word, get_words_by_user_and_date

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def load_from_to_db(bot, dp):
    logger.debug('load_scheduler')
    print('This is scheduled func')
    ids = get_users_chats()
    for row in ids:
        sk = StorageKey(bot_id=BOT_ID, user_id=row[0], chat_id=row[1])
        state_data = await dp.storage.get_data(bot, sk)
        if state_data['learned_words_list']:
            for word in state_data['learned_words']:
                insert_user_word(row[0], word['word'],
                                 date.fromisoformat(word['repetition_date']),
                                 word['days_count'])

        wls = get_words_by_user_and_date(row[0], date.today())
        words = state_data.get('words', dict())
        for wl in wls:
            words[wl[1]] = {'repetition_date': wl[2].isoformat(), 'days_count':wl[3]}
        print(f'{type(words)=}')
        print(f'{words}')
        await dp.storage.update_data(bot=bot, key=sk, data={'words': words})


async def train_words_in_time(bot, dp):
    # print('bot')
    # bot.context()
    # print(Bot.get_current(no_error=False))
    #Bot = bot
    logger.debug('train_scheduler')
    ids = get_users_chats()
    for row in ids:
        logging.info(f'{row=}')
        sk = StorageKey(bot_id=BOT_ID, user_id=row[0], chat_id=row[1])
        state = await dp.storage.get_state(bot=bot, key=sk)
        if state == 'QuestionsForm:attempts':
            continue
        state_data = await dp.storage.get_data(bot, sk)
        logging.info(f'state_data_from_train = {state_data}')
        if state_data.get('words'):
            words_message = 'Time for training!\nWords for this train:\n' + \
                            '\n'.join([w for w, d in state_data['words'].items()])
            await bot.send_message(chat_id=row[1], text=words_message)
            #await SendMessage(chat_id=row[1], text=words_message)

            state_data = await train_words(bot=bot, chat_id=row[1], state_data=state_data)

            await dp.storage.update_data(bot, sk, state_data)
            await dp.storage.set_state(bot, sk, WordForm.attempts)


async def main():
    await load_from_to_db()


if __name__ == "__main__":
    asyncio.run(main())
