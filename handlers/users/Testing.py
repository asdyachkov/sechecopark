import datetime

import psycopg2
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import DB_URI
from keyboards.default import keyb0, keyb2, keyb1, keyb3, keyb4
from loader import dp, bot
from states import Test

connect = psycopg2.connect(DB_URI, sslmode='require')
cursor = connect.cursor()

times = ['9:00',
         '10:00',
         '11:00',
         '12:00',
         '13:00',
         '14:00',
         '15:00',
         '16:00',
         '17:00',
         '18:00',
         '19:00',
         '20:00']
month_list = ['Январь',
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
              'Декабрь'
              ]
month_day = {'Январь': '31',
             'Февраль': '28',
             'Март': '31',
             'Апрель': '30',
             'Май': '31',
             'Июнь': '30',
             'Июль': '31',
             'Август': '31',
             'Сентябрь': '30',
             'Октябрь': '31',
             'Ноябрь': '30',
             'Декабрь': '31'
             }


def kolvo_dney(answer1, answer2):
    return int(month_day[answer1[1:-1]]) >= int(answer2[1:-1])


@dp.message_handler(Command('start'))
async def start_message(message: types.Message):
    await message.answer('Здравствуйте!\n'
                         'Данная программа предназначена для записи на занятия верховой ездой.\n'
                         'Нажмите на кнопку ниже, чтобы записаться.',
                         reply_markup=keyb0)


@dp.message_handler(text='Зарегестрироваться на посещение')
async def join_test(message: types.Message):
    await message.answer('Здравствуйте!\n'
                         'На какой месяц Вы бы хотели записаться?',
                         reply_markup=keyb2)
    await Test.Q1.set()


@dp.message_handler(text='Назад', state=Test.Q1)
async def join_teser(message: types.Message, state: FSMContext):
    await message.answer('Регистрация приостановлена.\n'
                         'Чтобы начать регистрацию заново, нажмите на кнопку ниже.',
                         reply_markup=keyb0)
    await state.reset_state()


@dp.message_handler(state=Test.Q1)
async def answer_q2(message: types.Message, state: FSMContext):
    month = "'" + str(message.text) + "'"
    if month[1:-1] in month_list:
        await state.update_data(answer1=month)
        await message.answer('Укажите число, когда Вы бы хотели к на приехать.\n'
                             '(Введите число с клавиатуры: например, 17)\n'
                             'Если Вы хотите выбрать другой месяц для посещения, нажмите кнопку ниже.',
                             reply_markup=keyb1)
        await Test.Q2.set()
    else:
        await message.answer('Кажется, месяц был указан неверно.\n'
                             'Попробуйте еще раз.')


@dp.message_handler(text='Выбрать другой месяц', state=Test.Q2)
async def join_teser666(message: types.Message):
    await message.answer('Выберите на какой месяц Вы бы хотели записаться.',
                         reply_markup=keyb2)
    await Test.Q1.set()


@dp.message_handler(state=Test.Q2)
async def vafhbvah(message: types.Message, state: FSMContext):
    date = "'" + str(message.text) + "'"
    data = await state.get_data()
    answer1 = data.get('answer1')
    answer2 = date
    if message.text != 'Время уже занято':
        if message.text.isdigit() and kolvo_dney(answer1, answer2):
            await state.update_data(answer2=date)
            now = datetime.datetime.now()
            if month_list[int(str(now)[5:7]) - 1] == answer1[1:-1] and int(message.text) < int(str(now)[8:10]):
                await message.answer('Кажется, этот день уже прошел.\n'
                                     'Выберите другой')
            elif month_list[int(str(now)[5:7]) - 1] == answer1[1:-1] and int(message.text) == int(str(now)[8:10]):
                await message.answer('На сегодня записаться не получится.\n'
                                     'Мы не уcпеем подготовить лошадку.\n'
                                     'Выберите, пожалуйста, другой день.')
            else:
                anus = []
                cursor.execute(f"SELECT time FROM Записи WHERE month = {answer1} and date = {answer2}")
                anus = cursor.fetchall()
                data = []
                if anus is not []:
                    for i in anus:
                        data.append(str(i)[2:-3:1])
                keyb1 = ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text=times[0] if times[0] not in data else 'Время уже занято'),
                            KeyboardButton(text=times[6] if times[6] not in data else 'Время уже занято')
                        ],
                        [
                            KeyboardButton(text=times[1] if times[1] not in data else 'Время уже занято'),
                            KeyboardButton(text=times[7] if times[7] not in data else 'Время уже занято')
                        ],
                        [
                            KeyboardButton(text=times[2] if times[2] not in data else 'Время уже занято'),
                            KeyboardButton(text=times[8] if times[8] not in data else 'Время уже занято')
                        ],
                        [
                            KeyboardButton(text=times[3] if times[3] not in data else 'Время уже занято'),
                            KeyboardButton(text=times[9] if times[9] not in data else 'Время уже занято')
                        ],
                        [
                            KeyboardButton(text=times[4] if times[4] not in data else 'Время уже занято'),
                            KeyboardButton(text=times[10] if times[10] not in data else 'Время уже занято')
                        ],
                        [
                            KeyboardButton(text=times[5] if times[5] not in data else 'Время уже занято'),
                            KeyboardButton(text=times[11] if times[11] not in data else 'Время уже занято')
                        ],
                        [
                            KeyboardButton(text='Назад')
                        ],
                    ],
                    resize_keyboard=True
                )
                await message.answer('Выберите удобное вам время.',
                                     reply_markup=keyb1)
                await Test.Q3.set()
        else:
            await message.answer('Кажется, Вы указали неправильную дату.\n'
                                 'Укажите число, когда Вы бы хотели к на приехать.\n'
                                 '(1 или 13 или, может, 24)')


@dp.message_handler(state=Test.Q3, text='Назад')
async def answer_q7(message: types.Message):
    await message.answer('Укажите число, когда Вы бы хотели к на приехать.\n'
                         '(Введите число с клавиатуры: например, 17)\n'
                         'Если Вы хотите выбрать другой месяц для посещения, нажмите кнопку ниже.',
                         reply_markup=keyb1)
    await Test.Q2.set()


@dp.message_handler(state=Test.Q3)
async def answer_q0(message: types.Message, state: FSMContext):
    await state.update_data(answer3=message.text)
    if message.text != 'Время уже занято' and message.text in times:
        if message.text != 'Назад':
            await message.answer('Скажите, Вы бы хотели записаться на тренировку'
                                 ' или на простую прогулку на лошади?\n'
                                 'И напишите, пожалуйста, Ваше имя, номер телефона и примерный вес человека,'
                                 ' который будет записан.\n'
                                 'Это важно для того, чтобы подобрать правильную лошадь.\n'
                                 '(Формат ответа свободный, все ответы укажите в одном сообщении.)\n'
                                 'Если хотите изменить выбранное время, нажмите на кнопку ниже.',
                                 reply_markup=keyb3)
            await Test.Q4.set()


@dp.message_handler(state=Test.Q4, text='Выбрать другое время')
async def quywivfcq(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get('answer1')
    answer2 = data.get('answer2')
    anus = []
    cursor.execute(f"SELECT time FROM Записи WHERE month = {answer1} and date = {answer2}")
    anus = cursor.fetchall()
    data = []
    if anus is not []:
        for i in anus:
            data.append(str(i)[2:-3:1])
    keyb1 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=times[0] if times[0] not in data else 'Время уже занято'),
                KeyboardButton(text=times[6] if times[6] not in data else 'Время уже занято')
            ],
            [
                KeyboardButton(text=times[1] if times[1] not in data else 'Время уже занято'),
                KeyboardButton(text=times[7] if times[7] not in data else 'Время уже занято')
            ],
            [
                KeyboardButton(text=times[2] if times[2] not in data else 'Время уже занято'),
                KeyboardButton(text=times[8] if times[8] not in data else 'Время уже занято')
            ],
            [
                KeyboardButton(text=times[3] if times[3] not in data else 'Время уже занято'),
                KeyboardButton(text=times[9] if times[9] not in data else 'Время уже занято')
            ],
            [
                KeyboardButton(text=times[4] if times[4] not in data else 'Время уже занято'),
                KeyboardButton(text=times[10] if times[10] not in data else 'Время уже занято')
            ],
            [
                KeyboardButton(text=times[5] if times[5] not in data else 'Время уже занято'),
                KeyboardButton(text=times[11] if times[11] not in data else 'Время уже занято')
            ],
            [
                KeyboardButton(text='Назад')
            ],
        ],
        resize_keyboard=True
    )
    await message.answer('Выберите удобное вам время.',
                         reply_markup=keyb1)
    await Test.Q3.set()


@dp.message_handler(state=Test.Q4)
async def answer_q9999(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer=answer)
    data = await state.get_data()
    answer1 = data.get('answer1')
    answer2 = data.get('answer2')
    answer3 = data.get('answer3')
    await message.answer('Проверьте правильность введенных данных:\n'
                         f'Запись на {answer1[1:-1]}, {answer2[1:-1]} число, {answer3}\n'
                         f'Ваш комментарий к записи:\n'
                         f'{answer}',
                         reply_markup=keyb4)
    await Test.Q5.set()


@dp.message_handler(state=Test.Q5, text='Изменить комментарий')
async def answer_q999(message: types.Message):
    if message.text != 'Назад':
        await message.answer('Скажите, Вы бы хотели записаться на тренировку'
                             ' или на простую прогулку на лошади?\n'
                             'И напишите, пожалуйста, Ваше имя, номер телефона и примерный вес человека,'
                             ' который будет записан.\n'
                             'Это важно для того, чтобы подобрать правильную лошадь.\n'
                             '(Формат ответа свободный, все ответы укажите в одном сообщении.)\n'
                             'Если хотите изменить выбранное время, нажмите на кнопку ниже.',
                             reply_markup=keyb3)
        await Test.Q4.set()


@dp.message_handler(state=Test.Q5, text='Создать запись')
async def answer_q99(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer = data.get('answer')
    answer1 = data.get('answer1')
    answer2 = data.get('answer2')
    answer3 = data.get('answer3')
    cursor.execute(f"INSERT INTO Записи VALUES(%s, %s, %s)", (answer1[1:-1], answer2[1:-1], answer3))
    connect.commit()
    await message.answer("Спасибо, регистрация завершена.\n"
                         "С нетерпением ждем встречи!\n"
                         "Если Вы захотите отменить запись, то свяжитесь с нами через инстаграм.",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await bot.send_message(chat_id='961406924',
                           text=f'Новая запись на {answer1[1:-1]}, {answer2[1:-1]} число, {answer3} часов.\n'
                                f'Комментарий посетителя: {answer}')
    await bot.send_message(chat_id='518091887',
                           text=f'Новая запись на {answer1[1:-1]}, {answer2[1:-1]} число, {answer3} часов.\n'
                                f'Комментарий посетителя: {answer}')


@dp.message_handler()
async def start_message(message: types.Message):
    await message.answer('Я не знаю как на такое отвечать...\n'
                         'Напишите /start для начала моей работы, и я расскажу вам, что умею.',
                         reply_markup=types.ReplyKeyboardRemove())
