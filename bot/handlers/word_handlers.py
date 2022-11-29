import logging
import re
from datetime import date

from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject, Text
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from textblob import Word

from forms.WordForm import WordForm
from utils.handler_utils import make_word_train_text, make_word_train_task, spell_checker
from utils.parsing_utils import parsing_dict
from database.PostgreSQL import insert_new_user_word, get_words_by_user_and_date
from keyboards.word_keyboards import after_spell_check_keyboard, after_spell_check_unknown_keyboard

router = Router(name='word_router')
scheduler = AsyncIOScheduler()
BASE_URL = 'https://www.collinsdictionary.com/dictionary/english/'

# def word_examples(word_list):
#     for word_dict in word_list:
#         yield word_dict


@router.message(Command(commands=['word']))
async def word_handler(message: types.Message, command: CommandObject, state:FSMContext):
    if command.args:
        # use html.quote(), if you need экранировать symbols: <>
        print(f'{command.args=}')
        text = command.args.strip()
        print(f'{text}')
        misspelled, unknown, corrected = spell_checker(text)
        url = BASE_URL + re.sub(r'\s+', '-', text)

        if unknown:
            await message.answer(f'There are possible mistakes in words: {unknown}.\n'
                                 f'You can find possible words here: {url}. \n'
                                 f'Should I remember it anyway?',
                                 reply_markup=after_spell_check_unknown_keyboard(text))
            return
        if misspelled:
            await message.answer(f'I found possible mistakes. Did you mean: {corrected}',
                                 reply_markup=after_spell_check_keyboard(text, corrected))
            return

        await message.answer(f"Visit the dictionary: {url}.\nI'll check your knowledge later")

        await add_word_to_rstorage(text, state)
    else:
        await message.answer("Please, input the word you wanna know after command /word")


@router.callback_query(Text(startswith='rem'))
async def right_spell_correction_handler(callback: types.CallbackQuery, state: FSMContext):
    text = callback.data.split("_")[1]
    url = BASE_URL + re.sub(r'\s+', '-', text)
    await callback.answer(f"Visit the dictionary: {url}.\nI'll check your knowledge later")

    await add_word_to_rstorage(text, state)


@router.callback_query(Text(text="pass"))
async def right_spell_correction_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('OK')


@router.callback_query(Text(startswith='sr'))
async def right_spell_correction_handler(callback: types.CallbackQuery, state: FSMContext):
    text = callback.data.split("_")[1]
    url = BASE_URL + re.sub(r'\s+', '-', text)
    await callback.message.answer(f"Visit the dictionary: {url}.\nI'll check your knowledge later")

    await add_word_to_rstorage(text, state)


@router.callback_query(Text(startswith='swi'))
async def wrong_spell_correction_handler(callback: types.CallbackQuery, state: FSMContext):
    text = callback.data.split("_")[1]
    url = BASE_URL + re.sub(r'\s+', '-', text)
    await callback.message.answer(f"Visit the dictionary: {url}.\nI'll check your knowledge later")

    await add_word_to_rstorage(text, state)


async def add_word_to_rstorage(word, state):
    state_data = await state.get_data()
    wl = state_data.get('words_list', [])
    wl.append({'word': word, 'repetition_date': str(date.today()), 'days_count': 0})
    await state.update_data(words_list=wl)

@router.message(Command(commands=['get_words']))
async def get_words(message: types.Message, command: CommandObject, state: FSMContext):
    # wl = [{'word': 'word1', 'definition': ['word1_def', 'w1d2'], 'examples': ['word1_exmp','w1e2','w1e3']},
    #       {'word': 'word2', 'definition': ['word2_def'], 'examples': ['word2_exmp']},
    #       {'word': 'word3', 'definition': ['word3_def'], 'examples': ['word3_exmp']}]
    # async with state.proxy() as data:
    #     data['words_list'] = words_list
    # wl = ['retain', 'dismissal']
    wl = get_words_by_user_and_date(message.from_user.id, date.today())
    await state.update_data(words_list=wl)
    logging.info('Data is added to storage')


@router.message(Command(commands=['see_state']))
async def get_words(message: types.Message, command: CommandObject, state: FSMContext):
    sd = await state.get_data()
    print(f'{sd=}')



@router.message(Command(commands=['train_words']))
async def train_words_handler(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data.get('words_list'):
        word_list = state_data['words_list'].pop()
        # text = make_word_train_text(word_dict)
        state_data['target_word_list'] = word_list
        if not state_data.get('learned_words_list'):
            state_data['learned_words_list'] = []
        state_data['attempts'] = 0

        await state.update_data(state_data)
        await state.set_state(WordForm.attempts)
        text = make_word_train_task(word_list['word'])
    else:
        text = 'There are not words for today studying.'

    await message.answer(text)


# Get from DB:
#   1. Def and exmp should be lists
#   2. Shuffle them before send





