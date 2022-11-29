from aiogram.filters.state import StatesGroup, State


# Список слов на сегодня
class WordForm(StatesGroup):
    words_list = State()
    learned_words_list = State()
    target_word_list = State()
    attempts = State()


