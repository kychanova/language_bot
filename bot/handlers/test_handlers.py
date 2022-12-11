import logging

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


router = Router(name='test_router')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@router.message(Command(commands=['get_state_data']))
async def questions_handler(message: types.Message, state: FSMContext):
    state_data_from_test = await state.get_data()
    if state_data_from_test:
        logging.info(f'{state_data_from_test=}')
        print('print:')
        print(f'{state_data_from_test=}')
        logger.debug('debug logger:')
        logger.debug(f'{state_data_from_test=}')
    else:
        logging.info(f'no state_data from test')
        print('print: no state_data from test')
        logger.debug('logger debug: no state_data from test')