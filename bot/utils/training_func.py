# There are only training functions, all specific utils for them and base trainer
# in training_utils.py
import re
from random import choice
from typing import Text, Any

from aiogram.methods.send_audio import SendAudio
from aiogram.methods.send_message import SendMessage

from utils.parsing_utils import get_word_dict_fd
from utils.parsing_utils import get_page

from utils.training_utils import make_word_train_task, miss_in_dictionary


def base_train(bot, chat_id, state_data):
    word = next(iter(state_data['words']))
    state_data['target_word'] = word
    if not state_data.get('learned_words'):
        state_data['learned_words'] = []
    state_data['attempts'] = 0
    return word, state_data


async def audio_trainer(bot, chat_id, state_data):
    word, state_data = base_train(chat_id, state_data)
    regions = {'us':'American', 'uk': 'Britain'}
    not_in_dict = True
    for region, rname in regions.items():
        url = f'https://api.dictionaryapi.dev/media/pronunciations/en/{word}-{region}.mp3'
        r = get_page(url)
        if r.ok:
            #await SendMessage(chat_id=chat_id, text=rname)
            await bot.send_message(chat_id=chat_id, text=rname)
            # print(f'{r.content}')
            #await SendAudio(chat_id=chat_id, audio=url)
            await bot.send_audio(chat_id=chat_id, audio=url)
            not_in_dict = False
    if not_in_dict:
        await miss_in_dictionary(chat_id, word, bot)
    return state_data


async def defs_trainer(bot, chat_id, state_data):
    word, state_data = base_train(chat_id, state_data)
    text = make_word_train_task(word)
    if text:
        #await SendMessage(chat_id=chat_id, text=text)
        await bot.send_message(chat_id=chat_id, text=text)
    else:
        await miss_in_dictionary(chat_id, word, bot)
    return state_data


async def video_trainer(bot, chat_id, state_data):
    video_clips_url = 'https://playphrase.me/#/search?q='
    word, state_data = base_train(chat_id, state_data)
    word = word.replace(' ', '+')
    text = video_clips_url + word
    #await SendMessage(chat_id=chat_id, text=text)
    await bot.send_message(chat_id=chat_id, text=text)
    return state_data



