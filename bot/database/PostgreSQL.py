import os
import psycopg2
import logging
from datetime import date, timedelta
from glob import glob

import yaml
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, Date, PrimaryKeyConstraint, String
from sqlalchemy.sql import select, and_, exists
from sqlalchemy.dialects.postgresql import insert

# TODO: implement repository pattern
logging.info(f'{os.getcwd()}')
with open('config.yml', 'r') as file:
   config_data = yaml.safe_load(file)
# if config_data.get('data_base') == 'postgres':
connect_string = f"postgresql://{os.environ.get('POSTGRES_USER')}:" \
                 f"{os.environ.get('POSTGRES_PASSWORD')}" \
                 f"@{config_data.get('postgres_host')}:5432/{os.environ.get('POSTGRES_DB')}"
engine = create_engine(connect_string)
conn = engine.connect()
meta = MetaData(engine)


def insert_user_word(user_id: int, word: str, repetition_date: date, days_count: int = 0) -> None:
    today_date = date.today()
    if (today_date - repetition_date).days > 2:
        days_count_next = days_count
    else:
        days_count_next = days_count * 2 + 1
    next_date = today_date + timedelta(days_count_next-days_count)
    if days_count == 0:
        query = insert(users_words).values(id_user=user_id, word=word, repetition_date=next_date,
                                           days_count=days_count_next)
        query = query.on_conflict_do_update(constraint='uw_pk', set_={'repetition_date': next_date,
                                                                      'days_count': days_count_next})
    else:
        query = users_words.update().where(id_user=user_id, word=word).\
                                    values(repetition_date=next_date, days_count=days_count_next)
    conn.execute(query)


def get_words_by_user_and_date(user_id: int, date: date) -> list[tuple]:
    query = users_words.select().where(and_(users_words.c.id_user == user_id,
                                            users_words.c.repetition_date <= date))
    res = conn.execute(query)
    return res.fetchall()


def add_user_to_db(user_id: int, chat_id: int) -> None:
    query = users_chats.insert().values(id_user=user_id, id_chat=chat_id)
    conn.execute(query)


def get_users_chats() -> list[tuple]:
    query = users_chats.select()
    res = conn.execute(query)
    return res.fetchall()


def init_db():
    uw_table = Table('users_words', meta,
                     Column('id_user', Integer),
                     Column('word', String(50)),
                     Column('repetition_date', Date),
                     Column('days_count', Integer),
                     PrimaryKeyConstraint('id_user', 'word', name='uw_pk'))

    uc_table = Table('users_chats', meta,
                     Column('id_user', Integer),
                     Column('id_chat', Integer),
                     PrimaryKeyConstraint('id_user', 'id_chat', name='uc_pk'))

    meta.create_all(engine)


init_db()
users_words = Table('users_words', meta, autoload=True)
users_chats = Table('users_chats', meta, autoload=True)

