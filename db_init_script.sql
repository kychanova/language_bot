--CREATE TABLE words (
--id serial PRIMARY KEY,
--word varchar(15),
--definitions text[],
--examples text[]
--)


CREATE TABLE IF NOT EXISTS user_words (
id_user int,
word int,
repetition_date date,
days_count int,
CONSTRAINT PK_UW PRIMARY KEY (id_user,word)
)

CREATE TABLE IF NOT EXISTS users_chats (
id_user int,
id_chat int,
CONSTRAINT PK_UC PRIMARY KEY (id_user,id_chat)
)

