from telebot import types
import texts


def dashboard():
    items = texts.DASHBOARD_ITEMS
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=2)
    for index in range(0, len(items) - 1, 2):
        markup.row(types.KeyboardButton(items[index]), types.KeyboardButton(items[index + 1]))
    return markup


def admin_panel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=2)
    items = texts.ADMIN_ITEMS
    for item in items:
        markup.add(item)
    return markup


def schedule_days():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=2)
    first_week = texts.SCHEDULE_DAYS[:5]
    second_week = texts.SCHEDULE_DAYS[5:]
    markup.row(*first_week)
    markup.row(*second_week)
    markup.row('Назад')

    return markup


def settings():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=2)
    items = texts.SETTING_ITEMS
    for item in items:
        markup.add(item)

    return markup
