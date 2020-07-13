from telebot import types

# Reply keyboard
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_task = types.KeyboardButton('📋 Задание')
    btn_partner = types.KeyboardButton('👥 Партнёрская программа')
    btn_balance = types.KeyboardButton('💰 Баланс')
    btn_about = types.KeyboardButton('📚 О боте')
    markup.add(btn_task, btn_partner, btn_balance, btn_about)
    return markup

def tasks_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_subscribe = types.InlineKeyboardButton(text='Подписка на телеграмм-канал', callback_data='subscribe')
    btn_postlook = types.InlineKeyboardButton(text='Просмотр поста', callback_data='postview')
    btn_clicklink = types.InlineKeyboardButton(text='Переход по ссылке', callback_data='clicklink')
    btn_voicemsg = types.InlineKeyboardButton(text='Отправить голосовое сообщение', callback_data='voicemsg')
    markup.add(btn_subscribe, btn_postlook, btn_clicklink, btn_voicemsg)
    return markup

def task_subscribe_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='Перейти к каналу',url=url)
    btn_check = types.InlineKeyboardButton(text='Проверить подписку/получить награду', callback_data='get_tg_bonus')
    btn_skip = types.InlineKeyboardButton(text='Пропустить канал', callback_data='skip_ch')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_ch')
    markup.add(btn_task, btn_check, btn_skip, btn_cancel)
    return markup

def postview_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='🔗 Ссылка на пост', url=url)
    btn_check = types.InlineKeyboardButton(text='🕑 Получить награду', callback_data='get_post_bonus')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_post')
    markup.add(btn_task, btn_check, btn_cancel)
    return markup

def posttask_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='Перейти к просмотру поста', callback_data='goto_post')
    btn_skip = types.InlineKeyboardButton(text='Пропустить', callback_data='skip_post')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_post')
    markup.add(btn_task, btn_skip, btn_cancel)
    return markup

def postview_amount_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Простое', callback_data='simple')
    btn_2 = types.InlineKeyboardButton(text='Сложное', callback_data='hard')
    markup.add(btn_1, btn_2)
    return markup

def linktask_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='Ссылка', callback_data='task_clicklink', url=url)
    btn_check = types.InlineKeyboardButton(text='Получить награду', callback_data='get_link_bonus')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_link')
    markup.add(btn_task, btn_check, btn_cancel)
    return markup

def clicklink_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_1 = types.InlineKeyboardButton(text='🔗 Ссылка на пост', url=url)
    markup.add(btn_1)
    return markup
