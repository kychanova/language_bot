from aiogram.filters.state import StatesGroup, State


# Список слов на сегодня
class WordForm(StatesGroup):
    words_dict = State()
    learned_words = State()
    target_word = State()
    attempts = State()


