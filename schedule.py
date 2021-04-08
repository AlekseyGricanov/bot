import requests
from bs4 import BeautifulSoup
from constants import group_id, URL
from datetime import datetime

def is_time(s):
    try:
        datetime.strptime(str, '%H:%M')
        return True
    except ValueError:
        return False

def get_schedule(date, group, attempt = 0):
    date = date.format('DD.MM.YYYY')

    result = requests.post(URL, data = {
            'rtype': 1, 
            'group' : group_id[group],
            'datafrom' : date,
            'dataend' : date}
        )
    soup = BeautifulSoup(result.text, 'html.parser')

    if soup.get_text() == 'Информации для отображения отчета не обнаружено! Измените период.':
        return str(date[:5]) + ' нет занятий. Отдыхай :з'
        
    
    # Для удобства будем работать не со всем текстом, а с ячейками таблицы
    td_tags = soup.find_all('td') 
    td_tags = [tag.get_text() for tag in td_tags]

    # Первые две ячейки - ненужный текст
    td_tags = td_tags[2:]

    mid = len(td_tags) // 2
    # Первая половина ячеек - временной диапазон занятий
    time = td_tags[:mid]
    # Средний элемент - дата
    schedule = td_tags[mid] + '\n\n'
    # Вторая половина - название дисциплин
    subjects = td_tags[mid+1:]

    # Преобразовываем в красивую строковую форму
    for i in range(mid):
        schedule += '⏰ '
        schedule += time[i]
        schedule += '\t'
        if subjects[i] == '':
            schedule += 'Окно. Отдыхай :з'
        else:
            schedule += subjects[i]
        schedule += '\n\n'

    if not schedule:
        raise NameError('Empty schedule.')
    else:
        return schedule
