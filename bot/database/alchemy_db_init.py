import logging
import os
import yaml
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, Date, PrimaryKeyConstraint
from sqlalchemy.sql import select, and_, exists

# TODO: implement repository pattern
logging.info(f'{os.getcwd()}')
with open('config.yml', 'r') as file:
   config_data = yaml.safe_load(file)
if config_data.get('data_base') == 'postgres':
    connect_string = f"postgresql://{os.environ.get('POSTGRES_USER')}:" \
                     f"{os.environ.get('POSTGRES_PASSWORD')}" \
                     f"@{config_data.get('postgres_host')}:5432/{os.environ.get('POSTGRES_DB')}"
engine = create_engine(connect_string)
conn = engine.connect()
meta = MetaData(engine)


def init_db():
    logging.info('create tables')
    uw_table = Table('users_words', meta,
                     Column('id_user', Integer),
                     Column('word', Integer),
                     Column('repetition_date', Date),
                     Column('days_count', Integer),
                     PrimaryKeyConstraint('id_user', 'word', name='uw_pk'))

    uc_table = Table('users_chats', meta,
                     Column('id_user', Integer),
                     Column('id_chat', Integer),
                     PrimaryKeyConstraint('id_user', 'id_chat', name='uc_pk'))

    meta.create_all(engine)
