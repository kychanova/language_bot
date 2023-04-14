from math import ceil

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage

from forms.WordForm import WordForm
from forms.QuestionsForm import QuestionsForm
#from utils.ml_utils import check_sent_similarity
from utils.handler_utils import make_word_train_task, train_words

from utils.training_func import defs_trainer

router = Router(name='form_router')


@router.message(WordForm.attempts)
async def user_word_input_handler(message: types.Message, state: FSMContext):
    async def make_new_task(state_data=None):
        word = state_data['target_word']
        state_data['learned_words'].append({'word': word,
                                            'repetition_date': state_data['words'][word]['repetition_date'],
                                            'days_count': state_data['words'][word]['days_count']})
        del state_data['words'][word]
        if state_data.get('words'):
            state_data = await train_words(chat_id=message.chat.id, state_data=state_data)
            await state.set_state(WordForm.attempts)
        else:
            await state.set_state()
            text_inner = 'You have learned all words for now!'
        await state.update_data(state_data)

    state_data = await state.get_data()
    target_word = state_data['target_word']
    if message.text == target_word:
        await message.answer('Well done!')
        await make_new_task(state_data)
    else:
        if state_data['attempts'] > 1:
            await message.answer('Right answer: ' + target_word)
            await make_new_task(state_data)
        elif state_data['attempts']==1:
            await message.answer('A little hint: ' + target_word[:ceil(len(target_word)*0.2)])
        else:
            await message.answer("Try one more time!")
            await state.update_data(attempts=state_data['attempts']+1)
        await state.set_state(WordForm.attempts)


@router.message(QuestionsForm.attempts)
async def user_answer_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(f'{data["questions"]=}')
    print(f'{data["answers"]=}')

    right_answer = data['answers'].pop()
    if message.text.lower() == right_answer.lower():
        print('good answer')
        try:
            message_text = data['questions'].pop()

            await state.update_data(answers=data['answers'])
            await state.update_data(questions=data['questions'])
            await state.update_data(attempts=0)

            await state.set_state(QuestionsForm.user_answer)
        except IndexError:
            print('IndexError')
            message_text = 'Well done!\n You have answered all the questions!'
            await state.set_state()
        await message.answer(message_text)
    else:
        if data['attempts'] > 2:
            text = 'Right answer: ' + right_answer
        else:
            await state.update_data(attempts=data['attempts']+1)
            text = 'Try one more time!'
        await message.answer(text)
