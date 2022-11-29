# from aiogram import Router
#
#
# router = Router()
#
# @router.message(commands=['send_article'])
# async def send_article_handler(message: types.Message, state: types.FSMState):
#     url = 'https://theconversation.com/us/arts'
#     article_text = article_recipient.parsing(url)
#     logging.debug(f'{article_recipient.id=}')
#
#     summarized = bert_summarizer(article_text, num_sentences=15)
#     state.update_data(text=summarized)
#     await message.answer(summarized)
#     await message.answer("Try understand it. If you don't know a word just write down command:"
#                          "/word: and the word. For example, /word: amazing'.\n"
#                          " You can do it any time you need")