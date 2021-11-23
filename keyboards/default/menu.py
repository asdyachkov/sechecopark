import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

now = datetime.datetime.now()

month = ['Январь',
         'Февраль',
         'Март',
         'Апрель',
         'Май',
         'Июнь',
         'Июль',
         'Август',
         'Сентябрь',
         'Октябрь',
         'Ноябрь',
         'Декабрь']
nowi = int(now.month)
sixmonth = []
for i in range(4):
    q = i + nowi
    if q >= 12:
        q -= 12
    sixmonth.append(month[q - 1])
keyb2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=sixmonth[0]), KeyboardButton(text=sixmonth[1])
        ],
        [
            KeyboardButton(text=sixmonth[2]), KeyboardButton(text=sixmonth[3])
        ],
        [
            KeyboardButton(text='Назад')
        ],
    ],
    resize_keyboard=True
)
keyb0 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Зарегестрироваться на посещение'), KeyboardButton(text='Отменить запись')
        ]
    ],
    resize_keyboard=True
)
keyb1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выбрать другой месяц')
        ]
    ],
    resize_keyboard=True
)
keyb3 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выбрать другое время')
        ]
    ],
    resize_keyboard=True
)
keyb4 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать запись'), KeyboardButton(text='Изменить комментарий')
        ],
    ],
    resize_keyboard=True
)
keyb5 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)
keyb6 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отменить запись'), KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)
