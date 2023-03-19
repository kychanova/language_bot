# There are specific functions for training_func.py
import re
from random import choice
from typing import Text, Any

from aiogram.methods.send_audio import SendAudio
from aiogram.methods.send_message import SendMessage

from utils.parsing_utils import get_word_dict_fd
from utils.parsing_utils import get_page



async def miss_in_dictionary(chat_id, word, bot):
    mes_text = f"I don't have the word <strong>{word}</strong> in the base(((\nSo just repeat it. "
    await bot.send_message(chat_id=chat_id, text=mes_text)


def make_word_train_task(word: Text) -> Text:
    """
    This function form task text. For that get word dict from FreeDictionary API.
    If there is no information about this word in FreeDictionary, return text about this.
    :param word:
    :return: task text
    """
    word_dict = get_word_dict_fd(word)
    if not word_dict:
        return word_dict
    text = ''
    def_exmp =  []
    for word_mean in word_dict[0]['meanings']:
        for word_def in word_mean['definitions']:
            def_exmp.append((word_def.get('definition'), word_def.get('example')))
    for d, e in def_exmp:
        if d:
            replaced = re.sub(word, '_____', d, flags=re.IGNORECASE)
            text += '<strong>Definition:</strong> ' + replaced + '\n'
        if e:
            replaced = re.sub(word, '_____', e, flags=re.IGNORECASE)
            text += '<strong>Example:</strong> ' + replaced
        text += '\n\n'
    return text