from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from forms.WordForm import WordForm
from forms.QuestionsForm import QuestionsForm
#from utils.ml_utils import check_sent_similarity
from utils.handler_utils import make_word_train_task

router = Router(name='form_router')


@router.message(WordForm.attempts)
async def user_word_input_handler(message: types.Message, state: FSMContext):
    async def make_new_task():
        state_data['learned_words_list'].append(state_data['target_word_list'])
        del state_data['words_list'][-1]
        if state_data.get('words_list'):
            word_list = state_data['words_list'][-1]
            text_inner = make_word_train_task(word_list['word'])
            print(f'{state_data["words_list"]=}')
            state_data['target_word_list'] = word_list
            state_data['attempts'] = 0
            await state.set_state(WordForm.attempts)
            print(f'{type(text_inner)=}')
        else:
            await state.set_state()
            text_inner = 'You have learned all words for now!'
        await state.update_data(state_data)
        return text_inner

    state_data = await state.get_data()
    print(f"{state_data=}")
    target_word_list = state_data['target_word_list']
    if message.text == target_word_list['word']:
        await message.answer('Well done!')
        text = await make_new_task()
    else:
        if state_data['attempts'] > 1:
            text = await make_new_task()
            await message.answer('Right answer: ' + target_word_list['word'])
        else:
            text = "Try one more time!"
            await state.update_data(attempts=state_data['attempts']+1)
        await state.set_state(WordForm.attempts)
    print(f'{text=}')
    print(f'{type(text)=}')
    await message.answer(text)


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
