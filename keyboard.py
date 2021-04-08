import json

main_color = 'primary'

def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }

def get_keyboard():
    keyboard = {
        "one_time" : False,
        "buttons" : [
            [get_button('Сегодня', main_color), get_button('Завтра', main_color)],
            [get_button('Эта неделя', main_color), get_button('Следующая неделя', main_color)],
            [get_button('Изменить группу', 'secondary')]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard