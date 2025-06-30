import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
phone_number = os.getenv('phone_number')
bot_token = os.getenv('TELEGRAM_NOTE_BOT')
bot_chat_id = os.getenv('TELEGRAM_CHAT_ID')

async def send_telegram_message(message):
    bot = Bot(token=bot_token)
    async with bot:
        await bot.send_message(chat_id=bot_chat_id, text=message)
