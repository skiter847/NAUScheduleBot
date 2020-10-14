import telebot
import texts
import keyboards
import schedule
import services
import time
from model import db, User
from apscheduler.schedulers.background import BackgroundScheduler

bot = telebot.TeleBot('1351639031:AAGbYDKNCdXQbSPCzvqpWTWQiQZNBRsnt8k')


def get_subgroup_step(message, dep_name, group_number, update=False):
    subgroup = message.text
    user_id = message.chat.id
    if update:
        user = services.get_user_model(user_id)
        user.department_name = dep_name
        user.group_number = group_number
        user.subgroup = subgroup
        user.save()
    else:
        User.create(id=user_id, department_name=dep_name, group_number=group_number, subgroup=subgroup)
    bot.send_message(message.chat.id, 'Выбирай', reply_markup=keyboards.dashboard())


def get_group_number_step(message, dep_name, update=False):
    group_number = message.text
    if schedule.nau.get_schedule(dep_name, group_number) == 'Не знайдено!':
        bot.send_message(message.chat.id, 'Группа не найдена, попробуйте еще раз')
        bot.register_next_step_handler(message, get_group_number_step, dep_name, update)
    else:
        bot.send_message(message.chat.id, 'Введите подгруппу')
        bot.register_next_step_handler(message, get_subgroup_step, dep_name, group_number, update)


def get_department_name_step(message, update=False):
    dep_name = message.text.upper()
    if schedule.DEPARTMENT_CODES.get(dep_name, None):
        bot.send_message(message.chat.id, 'Введите номер группы')
        bot.register_next_step_handler(message, get_group_number_step, dep_name, update)
    else:
        bot.send_message(message.chat.id, 'Факультет не найден, попробуйте еще раз')
        bot.register_next_step_handler(message, get_department_name_step, update)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    if services.user_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы', reply_markup=keyboards.dashboard())
    else:
        bot.send_message(message.chat.id, 'Введите название факультета')
        bot.send_message(message.chat.id, texts.DEPARTMENTS_LIST)
        bot.register_next_step_handler(message, get_department_name_step)


@bot.message_handler(commands=['8ndcvjvpk5i4'])
def admin_panel_handler(message):
    bot.send_message(message.chat.id, text='Админ панель', reply_markup=keyboards.admin_panel())


@bot.message_handler(func=lambda message: message.text == 'Изменить текущую неделю')
def set_current_week(message):
    schedule.set_week()
    bot.send_message(message.chat.id, 'Успешно')


@bot.message_handler(func=lambda message: message.text == 'Расписание звонков')
def call_schedule_handler(message):
    bot.send_message(message.chat.id, texts.CALL_SCHEDULE)


@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_handler(message):
    bot.send_message(message.chat.id, 'Выбирай', reply_markup=keyboards.dashboard())


@bot.message_handler(func=lambda message: message.text == 'На завтра')
def tomorrow_handler(message):
    user = services.get_user_model(message.chat.id)
    pairs = schedule.get_tomorrow_schedule(user)
    if pairs is not None:
        for pair in pairs:
            bot.send_message(user.id, pair)
    else:
        bot.send_message(user.id, 'Завтра выходной😌')


@bot.message_handler(func=lambda message: message.text == 'Жаловаться сюда')
def complain_handler(message):
    bot.send_message(message.chat.id, 'Все жалобы сюда - @pyPunisher')


@bot.message_handler(func=lambda message: message.text == 'На сегодня')
def tomorrow_handler(message):
    user = services.get_user_model(message.chat.id)
    pairs = schedule.get_today_schedule(user)
    if pairs is not None:
        for pair in pairs:
            bot.send_message(user.id, pair)
    else:
        bot.send_message(user.id, 'Сегодня выходной😌')


@bot.message_handler(func=lambda message: message.text == 'Текущая неделя')
def tomorrow_handler(message):
    bot.send_message(message.chat.id, schedule.get_current_week())


@bot.message_handler(func=lambda message: message.text == 'Расписание')
def schedule_days_handler(message):
    bot.send_message(message.chat.id, 'Выбирай', reply_markup=keyboards.schedule_days())


@bot.message_handler(func=lambda message: message.text == 'Крутить барабан')
def drum_handler(message):
    bot.send_message(message.chat.id, 'Кручу барабан...')
    time.sleep(1)
    bot.send_message(message.chat.id, 'Сегодня не твой день, пиздуй на пару!')


@bot.message_handler(func=lambda message: message.text == 'Настройки')
def settings_handler(message):
    bot.send_message(message.chat.id, 'Настройки', reply_markup=keyboards.settings())


@bot.message_handler(func=lambda message: message.text == 'Изменить факультет, группу и подгруппу')
def set_user_data_handler(message):
    bot.send_message(message.chat.id, 'Введите название факультета')
    bot.send_message(message.chat.id, texts.DEPARTMENTS_LIST)
    bot.register_next_step_handler(message, get_department_name_step, update=True)


@bot.message_handler(func=lambda message: message.text == 'Рассылка')
def subscribe_handler(message):
    bot.send_message(message.chat.id, 'В разработке')


@bot.message_handler(regexp=r'[1/2]\.\w{3}')
def schedule_day_handler(message):
    if len(message.text) == 5:
        user = services.get_user_model(message.chat.id)
        pairs = schedule.get_schedule_per_day(user, message.text)

        for pair in pairs:
            bot.send_message(user.id, pair)


if __name__ == '__main__':

    scheduler = BackgroundScheduler()

    if db.connect():
        db.create_tables([User])

    scheduler.add_job(schedule.send_pairs_for_users,
                      'cron',
                      day_of_week='0-5',
                      hour='06',
                      minute='30',
                      args=(bot,),
                      kwargs={'morning': True}
                      )
    scheduler.add_job(schedule.send_pairs_for_users,
                      'cron',
                      day_of_week='0-5',
                      hour='20',
                      minute='30',
                      args=(bot,),
                      kwargs={'evening': True}
                      )

    scheduler.start()

    while True:
        try:
            bot.polling()
        except Exception as e:
            print(e)
            time.sleep(13)
