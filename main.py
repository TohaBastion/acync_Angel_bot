import logging
import sys

import asyncio
import aioschedule as schedule
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random
from setting import TOKEN, id_chat

from google_parth import *

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def random_emojis():
    emoji_list = list('😎👾🤖🦾👳‍♂️🏃🦺🎩👑🧳🦄🐿⭐️🍔🍟🥓🥩🍗🍕🧀🍖🦴🍿🍫🥃🥤⚾⚾🥎️🥎🤿🥇🚦🔋☎️📡🛎🎊🎉🎎🎁🎈↗️⏫⏏️')
    new_random_emojis = ''.join(random.sample(emoji_list, k=7))
    return new_random_emojis


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    btn1 = KeyboardButton(text='⚾ Розклад запланованих ігор')
    btn2 = KeyboardButton(text='📈 📉 Посилання на статистику')
    btn_row = [btn1, btn2]
    markup = ReplyKeyboardMarkup(keyboard=[btn_row], resize_keyboard=True)

    # Відправлення повідомлення з клавіатурою
    await bot.send_message(
        message.chat.id,
        text=f'ПАПИДЖЕ! КАЖИ ШО ХТІВ!?\n{random_emojis()}',
        reply_markup=markup
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text == '\U000026BE Розклад запланованих ігор' or message.text == 'Розклад запланованих ігор':
        await message.answer(f'ПАПИДЖЕ!!! ПОГОДЬ Я ГЛЯНУ В РОЗКЛАД!\n{random_emojis()}')
        i = google_parth_schedule('KBL_2024')
        answer = "\n".join([x for x in i])
        await message.answer(f'{answer}')
    elif message.text == '\U0001F4C8 \U0001F4C9 Посилання на статистику' or message.text == 'Посилання на статистику':
        link_btn = InlineKeyboardButton(text='Перейти', url='http://iscorebaseball.com/angelskyiv')
        markup = InlineKeyboardMarkup(inline_keyboard=[[link_btn]])
        await message.answer(
            f'ТИ ХАРОШИЙ ДРУГ!{random_emojis()}\nТРИМАЙ ПОСИЛАННЯ!\nhttp://iscorebaseball.com/angelskyiv',
            reply_markup=markup)


async def happy_birthday():
    i = google_parth_birthday('Angels_Team')
    for x in i:
        await bot.send_message(chat_id=id_chat, text=f'{x.upper()}\n{random_emojis()}')
        await bot.send_sticker(chat_id=id_chat,
                               sticker='CAACAgIAAxkBAAEMKnRmTgRKXwSlCazWNbwy9afBiOQ5hQACog4AAkwumEiUYoAWoM0EVjUE')


async def run_pull_schedule():
    i = google_parth_schedule_pull('KBL_2024')
    for row in i:
        game_date = row['date']
        game_time = row['time']
        first_team = row['first_team']
        second_team = row['second_team']

        await bot.send_poll(chat_id=id_chat, question=f'Чи плануєте бути на грі\n{game_date} о '
                                                      f'{game_time}\n {first_team} - '
                                                      f'{second_team}?', options=(['Так', 'Ні', 'Я ще думаю']))


async def my_loop():
    schedule.every().day.at('05:00').do(lambda: asyncio.create_task(happy_birthday()))
    schedule.every().day.at('09:00').do(lambda: asyncio.create_task(run_pull_schedule()))
    while True:
        await schedule.run_pending()
        await asyncio.sleep(0.1)


async def main():
    task1 = asyncio.create_task(dp.start_polling(bot))
    task2 = asyncio.create_task(my_loop())

    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
