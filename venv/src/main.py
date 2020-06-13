import telebot
import keyboard as kb
import datetime as dt
import os
import webbrowser as wb
import pandas as pd
import csv

from src.databaseEngine import DatabaseEngine
from src.dbItem import *
from src.statement import Statement
from src import config

# Инициализация
bot = telebot.TeleBot(config.TOKEN)
db = DatabaseEngine()
statement = Statement()
# ============================================================
# TEST
test_post_1 = Posts_Simple(title='Первый тестовый пост', link='https://habr.com/ru/', 
                    bonus=2, time=15)
test_post_2 = Posts_Hard(title='Второй тестовый пост', link='https://habr.com/ru/company/lamptest/blog/505034/',
                    time=30, bonus=3)
test_post_3 = Posts_Simple(title='Учёные нашли клад',
                    link='https://iz.ru/843861/2019-02-09/v-astrakhanskoi-oblasti-uchenye-nashli-klad-na-meste-stolitcy-zolotoi-ordy',
                    bonus=2, time=20)
test_post_4 = Posts_Hard(title='Пираты напали на судно', link='https://ria.ru/20200226/1565204927.html', 
                    bonus=4, time=50)

test_channel_1 = Channels(chat_name='@rabynagalerah', title='Первый тестовый канал (Рабы галерные)', link='https://t.me/rabynagalerah')
test_channel_2 = Channels(chat_name='@devsp', title='Второй тестовый канал (Data Sciense)', link='https://t.me/devsp')

test_link_simple = Links_Simple(title='Первая простая ссылка', link='https://habr.com/ru/', time=15)
test_link_2_stage = Links_2_Stage(title='Первая 2-x факторная ссылка',
                                  link_1='https://habr.com/ru/',
                                  link_2='https://habr.com/ru/',
                                  time_1=15, time_2=20)
test_link_3_stage = Links_3_Stage(title='Первая 3-x факторная ссылка',
                                  link_1='https://habr.com/ru/',
                                  link_2='https://habr.com/ru/',
                                  link_3='https://habr.com/ru/',
                                  time_1=15, time_2=20, time_3=15)

#ТЕСТОВОЕ ДОБАВЛЕНИЕ ПОСТОВ И КАНАЛОВ В БАЗУ
# db.add_posts(test_post_1, test_post_2, test_post_3, test_post_4)
# db.add_channel(test_channel_1, test_channel_2)
# db.add_links(test_link_simple, test_link_2_stage, test_link_3_stage)
# TEST
# ============================================================



# Welcome!
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = 'Привет! Я Money_bot! Помогаю заработать...'
    bot.send_message(message.chat.id, text, reply_markup=kb.main_keyboard())
    if db.is_user_recorded(message.chat.id) == False:
        db.add_user(User(message.chat.id))

@bot.message_handler(commands=['import_channels'])
def welcome(message):
    text = 'Двайте загрузим новые задания. Выберите файл'
    bot.send_message(message.chat.id, text)

    # Метод для добавления новых каналов в базу
    @bot.message_handler(content_types=['document'])
    def import_ch_tasks(message):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = "C:/Python/PycharmProjects/MoneyBot/files/" + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        with open(src, 'rb') as new_file:
            df = pd.read_csv(src, sep=';')
            dict_dataframe = df.to_dict()
        titles = []
        links = []
        for key, value in dict_dataframe.items():
            if key == 'title':
                for k, v in value.items():
                    titles.append(v)
            elif key == 'link':
                for k, v in value.items():
                    links.append(v)
        data = list(zip(titles, links))  # Готовые пары данных (заголовок, ссылка)
        print(data)

        # Добавляем каналы в базу
        for ch in data:
            new_ch = Channels(ch[0], ch[1])
            db.add_channel(new_ch)
        bot.reply_to(message, "Новые каналы добавлены!")

# Обработчик нажатия кнопок главного меню
@bot.message_handler(content_types=["text"])
def buttons_reply(message):
    user_id = message.chat.id
    if message.text == '📋 Задание':
        text = 'Выберите способ заработка: 👇'
        bot.send_message(user_id, text, reply_markup=kb.tasks_keyboard())
    elif message.text == '👥 Партнёрская программа':
        text = 'В разработке'
        bot.send_message(user_id, text, reply_markup=kb.main_keyboard())
    elif message.text == '💼 Баланс':
        text = db.balance(user_id)
        bot.send_message(user_id, text, reply_markup=kb.main_keyboard())
    elif message.text == '📚 О боте':
        text = 'Данный бот создан для заработка в Телеграме. Используйте кнопки меню для работы с ботом.\n\n' + \
               'Разработчик - https://t.me/Mike_Menshikov'
        bot.send_message(user_id, text, reply_markup=kb.main_keyboard())
    else:
        text = 'Что вы хотите сделать? напишите /start чтобы перезагрузить меню'
        bot.send_message(user_id, text, reply_markup=kb.main_keyboard())

# Обработчик нажатия inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = call.message.chat.id
    # ==================================================================================================================
    #                                           ПОДПИСКА НА КАНАЛ
    # ==================================================================================================================
    if call.data == 'subscribe':
        ch = db.get_next_channel(user_id)
        if ch['available'] == True:
            statement.set_statement(ch=ch['ch_info'])
            print(statement.__dict__)
            text = f"Подпишитесь на канал '{ch['ch_info']['ch_title']}' и получите вознаграждение!\n Награда - 2 балла"
            bot.send_message(user_id, text, reply_markup=kb.task_subscribe_keyboard(ch['ch_info']['ch_link']))
        else:
            text = 'К сожалению, новых тг-каналов не найдено. Вернитесь к заданию позже'
            bot.send_message(user_id, text)
            statement.reset_statement(ch='zero')

    elif call.data == 'get_tg_bonus':
        if statement.is_channel_active():
            chat_id = statement.get_ch_info()['chat_name']
            print(f'User_id = {user_id}')
            print(f"Chat_name - {chat_id}")
            try:
                statuss = ['creator', 'administrator', 'member']
                st = bot.get_chat_member(chat_id=chat_id, user_id=call.message.from_user.id).status
                print(st)
                if st in statuss:
                    bot.send_message(user_id, 'Награда получена')
                    # db.record_bonus(user_id, 2)
                    # statement.reset_statement(ch='zero')
                else:
                    bot.send_message(user_id, f"Подпишитесь на канал {chat_id}")
            except Exception as e:
                bot.send_message(chat_id=user_id, text=f'Ошибка: {e}')
        else:
            text = 'Задание "Подписка на телеграмм-канал" не активно!\n Воспользуйтесь кнопками меню для выбора задания'
            bot.send_message(user_id, text)

    elif call.data == 'skip_ch':
        if statement.is_channel_active():
            bot.send_message(user_id, '***Channel skipped***')
            db.inc_ch_skip(user_id)
            ch = db.get_next_channel(user_id)
            if ch['available'] == True:
                statement.set_statement(ch=ch['ch_info'])
                text = f"Подпишитесь на канал '{ch['ch_info']['ch_title']}' и получите вознаграждение!\n " \
                       f"Награда - 2 балла"
                bot.send_message(user_id, text, reply_markup=kb.task_subscribe_keyboard(ch['ch_info']['ch_link']))
            else:
                text = 'К сожалению, новых тг-каналов не найдено. Вернитесь к заданию позже'
                bot.send_message(user_id, text)
                statement.reset_statement(ch='zero')
        else:
            text = 'Задание "Подписка на телеграмм-канал" не активно!\n Воспользуйтесь кнопками меню для выбора задания'
            bot.send_message(user_id, text)
        
    elif call.data == 'cancel_ch':
        if statement.is_channel_active():
            text = 'Задание отменено'
            bot.send_message(user_id, text)
            statement.reset_statement(ch='zero')
        else:
            text = 'Задание "Подписка на телеграмм-канал" не активно!\n Воспользуйтесь кнопками меню для выбора задания'
            bot.send_message(user_id, text)

    # ==================================================================================================================
    #                                               ПРОСМОТР ПОСТА
    # ==================================================================================================================
    elif call.data == 'postview':
        CHOOSE_DIFF = 'Выберите сложность задания:'
        bot.send_message(user_id, CHOOSE_DIFF, reply_markup=kb.postview_amount_keyboard())
        
        print(statement.__dict__)

    elif call.data == 'simple':
        post = db.get_next_post(user_id=user_id, complexity='simple')
        if post['available'] == True:
            statement.set_statement(post=post['post_info'])
            text = f"Перейдите к просмотру поста '{post['post_info']['post_title']}' и получите вознаграждение.\n" + \
                    f"Награда - {post['post_info']['post_bonus']} балла"
            bot.send_message(user_id, text, reply_markup=kb.posttask_keyboard())
        else:
            text = 'К сожалению, для данной категории сложности ПОСТОВ больше нет.\n' + \
                   'Вернитесь к заданию позже...'
            bot.send_message(user_id, text)
            statement.reset_statement(post='zero')

    elif call.data == 'hard':
        post = db.get_next_post(user_id=user_id, complexity='hard')
        if post['available'] == True:
            statement.set_statement(post=post['post_info'])
            text = f"Перейдите к просмотру поста '{post['post_info']['post_title']}' и получите вознаграждение.\n" + \
                   f"Награда - {post['post_info']['post_bonus']} балла"
            bot.send_message(user_id, text, reply_markup=kb.posttask_keyboard())
        else:
            text = 'К сожалению, для данной категории сложности ПОСТОВ больше нет.\n' + \
                   'Вернитесь к заданию позже...'
            bot.send_message(user_id, text)
            statement.reset_statement(post='zero')
    
    elif call.data == 'goto_post':
        if statement.is_post_active():
            statement.set_post_starttime(st=dt.datetime.now())
            text = db.get_post_description(post_id=statement.get_post_info()['post_id'],
                                    complexity=statement.get_post_info()['post_complexity'])
            bot.send_message(user_id, text, reply_markup=kb.postview_keyboard(statement.get_post_info()['post_url']))
        else:
            text = 'Задание "Просмотр ПОСТА" не активно'
            bot.send_message(user_id, text)
        
    elif call.data == 'get_post_bonus':
        if statement.is_post_active():
            post_time = dt.timedelta(seconds=statement.get_post_info()['post_time'])
            time = dt.datetime.now()
            post_info = statement.get_post_info()
            time_difference = time - post_info['start_time']
            if time_difference >= post_time:

                bonus = post_info['post_bonus']
                text = f"Награда в {bonus} балла получена!"
                db.record_bonus(user_id, bonus)
                db.inc_postview(user_id, complexity=post_info['post_complexity'])
                statement.reset_statement(post='zero')
                bot.send_message(user_id, text)
            else:
                text = f'Вернитесь к просмотру поста. Осталось {post_time - time_difference} c'
                bot.send_message(user_id, text)
        else:
            text = 'Задание "Просмотр поста" не активно'
            bot.send_message(user_id, text)
            
    elif call.data == 'skip_post':
        if statement.is_post_active():
            bot.send_message(user_id, '***Post skipped***')
            post = {'available': False}
            post_compl = statement.get_post_info()['post_complexity']
            if post_compl == 'simple':
                db.inc_post_skip(user_id, complexity='simple')
                post = db.get_next_post(user_id, complexity='simple')
            elif post_compl == 'hard':
                db.inc_post_skip(user_id, complexity='hard')
                post = db.get_next_post(user_id, complexity='hard')

            if post['available'] == True:
                statement.set_statement(post=post['post_info'])
                text = f"Перейдите к просмотру поста '{post['post_info']['post_title']}' и получите вознаграждение.\n" + \
                       f"Награда - {post['post_info']['post_bonus']} балла"
                bot.send_message(user_id, text, reply_markup=kb.posttask_keyboard())
            elif post['available'] == False:
                text = 'К сожалению, для данной категории сложности ПОСТОВ больше нет.\n' + \
                       'Вернитесь к заданию позже...'
                bot.send_message(user_id, text)
                statement.reset_statement(post='zero')
        else:
            text = 'Нет текущего задания'
            bot.send_message(user_id, text)

    elif call.data == 'cancel_post':
        if statement.is_post_active():
            text = '***Задание отменено***'
            bot.send_message(user_id, text)
            statement.reset_statement(post='zero')
        else:
            text = 'Нет текущего задания'
            bot.send_message(user_id, text)
    
    # ==================================================================================================================
    #                                             ПРИГЛАСИТЬ РЕФЕРАЛА
    # ==================================================================================================================
    elif call.data == 'invite':
        text = 'Пригласите на канал нового пользователя и получите вознаграждение 1 балл!\n' \
               '📩 Реферальная ссылка: https://t.me/Mo_Tele_bot'
        bot.send_message(user_id, text)

    # ==================================================================================================================
    #                                              ПЕРЕХОД ПО ССЫЛКЕ
    # ==================================================================================================================
    elif call.data == 'clicklink':
        text = 'Выберите сложность задания:'
        bot.send_message(user_id, text, reply_markup=kb.clicklink_amount_keyboard())

    elif call.data == 'link_simple':
        link = db.get_next_simple_link(user_id)

        if link['available'] == True:
            text = f"Перейдите по ССЫЛКЕ и получите вознаграждение {link['link_info']['link_bonus']} балла.\n "
            bot.send_message(user_id, text, reply_markup=kb.click_1_stage_link_keyboard())
            statement.set_statement(link=link['link_info'])
            print(statement.__dict__)
        else:
            text = 'К сожалению, для данной категории сложности ССЫЛОК больше нет.\n' + \
                   'Вернитесь к заданию позже...'
            bot.send_message(user_id, text)

    elif call.data == 'link_hard':
        pass

    elif call.data == 'goto_link':
        if statement.is_link_active():
            statement.set_1stage_link_starttime(st=dt.datetime.now())
            link_info = statement.get_link_info()
            text = f"Время на выполнение - {link_info['link_time']} сек"
            bot.send_message(user_id, text, reply_markup=kb.linktask_keyboard(url=link_info['link_url']))
        else:
            text = 'Нет текущего задания'
            bot.send_message(user_id, text)

    elif call.data == 'skip_link_simple':
        if statement.is_link_active():
            db.inc_1step_link_skip(user_id)
            link = db.get_next_simple_link(user_id)
            if link['available'] == True:
                text = f"Перейдите по ССЫЛКЕ и получите вознаграждение {link['link_info']['link_bonus']} балла.\n "
                bot.send_message(user_id, text, reply_markup=kb.click_1_stage_link_keyboard())
                statement.set_statement(link=link['link_info'])
            else:
                text = 'К сожалению, для данной категории сложности ССЫЛОК больше нет.\n' + \
                       'Вернитесь к заданию позже...'
                bot.send_message(user_id, text)
                statement.reset_statement(link='zero')
        else:
            text = 'Нет текущего задания'
            bot.send_message(user_id, text)

    elif call.data == 'cancel_link':
        if statement.is_link_active():
            text = '***Задание отменено***'
            bot.send_message(user_id, text)
            statement.reset_statement(link='zero')
        else:
            text = 'Нет текущего задания'
            bot.send_message(user_id, text)

    elif call.data == 'get_link_bonus':
        if statement.is_link_active():
            link_info = statement.get_link_info()
            link_time = dt.timedelta(seconds=link_info['link_time'])
            time_now = dt.datetime.now()
            time_difference = time_now - link_info['start_time']
            if time_difference >= link_time:
                bonus = link_info['link_bonus']
                text = f"Награда в {bonus} балла получена!"
                db.record_bonus(user_id, bonus)
                db.inc_step1_linkview(user_id)
                bot.send_message(user_id, text)
                statement.reset_statement(link='zero')
            else:
                text = f'Вернитесь к просмотру ССЫЛКИ. Осталось {link_time - time_difference} c'
                bot.send_message(user_id, text)
        else:
            text = 'Нет текущего задания'
            bot.send_message(user_id, text)
    
    # ==================================================================================================================
    #                                           ОТПРАВИТЬ ГОЛОСОВОЕ СООБЩЕНИЕ
    # ==================================================================================================================
    elif call.data == 'voicemsg':
        text = 'Запишите и отправьте голосовое сообщение.'
        bot.send_message(user_id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=5)
