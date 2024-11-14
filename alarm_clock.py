from datetime import datetime 
import threading
import time
import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
import pygame

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
phone_number = os.getenv('phone_number')
bot_token = os.getenv('bot_token')
bot_chat_id = 7181552894

# Initialize the client
client = TelegramClient('alarm_bot', api_id, api_hash)

wake_up_message = "Type Following Sentence to stop the alarm... \n I am totally awake and ready to take a shower"

async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

@client.on(events.NewMessage(chats=bot_chat_id))
async def handler(event):
    global wake_up_message
    sender = await event.get_sender()
    
    if sender.username == "slothtrader1" and event.text == wake_up_message:
        # This is a message from the group itself or an anonymous admin
        print(f"Alarm Off")
        pygame.mixer.music.stop()
        loop = asyncio.get_event_loop()
        loop.stop()



async def alarm_mission_run():
    await client.start()
    print("Client Started")

class AlarmClock:
    def __init__(self, alarm_time):
        self.alarm_time = alarm_time
        self.alarm_thread = threading.Thread(target=self.run_alarm)

    def run_alarm(self):
        global wake_up_message
        current_time = datetime.now().strftime("%H:%M")
        print(current_time, self.alarm_time)
        while current_time != self.alarm_time:
            current_time = datetime.now().strftime("%H:%M")
            time.sleep(5)
            print(current_time, self.alarm_time)
        send_telegram_message(bot_token, bot_chat_id, wake_up_message)
        pygame.mixer.init()
        pygame.mixer.music.load('alarm.mp3')
        asyncio.run(alarm_mission_run())
        
        

    def start(self):
        self.alarm_thread.start()

