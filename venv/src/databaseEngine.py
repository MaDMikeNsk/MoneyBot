from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dbItem import *
from src import config


class DatabaseEngine:
    def __init__(self): 
        self.engine = create_engine(config.DB_PATH, echo=True, connect_args={'check_same_thread': False})
        session = sessionmaker(bind=self.engine)
        self.session = session()

    # ==================================================================================================================
    #                                            ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ==================================================================================================================
    # IS USER IN DATABASE?
    def is_user_recorded(self, user_id):
        result = False
        for record in self.session.query(User).all():
            if record.user_id == user_id:
                result = True
        return result

    # ==================================================================================================================
    #                                            ADD TO DATABASE
    # ==================================================================================================================
    def add_user(self, user):
        self.session.add(user)
        self.session.commit()

    def add_posts(self, *posts):
        for post in posts:
            self.session.add(post)
        self.session.commit()
    
    def add_channel(self, *channels):
        for ch in channels:
            self.session.add(ch)
        self.session.commit()

    def add_links(self, *links):
        for link in links:
            self.session.add(link)
        self.session.commit()

    # ==================================================================================================================
    #                                              BALANCE & BONUS
    # ==================================================================================================================
    def balance(self, user_id):
        if self.is_user_recorded(user_id):
            for user in self.session.query(User).filter(User.user_id == user_id).all():
                text = f'Мой id: {user.user_id}\n' + \
                   '================================\n' + \
                   f'Выполнено заданий: {user.tasks_counter}\n' + \
                   f'Сделано подписок: {user.subscribes_counter}\n' + \
                   f'Просмотрено постов: {user.simple_post_view + user.hard_post_view}\n' + \
                   f'Пропущено постов: {user.skipped_simple_post + user.skipped_hard_post}\n' + \
                   f'Пропущено тг-каналов: {user.skipped_ch}\n' + \
                   f'Приглашено пользователей: {user.total_referals}\n' + \
                   f'Переходов по ссылкам: {user.redirect_counter}\n' + \
                   f'Отправлено голосовых сообщений: {user.voicemsg_counter}\n' + \
                   f'================================\n' + \
                   f'Общее количество баллов: {user.total_balance}\n' + \
                   f'В том числе от рефералов: {user.from_referals}'
            return text
        else:
            text = f"Произошла ошибка. Нажмите команду /start для начала работы"
            return text

    def record_bonus(self, user_id, bonus):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            user.total_balance += bonus
        self.session.commit()

    # ==================================================================================================================
    #                                           ПОДПИСКА НА КАНАЛ
    # ==================================================================================================================
    def get_next_channel(self, user_id) -> dict:
        res = {'available': False,
               'ch_info': {'ch_id': 0,
                           'chat_name': '',
                           'ch_title': '',
                           'ch_link': ''}}
        index = 0
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            index = user.subscribed_ch + user.skipped_ch

        for ch in self.session.query(Channels).all():
            if ch.id == index + 1:
                res['available'] = True
                res['ch_info']['ch_id'] = ch.id
                res['ch_info']['chat_name'] = ch.chat_name
                res['ch_info']['ch_title'] = ch.title
                res['ch_info']['ch_link'] = ch.link
                break
        return res

    def inc_ch_skip(self, user_id):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            user.skipped_ch += 1
        self.session.commit()

    # ==================================================================================================================
    #                                           ПРОСМОТР ПОСТОВ
    # ==================================================================================================================
    def get_post_description(self, post_id, complexity):
        if complexity == 'simple':
            table = Posts_Simple
        else:
            table = Posts_Hard

        for post in self.session.query(table).filter(table.id == post_id).all():
            text = f'Время на выполнение - {post.time} с'
        return text

    def inc_postview(self, user_id, complexity):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            if complexity == 'simple':
                user.simple_post_view += 1
            elif complexity == 'hard':
                user.hard_post_view += 1
        self.session.commit()
            
    def inc_post_skip(self, user_id, complexity):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            if complexity == 'simple':
                user.skipped_simple_post += 1
            elif complexity == 'hard':
                user.skipped_hard_post += 1
        self.session.commit()

    def inc_1step_link_skip(self, user_id):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            user.skipped_1step_links += 1
        self.session.commit()

    def inc_step1_linkview(self, user_id):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            user.step1_link_counter += 1
        self.session.commit()

    def get_next_post(self, user_id, complexity)->dict:
        res  = {'available': False,
                'post_info': {'post_id': None,
                              'post_title': '',
                              'post_url' : '',
                              'post_complexity': '',
                              'post_bonus': 0,
                              'post_time': 0,
                              'start_time': None}}
        index = 0
        # Ищем посты в зависимости от сложности
        if complexity == 'simple':
            # Получаем номер текущего поста в зависимости от кол-ва просмотров и пропусков
            for user in self.session.query(User).filter(User.user_id == user_id).all():
                index = user.simple_post_view + user.skipped_simple_post
                table = Posts_Simple
        elif complexity == 'hard':
            # Получаем номер текущего поста в зависимости от кол-ва просмотров и пропусков
            for user in self.session.query(User).filter(User.user_id == user_id).all():
                index = user.hard_post_view + user.skipped_hard_post
                table = Posts_Hard
            
        for post in self.session.query(table).all():
            if post.id == index + 1:
                res['available'] = True
                res['post_info']['post_id'] = post.id
                res['post_info']['post_title'] = post.title
                res['post_info']['post_url'] = post.link
                res['post_info']['post_complexity'] = complexity
                res['post_info']['post_bonus'] = post.bonus
                res['post_info']['post_time'] = post.time
                break
        return res

    # ==================================================================================================================
    #                                           ПРОСМОТР ССЫЛОК
    # ==================================================================================================================
    def get_next_simple_link(self, user_id):
        res = {'available': False,
               'link_info': {'link_id': 0,
                             'link_title': '',
                             'link_url': '',
                             'link_bonus':0,
                             'link_time': 0,
                             'start_time': None}}
        index = 0
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            index = user.step1_link_counter + user.skipped_1step_links

        for link in self.session.query(Links_Simple).all():
            if link.id == index + 1:
                res['available'] = True
                res['link_info']['link_id'] = link.id
                res['link_info']['link_title'] = link.title
                res['link_info']['link_url'] = link.link
                res['link_info']['link_bonus'] = link.bonus
                res['link_info']['link_time'] = link.time
                break
        return res

            