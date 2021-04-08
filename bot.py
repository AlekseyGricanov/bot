import pendulum  
from pendulum.constants import MONDAY
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from db import *
from constants import *
from keyboard import get_keyboard
from schedule import get_schedule

def write_msg(user_id, text):
    vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id' : 0, 'keyboard' : get_keyboard()})

def send_week(user_id, fisrt_day):
    date = fisrt_day
    # Шестдиневное обучение
    for i in range(6):
        schedule = get_schedule(date, get_user_group(user_id))
        write_msg(user_id, schedule)
        date = date.add(days=1)

def handler(user_id, message):
    # Если пользователя нет в бд, нужно спросить группу
    if not exist(user_id):
        message = message.upper()
        # Если сообщение и есть номер группы, то записываем в бд
        if message in group_id:
            insert_new_user(user_id, message)
            write_msg(user_id, 'На какой день нужно расписание (сегодня/завтра)?')
        else:
            write_msg(user_id, 'Введи номер группы. Например: 103')
    else:
        message = message.lower()
        date = pendulum.today(TIME_ZONE)
        # Обрабатываем необычные сообщения (расписание не на один день)
        if message == "эта неделя":
            send_week(user_id, date.start_of('week'))
        elif message == "следующая неделя":
            send_week(user_id, date.next(MONDAY))
        elif message == "изменить группу":
            delete_user(user_id)
            write_msg(user_id, 'Какая группа?')
        else:
            if message == "завтра":
                date = pendulum.tomorrow(TIME_ZONE)
            elif message == "вчера":
                date = pendulum.yesterday(TIME_ZONE) 
            elif message in WEEK:
                if date.day_of_week != WEEK[message]:
                    date = date.next(WEEK[message])
            
            # В любом случае отправляем сообщение с расписанием
            schedule = get_schedule(date, get_user_group(user_id))
            write_msg(user_id, schedule)

vk_session = vk_api.VkApi(token=TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me: 
        try:
            handler(event.user_id, event.text)
        except Exception as e:
            write_msg(event.user_id, 'Что-то не так. Попробуй снова')
            error_text = "IT'S A MISTAKE:" + str(e)
            print(error_text)
            
