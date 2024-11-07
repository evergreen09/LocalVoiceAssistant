import pygame
import requests
import json
import time

def high_cross_alarm(target_price):
    current_price = 0.0
    price_url = f'https://okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP'
    while current_price < target_price:    
        current_price = float(requests.get(price_url).json()['data'][0]['last'])
        print(current_price)
    pygame.mixer.init()
    pygame.mixer.music.load('kanye_alarm.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def low_cross_alarm(target_price):
    current_price = 1000000.0
    price_url = f'https://okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP'
    while target_price < current_price:    
        current_price = float(requests.get(price_url).json()['data'][0]['last'])
        print(current_price)
    pygame.mixer.init()
    pygame.mixer.music.load('kanye_alarm.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)