import logging

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


router = Router(name='test_router')


@router.message(Command(commands=['state_data']))
async def questions_handler(message: types.Message, state: FSMContext):
    state_data_from_test = await state.get_data()
    logging.info(f'{state_data_from_test=}')