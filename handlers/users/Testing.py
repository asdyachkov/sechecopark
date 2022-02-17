from datetime import date

from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from states import Test
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import keyb0
from keyboards.inline.callback_datas import month_callback, day_callback
from loader import dp, bot

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
month_day = {'Январь': 31,
             'Февраль': 28,
             'Март': 31,
             'Апрель': 30,
             'Май': 31,
             'Июнь': 30,
             'Июль': 31,
             'Август': 31,
             'Сентябрь': 30,
             'Октябрь': 31,
             'Ноябрь': 30,
             'Декабрь': 31
             }


@dp.message_handler(Command('start'))
async def start_message(message: types.Message):
    await message.answer('Здравствуйте! 🙂\n'
                         'Данная программа предназначена для аренды нашего домика в деревне. 🏡\n'
                         'Нажмите на кнопку ниже, чтобы записаться.',
                         reply_markup=keyb0)


@dp.message_handler(Command('cancel'), state=Test.Q6)
async def zapis_otmena(message: types.Message, state: FSMContext):
    await message.answer("Запись отменена 📛")
    await message.answer("Для создания новой записи напишите /start",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.callback_query_handler(text_contains="arend_True")
async def start_zapis(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    now = int(str(date.today())[5:7])-1
    keyb1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{month_list[now] if now<= 12 else month_list[now-12]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now] if now<= 12 else month_list[now-12]}")),
                InlineKeyboardButton(text=f"{month_list[now+1] if now+1<= 12 else month_list[now-11]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now+1] if now+1<= 12 else month_list[now-11]}"))
            ],
            [
                InlineKeyboardButton(text=f"{month_list[now+2] if now+2<= 12 else month_list[now-10]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now+2] if now+2<= 12 else month_list[now-10]}")),
                InlineKeyboardButton(text=f"{month_list[now+3] if now+3<= 12 else month_list[now-9]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now+3] if now+3<= 12 else month_list[now-9]}"))
            ],
            [
                InlineKeyboardButton(text="Назад ↩", callback_data="cancel")
            ]
        ]
    )
    await call.message.answer("Выберите месяц и число, когда Вы бы хотели к нам приехать 📅",
                              reply_markup=keyb1)
    await Test.Q2.set()


@dp.callback_query_handler(state=Test.Q2, text_contains="cancel")
async def tell_about(call: CallbackQuery, state: FSMContext):
    await call.answer("Запись отменена 📛", show_alert=True)
    await call.message.answer("Для создания новой записи напишите /start")
    await call.message.edit_reply_markup(reply_markup=None)
    await state.finish()


@dp.callback_query_handler(state=Test.Q2)
async def month_zapis(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    month = str(call.data)[6::]
    now_day = int(str(date.today())[-2::])
    number_today = int(str(date.today())[5:7])-1
    await state.update_data(answer_month=month)
    keyb2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{'1' if now_day < 1 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="1")),
                InlineKeyboardButton(text=f"{'2' if now_day < 2 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="2")),
                InlineKeyboardButton(text=f"{'3' if now_day < 3 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="3")),
                InlineKeyboardButton(text=f"{'4' if now_day < 4 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="4")),
                InlineKeyboardButton(text=f"{'5' if now_day < 5 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="5")),
                InlineKeyboardButton(text=f"{'6' if now_day < 6 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="6")),
                InlineKeyboardButton(text=f"{'7' if now_day < 7 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="7")),
            ],
            [
                InlineKeyboardButton(text=f"{'8' if now_day < 8 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="8")),
                InlineKeyboardButton(text=f"{'9' if now_day < 9 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="9")),
                InlineKeyboardButton(text=f"{'10' if now_day < 10 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="10")),
                InlineKeyboardButton(text=f"{'11' if now_day < 11 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="11")),
                InlineKeyboardButton(text=f"{'12' if now_day < 12 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="12")),
                InlineKeyboardButton(text=f"{'13' if now_day < 13 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="13")),
                InlineKeyboardButton(text=f"{'14' if now_day < 14 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="14")),
            ],
            [
                InlineKeyboardButton(text=f"{'15' if now_day < 15 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="15")),
                InlineKeyboardButton(text=f"{'16' if now_day < 16 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="16")),
                InlineKeyboardButton(text=f"{'17' if now_day < 17 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="17")),
                InlineKeyboardButton(text=f"{'18' if now_day < 18 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="18")),
                InlineKeyboardButton(text=f"{'19' if now_day < 19 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="19")),
                InlineKeyboardButton(text=f"{'20' if now_day < 20 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="20")),
                InlineKeyboardButton(text=f"{'21' if now_day < 21 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="21")),
            ],
            [
                InlineKeyboardButton(text=f"{'22' if now_day < 22 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="22")),
                InlineKeyboardButton(text=f"{'23' if now_day < 23 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="23")),
                InlineKeyboardButton(text=f"{'24' if now_day < 24 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="24")),
                InlineKeyboardButton(text=f"{'25' if now_day < 25 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="25")),
                InlineKeyboardButton(text=f"{'26' if now_day < 26 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="26")),
                InlineKeyboardButton(text=f"{'27' if now_day < 27 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="27")),
                InlineKeyboardButton(text=f"{'28' if now_day < 28 or month != month_list[number_today] else ''}",
                                     callback_data=day_callback.new(date="28")),
            ],
            [
                InlineKeyboardButton(text=f"{'29' if month_day[month] > 28 and (now_day < 29 or month != month_list[number_today]) else ''}",
                                     callback_data=day_callback.new(date=f"{'29' if month_day[month] >= 29 else ''}")),
                InlineKeyboardButton(text=f"{'30' if month_day[month] > 29 and (now_day < 30 or month != month_list[number_today]) else ''}",
                                     callback_data=day_callback.new(date=f"{'30' if month_day[month] >= 30 else ''}")),
                InlineKeyboardButton(text=f"{'31' if month_day[month] > 30 and (now_day < 31 or month != month_list[number_today]) else ''}",
                                     callback_data=day_callback.new(date=f"{'31' if month_day[month] >= 31 else ''}"))
            ],
            [
                InlineKeyboardButton(text="Назад ↩", callback_data="cancel")
            ]
        ]
    )
    await call.message.answer("А теперь день 🗓", reply_markup=keyb2)
    await Test.Q3.set()


@dp.callback_query_handler(state=Test.Q3, text_contains="cancel")
async def another_month(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    now = int(str(date.today())[5:7]) - 1
    keyb1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{month_list[now] if now <= 12 else month_list[now - 12]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now] if now <= 12 else month_list[now - 12]}")),
                InlineKeyboardButton(text=f"{month_list[now + 1] if now + 1 <= 12 else month_list[now - 11]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now + 1] if now + 1 <= 12 else month_list[now - 11]}"))
            ],
            [
                InlineKeyboardButton(text=f"{month_list[now + 2] if now + 2 <= 12 else month_list[now - 10]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now + 2] if now + 2 <= 12 else month_list[now - 10]}")),
                InlineKeyboardButton(text=f"{month_list[now + 3] if now + 3 <= 12 else month_list[now - 9]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now + 3] if now + 3 <= 12 else month_list[now - 9]}"))
            ],
            [
                InlineKeyboardButton(text="Назад ↩", callback_data="cancel")
            ]
        ]
    )
    await call.message.answer("Выберите месяц и число, когда Вы бы хотели к нам приехать 🗓",
                              reply_markup=keyb1)
    await Test.Q2.set()


@dp.callback_query_handler(state=Test.Q3)
async def end_zapis(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    day = str(call.data)[6::]
    await state.update_data(answer_day=day)
    data = await state.get_data()
    month = data.get('answer_month')
    now_month = 0
    for i in month_list:
        if i == month:
            break
        now_month += 1
    keyb3 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{month_list[now_month] if now_month <= 12 else month_list[now_month - 12]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now_month] if now_month <= 12 else month_list[now_month - 12]}")),
                InlineKeyboardButton(text=f"{month_list[now_month + 1] if now_month + 1 <= 12 else month_list[now_month - 11]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now_month + 1] if now_month + 1 <= 12 else month_list[now_month - 11]}"))
            ],
            [
                InlineKeyboardButton(text="Назад ↩", callback_data="cancel")
            ]
        ]
    )
    await call.message.answer("Выберите месяц и число, когда Вы планируете выезд 📅",
                              reply_markup=keyb3)
    await Test.Q4.set()


@dp.callback_query_handler(state=Test.Q4, text_contains="cancel")
async def another_month(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    now = int(str(date.today())[5:7]) - 1
    keyb1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{month_list[now] if now <= 12 else month_list[now - 12]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now] if now <= 12 else month_list[now - 12]}")),
                InlineKeyboardButton(text=f"{month_list[now + 1] if now + 1 <= 12 else month_list[now - 11]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now + 1] if now + 1 <= 12 else month_list[now - 11]}"))
            ],
            [
                InlineKeyboardButton(text=f"{month_list[now + 2] if now + 2 <= 12 else month_list[now - 10]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now + 2] if now + 2 <= 12 else month_list[now - 10]}")),
                InlineKeyboardButton(text=f"{month_list[now + 3] if now + 3 <= 12 else month_list[now - 9]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now + 3] if now + 3 <= 12 else month_list[now - 9]}"))
            ],
            [
                InlineKeyboardButton(text="Назад ↩", callback_data="cancel")
            ]
        ]
    )
    await call.message.answer("Выберите месяц и число, когда Вы бы хотели к нам приехать 🗓",
                              reply_markup=keyb1)
    await Test.Q2.set()


@dp.callback_query_handler(state=Test.Q4)
async def day_out_zapis(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    month = str(call.data)[6::]
    await state.update_data(answer_month_out=month)
    data = await state.get_data()
    day = int(data.get('answer_day'))
    month_input = data.get('answer_month')
    keyb4 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{'1' if month_input != month or day < 1 else ''}", callback_data=day_callback.new(date="1")),
                InlineKeyboardButton(text=f"{'2' if month_input != month or day < 2 else ''}", callback_data=day_callback.new(date="2")),
                InlineKeyboardButton(text=f"{'3' if month_input != month or day < 3 else ''}", callback_data=day_callback.new(date="3")),
                InlineKeyboardButton(text=f"{'4' if month_input != month or day < 4 else ''}", callback_data=day_callback.new(date="4")),
                InlineKeyboardButton(text=f"{'5' if month_input != month or day < 5 else ''}", callback_data=day_callback.new(date="5")),
                InlineKeyboardButton(text=f"{'6' if month_input != month or day < 6 else ''}", callback_data=day_callback.new(date="6")),
                InlineKeyboardButton(text=f"{'7' if month_input != month or day < 7 else ''}", callback_data=day_callback.new(date="7")),
            ],
            [
                InlineKeyboardButton(text=f"{'8' if month_input != month or day < 8 else ''}", callback_data=day_callback.new(date="8")),
                InlineKeyboardButton(text=f"{'9' if month_input != month or day < 9 else ''}", callback_data=day_callback.new(date="9")),
                InlineKeyboardButton(text=f"{'10' if month_input != month or day < 10 else ''}", callback_data=day_callback.new(date="10")),
                InlineKeyboardButton(text=f"{'11' if month_input != month or day < 11 else ''}", callback_data=day_callback.new(date="11")),
                InlineKeyboardButton(text=f"{'12' if month_input != month or day < 12 else ''}", callback_data=day_callback.new(date="12")),
                InlineKeyboardButton(text=f"{'13' if month_input != month or day < 13 else ''}", callback_data=day_callback.new(date="13")),
                InlineKeyboardButton(text=f"{'14' if month_input != month or day < 14 else ''}", callback_data=day_callback.new(date="14")),
            ],
            [
                InlineKeyboardButton(text=f"{'15' if month_input != month or day < 15 else ''}", callback_data=day_callback.new(date="15")),
                InlineKeyboardButton(text=f"{'16' if month_input != month or day < 16 else ''}", callback_data=day_callback.new(date="16")),
                InlineKeyboardButton(text=f"{'17' if month_input != month or day < 17 else ''}", callback_data=day_callback.new(date="17")),
                InlineKeyboardButton(text=f"{'18' if month_input != month or day < 18 else ''}", callback_data=day_callback.new(date="18")),
                InlineKeyboardButton(text=f"{'19' if month_input != month or day < 19 else ''}", callback_data=day_callback.new(date="19")),
                InlineKeyboardButton(text=f"{'20' if month_input != month or day < 20 else ''}", callback_data=day_callback.new(date="20")),
                InlineKeyboardButton(text=f"{'21' if month_input != month or day < 21 else ''}", callback_data=day_callback.new(date="21")),
            ],
            [
                InlineKeyboardButton(text=f"{'22' if month_input != month or day < 22 else ''}", callback_data=day_callback.new(date="22")),
                InlineKeyboardButton(text=f"{'23' if month_input != month or day < 23 else ''}", callback_data=day_callback.new(date="23")),
                InlineKeyboardButton(text=f"{'24' if month_input != month or day < 24 else ''}", callback_data=day_callback.new(date="24")),
                InlineKeyboardButton(text=f"{'25' if month_input != month or day < 25 else ''}", callback_data=day_callback.new(date="25")),
                InlineKeyboardButton(text=f"{'26' if month_input != month or day < 26 else ''}", callback_data=day_callback.new(date="26")),
                InlineKeyboardButton(text=f"{'27' if month_input != month or day < 27 else ''}", callback_data=day_callback.new(date="27")),
                InlineKeyboardButton(text=f"{'28' if month_input != month or day < 28 else ''}", callback_data=day_callback.new(date="28")),
            ],
            [
                InlineKeyboardButton(text=f"{'29' if month_day[month] >= 29 and (month_input != month or day < 29) else ''}",
                                     callback_data=day_callback.new(date=f"{'29' if month_day[month] >= 29 else ''}")),
                InlineKeyboardButton(text=f"{'30' if month_day[month] >= 30 and (month_input != month or day < 30) else ''}",
                                     callback_data=day_callback.new(date=f"{'30' if month_day[month] >= 30 else ''}")),
                InlineKeyboardButton(text=f"{'31' if month_day[month] >= 31 and (month_input != month or day < 31) else ''}",
                                     callback_data=day_callback.new(date=f"{'31' if month_day[month] >= 31 else ''}"))
            ],
            [
                InlineKeyboardButton(text="Назад ↩", callback_data="cancel")
            ]
        ]
    )
    await call.message.answer("А теперь день 🗓", reply_markup=keyb4)
    await Test.Q5.set()


@dp.callback_query_handler(state=Test.Q5, text_contains="cancel")
async def end_zapis(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    day = str(call.data)[6::]
    await state.update_data(answer_day=day)
    data = await state.get_data()
    month = data.get('answer_month')
    now_month = 0
    for i in month_list:
        if i == month:
            break
        now_month += 1
    keyb3 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{month_list[now_month] if now_month <= 12 else month_list[now_month - 12]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now_month] if now_month <= 12 else month_list[now_month - 12]}")),
                InlineKeyboardButton(text=f"{month_list[now_month + 1] if now_month + 1 <= 12 else month_list[now_month - 11]}",
                                     callback_data=month_callback.new(
                                         month=f"{month_list[now_month + 1] if now_month + 1 <= 12 else month_list[now_month - 11]}"))
            ],
            [
                InlineKeyboardButton(text="Назад ↩", callback_data="cancel")
            ]
        ]
    )
    await call.message.answer("Выберите месяц и число, когда Вы планируете выезд 📅",
                              reply_markup=keyb3)
    await Test.Q4.set()


@dp.callback_query_handler(state=Test.Q5)
async def zapis_made(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=1)
    day_out = str(call.data)[6::]
    await state.update_data(answer_day_out=day_out)
    data = await state.get_data()
    month = data.get('answer_month')
    day = data.get('answer_day')
    month_out = data.get('answer_month_out')
    await call.message.answer("Аренда домика продлится: \n"
                              f"С {month}, {day} число ✅\n"
                              f"По {month_out}, {day_out} число ✅\n"
                              f"Для подтверждения и создания записи скажите как к Вам можно будет обращаться 😀\n"
                              f"И отправьте нам свой номер телефона ☎ \n"
                              f"Для отмены записи введите команду /cancel",
                              reply_markup=types.ReplyKeyboardRemove())
    await Test.Q6.set()


@dp.message_handler(state=Test.Q6)
async def create_zapis(message: types.message, state: FSMContext):
    await message.answer("Спасибо, запись создана!\n"
                         "В ближайшее время с Вами свяжется наш сотрудник ☺")
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    answer1 = data.get('answer_month')
    answer2 = data.get('answer_day')
    answer3 = data.get('answer_month_out')
    answer4 = data.get('answer_day_out')
    await state.finish()
    for i in ADMINS:
        await bot.send_message(chat_id=i,
                               text=f'Новая запись c {answer1}, {answer2} число, по {answer3}, {answer4} число\n'
                                    f'Имя и номер телефона посетителя: {phone_number}')


@dp.callback_query_handler(text="about")
async def tell_about(call: CallbackQuery):
    await call.answer()


@dp.callback_query_handler(text="helpme")
async def tell_about(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Мы готовы проконсультировать Вас!\n"
                              "Задайте свой вопрос ниже 💬")
    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def helpme1(message: types.Message, state: FSMContext):
    await bot.send_message('961406924', text=message.text)
    await bot.send_message('961406924', text=f"Спрашивает посетитель: @{message.from_user.username}\n"
                                             f"Попрошу ответить ему в личку.")
    await message.answer("Мы ответим Вам в личные сообщения в ближайшее время.")
    await state.finish()
    await message.answer("Возвращаю Вас в основное меню",
                         reply_markup=keyb0)
