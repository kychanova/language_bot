import time
import logging

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from gensim.summarization import summarize

from utils.ml_utils import generate_answers #,check_sent_similarity
from utils.parsing_utils import parsing_article
from utils.question_generator_class import QuestionGenerator
from forms.QuestionsForm import QuestionsForm


router = Router(name='article_router')
question_generator = QuestionGenerator()

@router.message(Command(commands=['send_article']))
async def send_article_handler(message: types.Message, state: FSMContext):
    await message.answer('Finding article...')
    conv_router = '/us/arts'
    start_parsing = time.time()
    content_dict = parsing_article(conv_router)
    logging.info(f'Parsing time = {time.time() - start_parsing}')
    start_sum = time.time()
    summarized = ''
    for title, p_list in content_dict.items():
        summarized += '<strong>' + title + '</strong>\n'
        summarized += summarize(''.join(p_list), ratio=0.3) + '\n'
    logging.info(f'Summarization time = {time.time()-start_sum}')
    await state.set_state(QuestionsForm.text)
    await state.update_data(text=summarized)
    await message.answer(summarized)
    await message.answer("Try understand it. If you don't know a word just write down command: "
                         "/word with the word of interest. For example,\n<strong> /word amazing'</strong>.\n"
                         "You can do it any time you need\n"
                         "When you will be ready, send /questions command to check your understanding.")
    start_qgen = time.time()
    quests = question_generator.generate_question(summarized, 2)
    await state.set_state(QuestionsForm.questions)
    await state.update_data(questions=quests)
    logging.info(f'Q generation time = {time.time()-start_qgen}')

    answers = generate_answers(summarized, quests)
    await state.set_state(QuestionsForm.answers)
    await state.update_data(answers=answers)


@router.message(Command(commands=['questions']))
async def questions_handler(message: types.Message, state: FSMContext):
    print('questions command handler')
    quest_data = await state.get_data()
    question = quest_data['questions'].pop()
    await message.answer(question)

    await state.update_data(questions=quest_data['questions'])
    await state.update_data(attempts=0)
    await state.set_state(QuestionsForm.attempts)


