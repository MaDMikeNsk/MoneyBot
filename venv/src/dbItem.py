import random

from sqlalchemy import Column, Integer, create_engine, Boolean, String, TEXT
from sqlalchemy.ext.declarative import declarative_base
from src.config import DB_PATH

engine = create_engine(DB_PATH, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'UserBalance'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    user_id = Column(Integer)
    father_id = Column(Integer) # Реферал-отец
    username = Column(TEXT) # Username in telegramm
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

    ch_active = Column(Boolean)
    post_active = Column(Boolean)
    link_active = Column(Boolean)

    def __init__(self, user_id, username, father=None):
        self.user_id = user_id
        self.username = username
        self.father_id = father
        self.tasks_counter = self.subscribes_counter = self.total_referals = \
            self.redirect_counter = self.voicemsg_counter = self.total_balance = self.from_referals = \
            self.skipped_simple_post = self.skipped_ch = self.link_counter = self.skipped_links = \
            self.skipped_hard_post = self.simple_post_view = self.skipped_hard_post = self.hard_post_view = \
            self.subscribed_ch = self.step1_link_counter = self.step2_link_counter = self.step3_link_counter = \
            self.skipped_1step_links = self.skipped_2step_links = self.skipped_3step_links = 0
        self.ch_active = self.post_active = self.link_active = False


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


class Links(Base):
    __tablename__ = 'Links'
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


Base.metadata.create_all(engine)
