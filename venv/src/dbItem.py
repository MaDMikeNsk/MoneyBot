import random

from sqlalchemy import Column, Integer, create_engine, Boolean, String, TEXT
from sqlalchemy.ext.declarative import declarative_base
from src import config

engine = create_engine(config.DB_PATH, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'UserBalance'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    user_id = Column(Integer)
    tasks_counter = Column(Integer) # Всего заданий выполнено
    subscribes_counter = Column(Integer) # Всего подписок на каналы

    total_referals = Column(Integer) # Приглашено пользователей (рефералов)
    redirect_counter = Column(Integer) # Переходов по ссылкам
    voicemsg_counter = Column(Integer) # Отправлено голосовых сообщений
    total_balance = Column(Integer) # Общее кол-во баллов
    from_referals = Column(Integer) # Баллы от рефералов

    skipped_simple_post = Column(Integer) # Пропущено простых постов
    skipped_hard_post = Column(Integer) # Пропущено сложных постов
    simple_post_view = Column(Integer) # Просмотрено простых постов
    hard_post_view = Column(Integer) # Просмотрено сложных постов

    subscribed_ch = Column(Integer)  # Сделано подписок
    skipped_ch = Column(Integer) # Пропущено каналов

    step1_link_counter = Column(Integer)  # Ссылок просмотрено (простые)
    step2_link_counter = Column(Integer)  # Ссылок просмотрено (2-х шаговые)
    step3_link_counter = Column(Integer)  # Ссылок просмотрено (3-х шаговые)
    skipped_1step_links = Column(Integer) # Пропущено ссылок (простые)
    skipped_2step_links = Column(Integer)  # Пропущено ссылок (2-х шаговые)
    skipped_3step_links = Column(Integer)  # Пропущено ссылок (3-х шаговые)

    def __init__(self, user_id):
        self.user_id = user_id
        self.tasks_counter = self.subscribes_counter = self.total_referals = \
            self.redirect_counter = self.voicemsg_counter = self.total_balance = self.from_referals = \
            self.skipped_simple_post = self.skipped_ch = self.link_counter = self.skipped_links = \
            self.skipped_hard_post = self.simple_post_view = self.skipped_hard_post = self.hard_post_view = \
            self.subscribed_ch = self.step1_link_counter = self.step2_link_counter = self.step3_link_counter = \
            self.skipped_1step_links = self.skipped_2step_links = self.skipped_3step_links = 0


class Channels(Base):
    __tablename__ = 'Channels'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    chat_name = Column(TEXT)
    title = Column(String(50))
    link = Column(TEXT)

    def __init__(self, chat_name, title, link):
        self.chat_name = chat_name
        self.title = title
        self.link = link


class Posts_Simple(Base):
    __tablename__ = 'Posts_Simple'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    title = Column(String(50))
    link = Column(TEXT)
    bonus = Column(Integer)
    time = Column(Integer)

    def __init__(self, title, link, time, bonus=2):
        self.title = title
        self.link = link
        self.bonus = bonus
        self.time = time

            
class Posts_Hard(Base):
    __tablename__ = 'Posts_Hard'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    title = Column(String(50))
    link = Column(TEXT)
    bonus = Column(Integer)
    time = Column(Integer)

    def __init__(self, title, link, time, bonus=None):
        self.title = title
        self.link = link
        self.time = time
        if bonus:
            self.bonus = bonus
        else:
            self.bonus = random.randint(3, 5)


class Links_Simple(Base):
    __tablename__ = 'Links_Simple'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    title = Column(String(50))
    link = Column(TEXT)
    bonus = Column(Integer)
    time = Column(Integer)

    def __init__(self, title, link, time, bonus=None):
        self.title = title
        self.link = link
        self.time = time
        if bonus:
            self.bonus = bonus
        else:
            self.bonus = random.randint(2, 3)


class Links_2_Stage(Base):
    __tablename__ = 'Links_2_Stage'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    title = Column(String(50))
    link_1 = Column(TEXT)
    link_2 = Column(TEXT)
    time_1 = Column(Integer)
    time_2 = Column(Integer)
    bonus = Column(Integer)

    def __init__(self, title, link_1, link_2, time_1, time_2, bonus=None):
        self.title = title
        self.link_1 = link_1
        self.link_1 = link_2
        self.time_1 = time_1
        self.time_2 = time_2
        if bonus:
            self.bonus = bonus
        else:
            self.bonus = random.randint(3, 5)


class Links_3_Stage(Base):
    __tablename__ = 'Links_3_Stage'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    title = Column(String(50))
    link_1 = Column(TEXT)
    link_2 = Column(TEXT)
    link_3 = Column(TEXT)
    time_1 = Column(Integer)
    time_2 = Column(Integer)
    time_3 = Column(Integer)
    bonus = Column(Integer)

    def __init__(self, title, link_1, link_2, link_3, time_1, time_2, time_3, bonus=None):
        self.title = title
        self.link_1 = link_1
        self.link_2 = link_2
        self.link_3 = link_3
        self.time_1 = time_1
        self.time_2 = time_2
        self.time_3 = time_3
        if bonus:
            self.bonus = bonus
        else:
            self.bonus = random.randint(6, 9)


Base.metadata.create_all(engine)
