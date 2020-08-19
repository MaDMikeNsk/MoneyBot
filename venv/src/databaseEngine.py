from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dbItem import *
from src.config import DB_PATH


class DatabaseEngine:
    def __init__(self): 
        self.engine = create_engine(DB_PATH, echo=True, connect_args={'check_same_thread': False})
        session = sessionmaker(bind=self.engine)
        self.session = session()

    # ==================================================================================================================
    #                                            ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ==================================================================================================================
    # IS USER IN DATABASE?
    def is_user_recorded(self, user_id):
        res = False
        for record in self.session.query(User).filter(User.user_id == user_id).all():
            res = True
        return res

    # RECORD TO DB
    def add_to_db(self, *args):
        for arg in args:
            self.session.add(arg)
        self.session.commit()

    def get_username(self, user_id):
        try:
            return self.session.query(User).filter(User.user_id == user_id).one().username
        except Exception as e:
            print(e)

    # ==================================================================================================================
    #                                              BALANCE & BONUS
    # ==================================================================================================================
    def balance(self, user_id):
        if self.is_user_recorded(user_id):
            for user in self.session.query(User).filter(User.user_id == user_id).all():
                text = f'Мой id: {user.user_id}\n' + \
                   '================================\n' + \
                   f'📝 Выполнено заданий: {user.tasks_counter}\n' + \
                   f'👥 Подписок на ТГ-каналы: {user.subscribes_counter}\n' + \
                   f'👁 Просмотрено постов: {user.simple_post_view + user.hard_post_view}\n' + \
                    f'🤖 Переходов по ссылкам: {user.redirect_counter}\n' + \
                    f'⭐️Выполнено квестов: {user.voicemsg_counter}\n' + \
                    f'👤 Приглашено пользователей: {user.total_referals}\n' + \
                   f'================================\n' + \
                   f'⚪: {user.total_silver}\n' + \
                    f'🟡: {user.total_gold}\n' + \
                    f'⚪ от рефералов: {user.from_referals}'
            return text
        else:
            text = f" Вас нет в базе данных. Нажмите команду /start для начала работы"
            return text

    def record_bonus(self, user_id, bonus=1, bonus_curr="silver", new_referal=False):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            # Бонус за нового пользователея (реферала)
            if new_referal:
                user.total_silver += 1
                user.from_referals += 1
                user.total_referals += 1
                break

            if bonus_curr == 'silver':
                user.total_silver += bonus
            elif bonus_curr == 'gold':
                user.total_gold += bonus

            # Накинем father 1 серебро (если есть)
            if user.father_id is not None:
                for usr in self.session.query(User).filter(User.user_id == user.father_id).all():
                    usr.total_silver += 1
                    usr.from_referals += 1

        self.session.commit()

    # ==================================================================================================================
    #                                           ПОДПИСКА НА КАНАЛ
    # ==================================================================================================================
    def is_ch_active(self, user_id):
        user = self.session.query(User).filter(User.user_id == user_id).one()
        return user.ch_active

    def activate_ch(self, user_id, active):
        user = self.session.query(User).filter(User.user_id == user_id).one()
        user.ch_active = active

    def get_next_channel(self, user_id) -> dict:
        res = {'available': False, 'ch_info': {}}
        user = self.session.query(User).filter(User.user_id == user_id).one()
        index = user.subscribed_ch + user.skipped_ch + 1

        try:
            ch = self.session.query(Channels).filter(Channels.id == index).one()
            res['available'] = True
            res['ch_info']['ch_id'] = ch.id
            res['ch_info']['chat_name'] = ch.chat_name
            res['ch_info']['ch_title'] = ch.title
            res['ch_info']['ch_link'] = ch.link
        except:
            pass
        return res

    def inc_ch_skip(self, user_id):
        user = self.session.query(User).filter(User.user_id == user_id).one()
        user.skipped_ch += 1
        self.session.commit()

    # ==================================================================================================================
    #                                           ПРОСМОТР ПОСТОВ
    # ==================================================================================================================
    def is_post_active(self, user_id):
        user = self.session.query(User).filter(User.user_id == user_id).one()
        return user.post_active

    def activate_post(self, user_id, active):
        user = self.session.query(User).filter(User.user_id == user_id).one()
        user.post_active = active

    def get_next_post(self, user_id, complexity) -> dict:
        res = {'available': False, 'post_info': {}}
        index = 0
        table = None

        # Ищем индекс поста в зависимости от сложности
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            if complexity == 'simple':
                index = user.simple_post_view + user.skipped_simple_post
                table = Posts_Simple
            elif complexity == 'hard':
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

    def get_post_time(self, post_id, complexity)-> str:
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

    # ==================================================================================================================
    #                                           ПРОСМОТР ССЫЛОК
    # ==================================================================================================================
    def get_next_simple_link(self, user_id):
        res = {'available': False,
               'link_info': {}}
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

    def inc_1step_link_skip(self, user_id):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            user.skipped_1step_links += 1
        self.session.commit()

    def inc_step1_linkview(self, user_id):
        for user in self.session.query(User).filter(User.user_id == user_id).all():
            user.step1_link_counter += 1
        self.session.commit()