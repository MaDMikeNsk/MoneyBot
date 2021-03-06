# BOT replays to User

# =====================================================================================================================
#                                              ОБЩИЕ ДЛЯ ВСЕХ
# =====================================================================================================================
def task_canceled():
    return '***Задание отменено***'

def task_not_active(task):
    if task == 'channel':
        return 'Задание "Подписка на телеграмм-канал" не активно!'
    elif task == 'post':
        return 'Задание "Просмотр поста" не активно!'
    elif task == 'link':
        return 'Задание "Переход по ссылке" не активно!'
    else:
        return '***ERROR***'

def no_next_task(task):
    if task == 'channel':
        return 'К сожалению, новых ТГ-каналов не найдено.\nВернитесь к заданию позже...'
    elif task == 'post':
        return 'К сожалению, для данной категории сложности ПОСТОВ больше нет.\nВернитесь к заданию позже...'
    elif task == 'link':
        return 'К сожалению, для данной категории сложности ССЫЛОК больше нет.\nВернитесь к заданию позже...'
    else:
        return '***ERROR***'
# =====================================================================================================================
#                                           ПОДПИСКА НА КАНАЛ
# =====================================================================================================================
def subscribe(title):
    return f"Подпишитесь на канал:\n👉 '{title}' 👈\nи получите вознаграждение!\n Награда - 2 балла"

# =====================================================================================================================
#                                              ПРОСМОТР ПОСТА
# =====================================================================================================================
def goto_post(title, bonus):
    return f"Перейдите к просмотру поста: \n👉 '{title}' 👈\nи получите вознаграждение. Награда - {bonus} балла"

# =====================================================================================================================
#                                              ПЕРЕХОД ПО ССЫЛКЕ
# =====================================================================================================================
def goto_link(bonus):
    return f"Перейдите по ССЫЛКЕ и получите вознаграждение {bonus} балла."
