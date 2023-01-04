import logging

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.PostgreSQL import add_user_to_db


router = Router(name='general_router')


@router.message(Command(commands=['start']))
async def start_handler(message: types.Message, state: FSMContext):
    await state.set_state()
    logging.info('start handling')
    await message.answer("Hello! I'm bot, that can help you improve your english skills.\n"
                        "Choose the option that you interested in and write down the command:\n"
                        "/send_article: I'll send you news articles and then ask questions about this;\n"
                        "/word: I'll send you dictionary link and then check you knowledge.")
    add_user_to_db(message.from_user.id, message.chat.id)

