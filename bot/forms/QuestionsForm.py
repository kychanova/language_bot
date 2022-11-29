from aiogram.filters.state import StatesGroup, State


class QuestionsForm(StatesGroup):
    text = State()
    questions = State()
    answers = State()
    user_answer = State()
    attempts = State()