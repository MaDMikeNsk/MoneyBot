import telebot
import keyboard as kb
import datetime as dt
import os
import pandas as pd
import csv
import src.replays as rp

from src.databaseEngine import DatabaseEngine
from src.dbItem import *
from src.config import TOKEN

# Инициализация
bot = telebot.TeleBot(TOKEN)
db = DatabaseEngine()
statement = {}

# ============================================================
# TEST
@bot.message_handler(commands=['test_code'])
def test_code(message):
    print(message.chat.id)
    member = bot.get_chat_member(chat_id='@kodogolik', user_id=message.chat.id)
    # username = get_username(chat_id=message.from_user.id, user_id=message.chat.id)
    print(member.__dict__)
# TEST
# ============================================================

def get_username(chat_id, user_id):
    member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)

    if member.user.__dict__['username']:
        username = '@' + member.user.__dict__['username']
    elif member.user.__dict__['first_name']:
        if member.user.__dict__['last_name']:
            username = member.user.__dict__['first_name'] + ' ' + member.user.__dict__['last_name']
        else:
            username = member.user.__dict__['first_name']
    elif member.user.__dict__['last_name']:
        username = member.user.__dict__['last_name']
    else:
        username = 'Noname'
    return username

# Welcome!
@bot.message_handler(commands=['start'])
def send_welcome(message):
    commands = message.text.split(' ')
    user_id = message.chat.id
    text = '🖐 Привет! Я MoneyBot! Помогаю заработать...'
    username = get_username(chat_id=message.from_user.id, user_id=user_id)

    if len(commands) < 2:
        if db.is_user_recorded(user_id) == False:
            db.add_to_db(User(user_id, username))
    else:
        father_id = int(commands[1])
        father_name = db.get_username(father_id)

        if father_id != user_id and db.is_user_recorded(user_id) == False:
            reply = f"Вас пригласил пользователь с ником {father_name}"
            bot.send_message(user_id, reply)
            db.add_to_db(User(user_id, username, father=father_id))
            db.record_bonus(user_id=father_id, bonus=1, new_referal=True)
    bot.send_message(user_id, text, reply_markup=kb.main_keyboard())

@bot.message_handler(commands=['import_task'])
def import_task(message):
    text = 'Двайте загрузим новые задания. Выберите файл'
    bot.send_message(message.chat.id, text)

    # Обработчик сообщений, содержащих документ с tasks
    @bot.message_handler(content_types=['document'])
    def handle_csv_doc(message):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = "temp/" + message.document.file_name
        print(message.document.file_name)

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        try:
            with open(src, 'rb') as new_file:
                df = pd.read_csv(src, sep=';', encoding='utf-8')
                dict_dataframe = df.to_dict('split')

                if 'channels' in message.document.file_name:
                    for row in dict_dataframe['data']:
                        db.add_to_db(Channels(chat_name='@' + row[0], title=row[1], link=row[2]))
                    bot.reply_to(message, "Новые каналы добавлены!")

                elif 'posts' in message.document.file_name:
                    for row in dict_dataframe['data']:
                        bonus = row[2]
                        if bonus > 2:
                            db.add_to_db(Posts_Hard(title=row[0], link=row[1], bonus=bonus, time=row[3]))
                        else:
                            db.add_to_db(Posts_Simple(title=row[0], link=row[1], bonus=bonus, time=row[3]))
                    bot.reply_to(message, "Новые посты добавлены!")

        except Exception as e:
            text = f"***ОШИБКА: {e} *** Неверный формат файла.\n" \
                   "Доступные имена файлов:\n" \
                   "\tchannels.csv\n" \
                   "\tposts.csv"
            bot.reply_to(message, text)
        os.remove(src)

# Обработчик нажатия кнопок главного меню
@bot.message_handler(content_types=["text"])
def buttons_reply(message):
    user_id = message.chat.id
    if db.is_user_recorded(user_id=user_id):
        if message.text == '📋 Задание':
            text = 'Выберите способ заработка: 👇'
            bot.send_message(user_id, text, reply_markup=kb.tasks_keyboard())

        elif message.text == '💰 Баланс':
            text = db.balance(user_id)
            bot.send_message(user_id, text, reply_markup=kb.main_keyboard())

        elif message.text == '👥 Партнёрская программа':
            text = '📢 Пригласите на канал нового пользователя и получите вознаграждение 1 балл!\n' \
                   'За каждое выполненное им задание вы также получаете награду!\n' \
                   '📩 Реферальная ссылка: https://t.me/Mo_Tele_bot?start=' + str(user_id)
            bot.send_message(user_id, text, reply_markup=kb.main_keyboard())

        elif message.text == '📚 О боте':
            text = 'Данный бот создан для заработка в Телеграме. Используйте кнопки меню для работы с ботом.\n\n' \
                    '🛠 Разработчик - @Mike_Menshikov'
            bot.send_message(user_id, text, reply_markup=kb.main_keyboard())

    else:
        text = 'Вас нет в базе данных. Нажмите /start для начала работы с ботом.'
        bot.send_message(user_id, text)


# Обработчик нажатия inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = call.message.chat.id
    global statement
    # ==================================================================================================================
    #                                           ПОДПИСКА НА КАНАЛ
    # ==================================================================================================================
    if call.data == 'subscribe':
        ch = db.get_next_channel(user_id)
        if ch['available'] == True:
            db.activate_ch(user_id, True)
            ch_title = bot.get_chat(chat_id=ch['ch_info']['chat_name']).title
            text = rp.subscribe(ch_title)
            bot.send_message(user_id, text, reply_markup=kb.task_subscribe_keyboard(ch['ch_info']['ch_link']))
        else:
            text = rp.no_next_task(task='channel')
            bot.send_message(user_id, text)
            db.activate_ch(user_id, False)

    elif call.data == 'get_tg_bonus':
        if db.is_ch_active(user_id):
            ch = db.get_next_channel(user_id)
            chat_id = ch['ch_info']['chat_name']
            user_id = call.from_user.id
            print(f'User_id = {user_id}')
            print(f"Chat_name - {chat_id}")
            try:
                statuss = ['creator', 'administrator', 'member']
                st = bot.get_chat_member(chat_id=chat_id, user_id=user_id).status
                print(f"User status - {st}")
                if st in statuss:
                    bot.send_message(user_id, 'Награда получена')
                    db.record_bonus(user_id, 2)
                    db.activate_ch(user_id, False)
                else:
                    bot.send_message(user_id, f"Подпишитесь на канал {chat_id}")
            except Exception as e:
                bot.send_message(chat_id=user_id, text=f'Ошибка: {e}')
        else:
            text = rp.task_not_active(task='channel')
            bot.send_message(user_id, text)

    elif call.data == 'skip_ch':
        if db.is_ch_active(user_id):
            bot.send_message(user_id, '***Channel skipped***')
            db.inc_ch_skip(user_id)
            ch = db.get_next_channel(user_id)
            if ch['available'] == True:
                text = rp.subscribe(ch['ch_info']['ch_title'])
                bot.send_message(user_id, text, reply_markup=kb.task_subscribe_keyboard(ch['ch_info']['ch_link']))
            else:
                text = rp.no_next_task(task='channel')
                bot.send_message(user_id, text)
                db.activate_ch(user_id, False)
        else:
            text = rp.task_not_active(task='channel')
            bot.send_message(user_id, text)
        
    elif call.data == 'cancel_ch':
        if db.is_ch_active(user_id):
            text = rp.task_canceled()
            bot.send_message(user_id, text)
            db.activate_ch(user_id, False)
        else:
            text = rp.task_not_active(task='channel')
            bot.send_message(user_id, text)

    # ==================================================================================================================
    #                                               ПРОСМОТР ПОСТА
    # ==================================================================================================================
    elif call.data == 'postview':
        CHOOSE_DIFF = 'Выберите сложность задания:'
        bot.send_message(user_id, CHOOSE_DIFF, reply_markup=kb.postview_amount_keyboard())

    elif call.data == 'simple':
        post = db.get_next_post(user_id=user_id, complexity='simple')
        if post['available'] == True:
            db.activate_post(user_id, True)
            statement = {str(user_id):{'post_complexity': 'simple'}}
            print(statement)
            text = rp.goto_post(title=post['post_info']['post_title'], bonus=post['post_info']['post_bonus'])
            bot.send_message(user_id, text, reply_markup=kb.posttask_keyboard())
        else:
            text = rp.no_next_task(task='post')
            bot.send_message(user_id, text)
            db.activate_post(user_id, False)

    elif call.data == 'hard':
        post = db.get_next_post(user_id=user_id, complexity='hard')
        if post['available'] == True:
            db.activate_post(user_id, True)
            statement = {str(user_id):{'post_complexity': 'hard'}}
            text = rp.goto_post(title=post['post_info']['post_title'], bonus=post['post_info']['post_bonus'])
            bot.send_message(user_id, text, reply_markup=kb.posttask_keyboard())
        else:
            text = rp.no_next_task(task='post')
            bot.send_message(user_id, text)
            db.activate_post(user_id, False)
    
    elif call.data == 'goto_post':
        if db.is_post_active(user_id):
            statement[str(user_id)]['post_start_time'] =dt.datetime.now()
            print(statement)
            post = db.get_next_post(user_id, complexity=statement[str(user_id)]['post_complexity'])
            text = db.get_post_time(post_id=post['post_info']['post_id'],
                                    complexity=post['post_info']['post_complexity'])
            bot.send_message(user_id, text, reply_markup=kb.postview_keyboard(post['post_info']['post_url']))
        else:
            text = rp.task_not_active(task='post')
            bot.send_message(user_id, text)
        
    elif call.data == 'get_post_bonus':
        if db.is_post_active(user_id):
            post = db.get_next_post(user_id, complexity=statement[str(user_id)]['post_complexity'])
            post_time = dt.timedelta(seconds=post['post_info']['post_time'])
            time = dt.datetime.now()
            time_difference = time - statement[str(user_id)]['post_start_time']
            if time_difference >= post_time:
                bonus = post['post_info']['post_bonus']
                text = f"Награда в {bonus} балла получена!"
                db.record_bonus(user_id, bonus)
                db.inc_postview(user_id, complexity=statement[str(user_id)]['post_complexity'])
                db.activate_post(user_id, False)
                bot.send_message(user_id, text)
            else:
                rest_time = post_time - time_difference
                text = f"Вернитесь к просмотру поста. Осталось {str(rest_time).split('.')[0].split(':')[2]} cек"
                bot.send_message(user_id, text)
        else:
            text = rp.task_not_active(task='post')
            bot.send_message(user_id, text)
            
    elif call.data == 'skip_post':
        if db.is_post_active(user_id):
            bot.send_message(user_id, '***Post skipped***')
            post_compl = statement[str(user_id)]['post_complexity']
            if post_compl == 'simple':
                db.inc_post_skip(user_id, complexity='simple')
                post = db.get_next_post(user_id, complexity='simple')
            elif post_compl == 'hard':
                db.inc_post_skip(user_id, complexity='hard')
                post = db.get_next_post(user_id, complexity='hard')

            if post['available'] == True:
                text = rp.goto_post(title=post['post_info']['post_title'], bonus=post['post_info']['post_bonus'])
                bot.send_message(user_id, text, reply_markup=kb.posttask_keyboard())
            elif post['available'] == False:
                text = rp.no_next_task(task='post')
                bot.send_message(user_id, text)
                db.activate_post(user_id, False)
        else:
            text = rp.task_not_active(task='post')
            bot.send_message(user_id, text)

    elif call.data == 'cancel_post':
        if db.is_post_active(user_id):
            text = rp.task_canceled()
            bot.send_message(user_id, text)
            db.activate_post(user_id, False)
        else:
            text = rp.task_not_active(task='post')
            bot.send_message(user_id, text)

    # ==================================================================================================================
    #                                              ПЕРЕХОД ПО ССЫЛКЕ
    # ==================================================================================================================
    elif call.data == 'clicklink':
        url = 'https://www.google.com/'
        text = f'Перейдите по ссылке и введите уникальный код.\n' \
               f'Ваш код: {user_id}'
        bot.send_message(user_id, text, reply_markup=kb.clicklink_keyboard(url))


    # ==================================================================================================================
    #                                           ОТПРАВИТЬ ГОЛОСОВОЕ СООБЩЕНИЕ
    # ==================================================================================================================
    elif call.data == 'voicemsg':
        text = 'Запишите и отправьте голосовое сообщение.'
        bot.send_message(user_id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
