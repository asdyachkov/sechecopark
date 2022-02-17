from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import arend_callback

keyb0 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Арендовать домик 🛎", callback_data=arend_callback.new(
                answer="arend_True"
            ))
        ],
        [
            InlineKeyboardButton(text="О нас 📋", callback_data="about")
        ],
        [
            InlineKeyboardButton(text="Поддержка ⁉", callback_data="helpme")
        ]
    ]
)
