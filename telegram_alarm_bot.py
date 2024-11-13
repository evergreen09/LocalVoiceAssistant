import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
phone_number = os.getenv('phone_number')
bot_token = os.getenv('bot_token')
bot_chat_id = 7181552894

# Initialize the client
client = TelegramClient('alarm_bot', api_id, api_hash)

"""
alarm(Must wake up functions[send message to bot(specific text or solve math problems)])
"""


async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


'''
# Initialize the client
client = TelegramClient('get_admin_msg', api_id, api_hash)

async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

@client.on(events.NewMessage(chats=chat_id))
async def handler(event):
    sender = await event.get_sender()
    
    if event.is_channel and sender is None:
        # This is a message from the group itself or an anonymous admin
        print(f"Message from the group or anonymous admin: {event.text}")
        message = f'Message from Raizel: {event.text}'
        await send_telegram_message(bot_token, bot_chat_id, message)
    else:
        # This is a message from another user
        print(f"New message from {sender.username if sender else 'unknown'}: {event.text}")

async def main():
    await client.start(phone_number)
    print("Client is running...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())'''