from telebot import types

# Глвное меню
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_task = types.KeyboardButton('📋 Задание')
    btn_partner = types.KeyboardButton('👥 Партнёрская программа')
    btn_balance = types.KeyboardButton('💰 Баланс')
    btn_promo = types.KeyboardButton('🚀 Продвижение')
    btn_game = types.KeyboardButton('🎮 Игры')
    btn_about = types.KeyboardButton('📚 О боте')
    markup.add(btn_task, btn_partner, btn_promo, btn_game, btn_balance, btn_about)
    return markup

# Кнопка "Баланс"
def balance_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('💳 Пополнить', callback_data='debit')
    btn_2 = types.InlineKeyboardButton('💲 Вывести', callback_data='credit')
    btn_3 = types.InlineKeyboardButton('⚖ Конвертировать', callback_data='convert')
    markup.add(btn_1, btn_2, btn_3)
    return markup

# Кнопка "Задание"
def tasks_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_subscribe = types.InlineKeyboardButton(text='👥 Подписки и лайки', callback_data='subscribe')
    btn_postlook = types.InlineKeyboardButton(text='👁 Просмотр поста', callback_data='postview')
    btn_clicklink = types.InlineKeyboardButton(text='⭐ Посмотреть контент', callback_data='clicklink')
    btn_voicemsg = types.InlineKeyboardButton(text='📢 Пройти опрос', callback_data='voicemsg')
    btn_promotion = types.InlineKeyboardButton(text='🏆 ТОП заданий', callback_data='top_tasks')
    markup.add(btn_subscribe, btn_postlook, btn_clicklink, btn_voicemsg, btn_promotion)
    return markup

# Кнопка "Подписки и лайки"
def task_subscribe_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='Перейти к каналу',url=url)
    btn_check = types.InlineKeyboardButton(text='Проверить подписку/получить награду', callback_data='get_tg_bonus')
    btn_skip = types.InlineKeyboardButton(text='Пропустить канал', callback_data='skip_ch')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_ch')
    markup.add(btn_task, btn_check, btn_skip, btn_cancel)
    return markup

# Кнопка "Перейти к просмотру поста"
def postview_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='🔗 Ссылка на пост', url=url)
    btn_check = types.InlineKeyboardButton(text='🕑 Получить награду', callback_data='get_post_bonus')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_post')
    markup.add(btn_task, btn_check, btn_cancel)
    return markup

# Кнопка "Просмотр поста"
def posttask_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='Перейти к просмотру поста', callback_data='goto_post')
    btn_skip = types.InlineKeyboardButton(text='Пропустить', callback_data='skip_post')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_post')
    markup.add(btn_task, btn_skip, btn_cancel)
    return markup

# Выбор сложности задания
def postview_amount_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Простое', callback_data='simple')
    btn_2 = types.InlineKeyboardButton(text='Сложное', callback_data='hard')
    markup.add(btn_1, btn_2)
    return markup

# Кнопка "Посмотреть контент"
def linktask_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_task = types.InlineKeyboardButton(text='Ссылка', callback_data='task_clicklink', url=url)
    btn_check = types.InlineKeyboardButton(text='Получить награду', callback_data='get_link_bonus')
    btn_cancel = types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_link')
    markup.add(btn_task, btn_check, btn_cancel)
    return markup

# Кнопка "Ссылка на пост"
def clicklink_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_1 = types.InlineKeyboardButton(text='🔗 Ссылка на пост', url=url)
    markup.add(btn_1)
    return markup

# Кнопка "Продвижение"
def promotion_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Telegram', callback_data='tg_promo')
    btn_2 = types.InlineKeyboardButton(text='Instagram', callback_data='insta_promo')
    btn_3 = types.InlineKeyboardButton(text='Youtube', callback_data='youtube_promo')
    btn_4 = types.InlineKeyboardButton(text='VK', callback_data='vk_promo')
    btn_5 = types.InlineKeyboardButton(text='Приложение в Google Play', callback_data='google_promo')
    btn_6 = types.InlineKeyboardButton(text='Приложение в App Store', callback_data='appstore_promo')
    btn_7 = types.InlineKeyboardButton(text='Создать опрос', callback_data='create_quiz')
    btn_8 = types.InlineKeyboardButton(text='Создать задание', callback_data='create_task')
    markup.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8)
    return markup

def tg_promo_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Пост', callback_data='tg_promo_post')
    btn_2 = types.InlineKeyboardButton(text='Канал', callback_data='tg_promo_ch')
    btn_3 = types.InlineKeyboardButton(text='Бота', callback_data='tg_promo_bot')
    btn_4 = types.InlineKeyboardButton(text='Группу', callback_data='tg_promo_group')
    btn_5 = types.InlineKeyboardButton(text='Расширенное задание', callback_data='tg_promo_advanced')
    markup.add(btn_1, btn_2, btn_3, btn_4, btn_5)
    return markup

def insta_promo_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Подписчики', callback_data='insta_promo_subs')
    btn_2 = types.InlineKeyboardButton(text='Лайки', callback_data='insta_promo_likes')
    markup.add(btn_1, btn_2)
    return markup

def youtube_promo_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Подписчики', callback_data='youtube_promo_subs')
    btn_2 = types.InlineKeyboardButton(text='Лайки', callback_data='youtube_promo_likes')
    btn_3 = types.InlineKeyboardButton(text='Просмотры', callback_data='youtube_promo_views')
    markup.add(btn_1, btn_2, btn_3)
    return markup

def vk_promo_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Друзья', callback_data='vk_promo_friends')
    btn_2 = types.InlineKeyboardButton(text='Лайки', callback_data='vk_promo_likes')
    btn_3 = types.InlineKeyboardButton(text='Подписчики', callback_data='vk_promo_subs')
    markup.add(btn_1, btn_2, btn_3)
    return markup

def games_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_1 = types.InlineKeyboardButton(text='🍀 Лотерея 🍀', callback_data='game_lottery')
    btn_2 = types.InlineKeyboardButton(text='🔵 Ставки 🔴', callback_data='game_bet')
    btn_3 = types.InlineKeyboardButton(text='🎲 Рандомайзер 🎲', callback_data='game_randomizer')
    markup.add(btn_1, btn_2, btn_3)
    return markup