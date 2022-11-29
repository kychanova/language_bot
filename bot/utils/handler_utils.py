import logging
import re
from random import shuffle
import urllib.request
import json

from textblob import Word



# TODO: сделать вот это нормально!
def make_word_train_text(word_dict):
    text = ''
    if word_dict['definition']:
        text += '<strong>Definition:</strong> ' + \
                word_dict['definition'].pop() + '\n'
    if word_dict['examples']:
        text += '<strong>Example:</strong> ' + \
                word_dict['examples'].pop().replace(word_dict['word'], '_____')
    print(f'make word tran text {type(text)=} ')
    return text


def make_word_train_task(word):
    word_dict = get_word_dict_fd(word)
    if not word_dict:
        return f"I don't have the word <strong>{word}</strong> in the base(((\nSo just repeat it. "
    text = ''
    def_exmp = [(word_def.get('definition'), word_def.get('example'))
                for word_mean in word_dict[0]['meanings']
                for word_def in word_mean['definitions']]
    for d, e in def_exmp:
        if d:
            replaced = re.sub(word, '_____', d, flags=re.IGNORECASE)
            text += '<strong>Definition:</strong> ' + replaced + '\n'
        if e:
            replaced = re.sub(word, '_____', e, flags=re.IGNORECASE)
            text += '<strong>Example:</strong> ' + replaced
        text += '\n\n'
    return text

def get_word_dict_fd(word):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + word
    logging.info(f'{url=}')
    with urllib.request.urlopen(url) as url:
        data = json.load(url)
    if data[0].get('word'):
        return data
    else:
        return None


def spell_checker(text):
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






