from pprint import pprint
import requests
import json

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types, Bot
import asyncio

from keyboards.keyboards import btn

router = Router()

READY = []


def switcher(d) -> bool:
    if d == 'text':
        READY.append('some')
        return True
    elif d == 'result' and len(READY):
        READY.clear()
        return True
    return False


@router.message(Command("start"))
async def cmd_btn(message: Message):
    await message.answer(
        "Выберите действие",
        reply_markup=btn
    )


@router.callback_query(F.data == "close")
async def make_ready_true(callback: types.CallbackQuery) -> None:
    await callback.message.delete()


@router.callback_query(F.data == "btn")
async def send_random_value(callback: types.CallbackQuery) -> None:
    switcher('text')
    await callback.message.answer('Введите название города для того, чтобы узнать погоду')
    await callback.message.delete()


HELP_COMMAND = """
/start начать работу с ботом
/help помощь
"""


@router.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)


def get_info(cityName):
    try:
        r = requests.get(f'http://127.0.0.1:8000/weather/?city={cityName}')
        dataJSON = r.json()
        if type(dataJSON) == list:

            dataJSON = dataJSON[0]
            dataDict = {
                'city': dataJSON['city']['cityName'],
                'temp': dataJSON['temp'],
                'pressureMM': dataJSON['pressureMM'],
                'windSpeed': dataJSON['windSpeed'],
                'wasType': 'list'
            }
            return dataDict
        elif type(dataJSON) == dict:
            data = {
                'error': dataJSON['CityError'],
                'wasType': 'dict'
            }
            return data
    except requests.exceptions.Timeout as e:
        raise SystemExit(e)
    except requests.exceptions.TooManyRedirects as e:
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


@router.message()
async def echo(message: types.Message, bot: Bot):
    result = switcher('result')
    RESPONSE = {}
    if result:
        cityName = message.text.lower().strip()
        pprint(cityName)
        RESPONSE = get_info(cityName)
        pprint(RESPONSE)
    if result:
        pprint(RESPONSE)
        if RESPONSE.get('wasType') == 'list':
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"*{RESPONSE.get('city').title()}*\n"
                     f"Температура: {RESPONSE.get('temp')}\n"
                     f"Скорость ветра: {RESPONSE.get('windSpeed')}\n"
                     f"Атмосферное давление: {RESPONSE.get('pressureMM')}",
                parse_mode='markdown'
            )
            switcher('no')
        elif RESPONSE.get('wasType') == 'dict':
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"*{RESPONSE.get('error')}*",
                parse_mode='markdown',
                reply_markup=btn
            )
            switcher('no')
    else:
        await message.delete()
