from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
from os import getenv

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# print(API_TOKEN)

# configure logging

logging.basicConfig(level=logging.INFO)

# initialize bot 

bot = Bot(token=API_TOKEN)

# initialize dispatcher

dp = Dispatcher(bot)

# define decorator handler

@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
    """This will return echo message

    Args:
        message (types.Message): _description_
    """
    
    await message.reply("Hi!\n I'm Echo Bot! \n Powered by Aiogram") 

@dp.message_handler()
async def echo(message: types.Message):
    """This will return echo message

    Args:
        message (types.Message): _description_
    """
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)