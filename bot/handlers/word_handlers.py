import logging
import re
from datetime import date

from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject, Text
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from textblob import Word

from forms.WordForm import WordForm
from utils.handler_utils import make_word_train_task, spell_checker
from database.PostgreSQL import insert_user_word, get_words_by_user_and_date
from keyboards.word_keyboards import after_spell_check_keyboard, after_spell_check_unknown_keyboard
from custom_classes.Word import Word as Word_local
from utils.handler_utils import add_words, train_words
from utils.training_func import defs_trainer

router = Router(name='word_router')
scheduler = AsyncIOScheduler()
BASE_URL = 'https://www.collinsdictionary.com/dictionary/english/'


@router.message(Command(commands=['word']))
async def word_handler(message: types.Message, command: CommandObject, state:FSMContext):
    await state.set_state()
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
    await callback.message.answer(f"Visit the dictionary: {url}.\nI'll check your knowledge later")

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
    words = state_data.get('words', dict())
    words[word] = {'repetition_date': str(date.today()), 'days_count': 0}
    await state.update_data(words=words)


# @router.message(Command(commands=['get_words']))
# async def get_words(message: types.Message, command: CommandObject, state: FSMContext):
#     wl = get_words_by_user_and_date(message.from_user.id, date.today())
#     await state.update_data(words_list=wl)
#     logging.info('Data is added to storage')


@router.message(Command(commands=['train_words']))
async def train_words_handler(message: types.Message, state: FSMContext):
    await state.set_state()
    state_data = await state.get_data()
    if state_data.get('words'):
        words_message = 'Words for this train:\n' + \
                        '\n'.join([w for w, d in state_data['words'].items()])
        await message.answer(words_message)

        state_data = await train_words(message.chat.id, state_data)

        await state.update_data(state_data)
        await state.set_state(WordForm.attempts)
    else:
        text = 'There are not words for today studying.'
        await message.answer(text)


@router.message(Command(commands=['get_word_definition']))
async def get_word_info_handler(message: types.Message, command: CommandObject, state:FSMContext):
    await state.set_state()
    if command.args:
        text = command.args.strip()
        url = BASE_URL + re.sub(r'\s+', '-', text)

        await message.answer(f"Visit the dictionary: {url}.")

    else:
        await message.answer("Please, input the word you wanna know after command /get_word_info")






