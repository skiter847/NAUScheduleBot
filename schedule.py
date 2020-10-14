from nauschedule import NAUScheduler
import texts
from datetime import datetime
from services import get_user_model, get_user_ids

nau = NAUScheduler()

DEPARTMENT_CODES = nau.get_department_codes()


def get_current_week():
    with open('current_week.txt') as f:
        return f.read()


def set_week():
    current_week = get_current_week()
    if current_week == '1':
        with open('current_week.txt', 'w') as f:
            f.write('2')
    else:
        with open('current_week.txt', 'w') as f:
            f.write('1')


def get_schedule_per_day(user, day):
    pairs = []
    schedule = nau.get_schedule(user.department_name, user.group_number, user.subgroup)
    for pair_num in range(1, 10):
        pair = schedule.get(f'{day}.{pair_num}')
        if pair is not None:
            pair.update({'num': pair_num, 'time': texts.PAIR_TIME[pair_num]})
            pairs.append(texts.pair_template(pair))
    return pairs


def send_pairs_for_users(bot, morning=False, evening=False):
    pairs = None
    user_ids = get_user_ids()
    for user_id in user_ids:
        bot.send_message(user_id,
                         f'{"Доброе утро, расписание на сегодня:" if morning else "Добрый вечер, расписание на завтра"}'
                         )
        user = get_user_model(user_id)
        if morning:
            pairs = get_today_schedule(user)
        elif evening:
            pairs = get_tomorrow_schedule(user)
        for pair in pairs:
            bot.send_message(user_id, pair)


def get_tomorrow_schedule(user):
    current_week = get_current_week()
    week_day = datetime.isoweekday(datetime.now())
    if week_day < 5:
        return get_schedule_per_day(user, f'{current_week}.{texts.DAY_NUMS[week_day + 1]}')


def get_today_schedule(user):
    current_week = get_current_week()
    week_day = datetime.isoweekday(datetime.now())
    if week_day < 5:
        return get_schedule_per_day(user, f'{current_week}.{texts.DAY_NUMS[week_day]}')
