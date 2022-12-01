import os
from datetime import date

import asyncio
import yaml
from dotenv import load_dotenv
from aiogram.fsm.storage.base import StorageKey

from forms.WordForm import WordForm
from utils.handler_utils import make_word_train_task


dotenv_path = os.path.join(os.path.dirname(__file__), '../.env.example')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
TOKEN = os.environ.get('TOKEN')
BOT_ID = int(os.environ.get('BOT_ID'))
print(f'{TOKEN=}')
with open('config.yml', 'r') as file:
   config_data = yaml.safe_load(file)

from database.PostgreSQL import get_users_chats, insert_user_word, get_words_by_user_and_date


async def load_from_to_db(bot, dp):
    print('This is scheduled func')
    ids = get_users_chats()
    for row in ids:
        sk = StorageKey(bot_id=BOT_ID, user_id=row[0], chat_id=row[1])
        state_data = await dp.storage.get_data(bot, sk)
        for word_list in state_data['learned_words_list']:
            insert_user_word(row[0], word_list['word'],
                                 date.fromisoformat(word_list['repetition_date']),
                                 word_list['days_count'])

        wls = get_words_by_user_and_date(row[0], date.today())
        words_list = state_data['words_list']
        for wl in wls:
            words_list.append({'word': wl[1],
                               'repetition_date': wl[2],
                               'days_count': wl[3]})
        await dp.storage.update_data(bot, sk, {'words_list': words_list})


async def train_words_in_time(bot, dp):
    ids = get_users_chats()
    for row in ids:
        sk = StorageKey(bot_id=BOT_ID, user_id=row[0], chat_id=row[1])
        state_data = await dp.storage.get_data(bot, sk)
        if state_data.get('words_list'):
            word_list = state_data['words_list'].pop()
            # text = make_word_train_text(word_dict)
            state_data['target_word_list'] = word_list
            if not state_data.get('learned_words_list'):
                state_data['learned_words_list'] = []
            state_data['attempts'] = 0

            await dp.storage.update_data(bot, sk, state_data)
            await dp.storage.set_state(bot, sk, WordForm.attempts)
            text = make_word_train_task(word_list['word'])
        else:
            text = 'There are not words for today studying.'

        await bot.send_message(chat_id=row[1], text=text)

async def main():
    await load_from_to_db()

if __name__ == "__main__":
    asyncio.run(main())