from bot.database.PostgreSQL import get_users_chats, insert_new_user_word, get_words_by_user_and_date


async def load_from_to_db(bot):
    a = get_users_chats()
    print(f'{a=}')





if __name__ == "__main__":
    load_from_to_db()