from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Узнать погоду",
            callback_data='btn'
        )
    ],
[
        InlineKeyboardButton(
            text="Закрыть",
            callback_data='close'
        )
    ]
])
