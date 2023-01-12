import logging
import re
from random import shuffle
import urllib.request
import json
from typing import Text, Any, Optional, Dict, Tuple

from textblob import Word

from utils.parsing_utils import get_word_dict_fd


# def make_word_train_text(word_dict):
#     text = ''
#     if word_dict['definition']:
#         text += '<strong>Definition:</strong> ' + \
#                 word_dict['definition'].pop() + '\n'
#     if word_dict['examples']:
#         text += '<strong>Example:</strong> ' + \
#                 word_dict['examples'].pop().replace(word_dict['word'], '_____')
#     print(f'make word tran text {type(text)=} ')
#     return text


def make_word_train_task(word: Text) -> Text:
    """
    This function form task text. For that get word dict from FreeDictionary API.
    If there is no information about this word in FreeDictionary, return text about this.
    :param word:
    :return: task text
    """
    word_dict = get_word_dict_fd(word)
    if not word_dict:
        return f"I don't have the word <strong>{word}</strong> in the base(((\nSo just repeat it. "
    text = ''
    def_exmp =  []
    for word_mean in word_dict[0]['meanings']:
        # if len(word_mean)>3:
        #     num_def = 1
        # elif len(word_mean)>2:
        #     num_def = 2
        # else:
        #     num_def = 3
        # shuffle(word_mean['definitions'])
        # for word_def in word_mean['definitions'][:num_def]:
        #     def_exmp.append((word_def.get('definition'), word_def.get('example')))
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


def spell_checker(text: Text) -> Tuple[bool, Text, Text]:
    """

    :param text:
    :return: misspelled: true - if there are mistakes in the text
             unknown - words, that were corrected with small model confidence
             corrected - corrected words
    """
    words = text.split(' ')
    misspelled = False
    corrected = ''
    unknown = ''
    for word in words:
        word_probs = Word(word).spellcheck()
        logging.info(f'{word_probs=}')

        if word_probs[0][1] < 0.5:
            unknown += word_probs[0][0]
            misspelled = True
        else:
            corrected += word_probs[0][0]

        if word != word_probs[0][0]:
            misspelled = True
    return misspelled, unknown, corrected






