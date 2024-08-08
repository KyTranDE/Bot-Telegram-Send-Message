# import asyncio
from telegram import Bot
from time import sleep
from messageTelegram.message_template import message_template
import json


def potsMessage(data): #data is json data
    bot = Bot(token='7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds')
    chat_id = '-4231092140'
    message = message_template.format(
        name=data['name'], price=data['price'], location=data['location'], url=data['urlcar'])

    bot.send_photo(
        chat_id=chat_id,
        photo=data['urlcar'],
        caption=message,
        parse_mode='HTML'  # Chỉ định định dạng HTML
    )

