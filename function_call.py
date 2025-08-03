from openai import OpenAI
from dotenv import load_dotenv
import os
import httpx
import json
from pydantic import BaseModel
import re
from datetime import datetime, timedelta
import ccxt
from playsound3 import playsound
import asyncio
import time
from alarm_clock import AlarmClock
from send_note import send_telegram_message
from m_tts import text_to_voice

load_dotenv()
binance = ccxt.binance()
start_time = None

# Necessary APIKeyS
weather_api = os.getenv("ACCUWEATHER_API_KEY")
news_api = os.getenv("NEWS_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

choose_task_system = """
Use the following step-by-step instructions to respond to user inputs.
Step 1 - The user will provide a query along with a list of functions with its name, description, and parameter(s). Identity the function based on user query and function description. Make sure you only choose a function from the function list provided by the user. Return None if no such functions from the list can fulfill a user query.
Step 2 - Figure out which parameters are required for selected function from previous step. Identify the appropriate value for a parameter or paremeters soley from the user query. Do not hallucinate.
"""

news_summarization = """
Your job is to summarize articles that are in a json format.
"""

function_list = """
{
    "functionName": "get_weather",
    "description": "Get weather condition and temperature based on the location parameter provided"
    "parameter": {
        "location": "str"
    },
    "functionName": "get_keyword_news",
    "description": "Based on the keyword parameter provided, the function returns news related to the keyword"
    "parameter": {
        "keyword": "str"
    },
    "functionName": "get_crypto_price",
    "description": "Returns the live price of cryptocurrency that user requested. The parameter must be in ticker symbol and not the name like following: XRP, ETH, LTC, BTC."
    "parameter": {
        tickerSymbol: "str"
    },
    "functionName": "btc_alarm",
    "description": "Sets alarm with target price. The target price parameter should be an integer."
    "parameter": {
        targetPrice: "int"
    },
    "functionName": "set_timer",
    "description": "Sets a timer in minutes. The timerTime parameter must be in seconds. If a user asks to set a timer in hours or minutes, convert it into seconds"
    "parameter": {
        timerTime: "int"
    },
    "functionName": "set_alarm",
    "description": "Sets an alarm based on the user's desire time. The parameter should be in HH:MM where hour is in 24 hour format."
    "parameter": {
        alarm_time: "str"
    },
    

}
"""

# Choosing Function Class
class chooseTask(BaseModel):
    function: str
    parameter: list[str]

def set_timer(timer_duration):
    global start_time
    timer_duration = int(timer_duration)
    end_time = time.time()
    timer_seconds = timer_duration - (end_time - start_time)
    print(timer_seconds)
    time.sleep(timer_seconds)

def set_alarm(alarm_time):
    pattern == r'^[0-9]:[0-9]$'
    if re.match(pattern, alarm_time):
        alarm = AlarmClock(alarm_time)
        alarm.start
    else:
        print(f"Wrong time Format: {alarm_time}")

def btc_alarm(target_price):
    target_price = int(target_price)
    print(target_price)
    price_url = f'https://okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP'
    current_price = float(httpx.get(price_url).json()['data'][0]['last'])
    if current_price < target_price:
        high_price_cross_alarm(target_price)
    else: 
        low_price_cross_alarm(target_price)

def high_price_cross_alarm(target_price):
    print('high')
    current_price = 0.0
    price_url = f'https://okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP'
    while current_price < target_price:    
        current_price = float(httpx.get(price_url).json()['data'][0]['last'])
        print(current_price)

    cross_alarm_sound = playsound('sourceFile/kanye_alarm.mp3', block=False backend='afplay')
    # Temp play alaram for 120 seconds -> Implement a method to turn off the alarm using telegram messenger or voice command
    time.sleep(120)
    cross_alarm_sound.stop() 

def low_price_cross_alarm(target_price):
    print('low')
    current_price = 1000000.0
    price_url = f'https://okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP'
    while target_price < current_price:    
        current_price = float(httpx.get(price_url).json()['data'][0]['last'])
        print(current_price)
        
    cross_alarm_sound = playsound('sourceFile/kanye_alarm.mp3', block=False backend='afplay')
    # Temp play alaram for 120 seconds -> Implement a method to turn off the alarm using telegram messenger or voice command
    time.sleep(120)
    cross_alarm_sound.stop() 


def get_crypto_price(ticker: str):
    last_price = binance.fetch_ticker(f'{ticker}/USDT')['last']
    print(f'${last_price}')

def get_location_key(location: str):
    url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={weather_api}&q={location}'
    response = httpx.get(url).json()
    key = response[0]['Key']
    return key

def weather_safety_advice(weather_forecast_detail: str):
    messages = [
        {"role": "system", "content": """Your one and only job is to provide weather safety advices 
        to the user based on a user prompt containing a weather forecast. 
        Here are some examples of advices you should provide. 
        It is expected to rain starting at 3PM. Please bring an umbrella with you if you plan to go out after 3PM.
        The sun is expected to be really bright this afternoon. Please wear sunglasses to protect your eyes.
        The temperature today is reaching over 30 degree celcius. Bring a water bottle with you if you plan to do outdoor activities.
        """},
        {"role": "user", "content": f"{weather_forecast_detail}"}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300
        )
        # Note the new way to access the response content:
        weather_advisory = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API for word '{weather_forecast_detail}': {e}")
        return f"Error fetching data for {weather_forecast_detail}."
    return weather_advisory

def get_weather(location: str):
    key = get_location_key(location)
    url = f'http://dataservice.accuweather.com/currentconditions/v1/{key}?apikey={weather_api}'
    response = httpx.get(url).json()
    weather_condition = response[0]['WeatherText']
    temperature_c = response[0]['Temperature']['Metric']['Value']
    weather_forecast = f'The weather in {location} is {weather_condition} and the temperature is {temperature_c} celcius'

    print(weather_forecast)
    # Weather Forecast to Speech
    text_to_voice(weather_forecast)

def get_keyword_news(keyword: str):
    date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f'https://newsapi.org/v2/everything?q={keyword}&from={date}&sortBy=relevancy&apiKey={news_api}'
    response = httpx.get(url).json()
    print(response)
    top_five = []
    for index, article in enumerate(response['articles']):
        if index < 5:
            top_five.append(article)
        else:
            break
    article_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{news_summarization}"},
            {"role": "user", "content": f"Analyze following articles and provide concise description of articles as if you are a morning radio show host:{top_five}"},
        ]
    )
    print(article_response.choices[0].message.content)

def get_task(user_query):
    global start_time
    start_time = time.time()
    task_function = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{choose_task_system}"},
            {"role": "user", "content": f"Following is a list of functions: {function_list}. {user_query}"},
        ],
        response_format=chooseTask,
    )
    task_response = task_function.choices[0].message.content

    task_json = json.loads(task_response)
    function_name = task_json['function'].strip()
    params = task_json['parameter']
    print(function_name)
    if len(params) == 1:
        argument = params[0]
        print(params, argument)

        try:
            function_call = globals()[function_name]
            function_call(argument)
        except AttributeError:
            print(f"Function {function_name} not found.")
        except TypeError as e:
            print(f"Error calling function {function_name}: {e}")
    else:
        try:
            function_call = globals()[function_name]
            function_call()
        except AttributeError:
            print(f"Function {function_name} not found.")
        except TypeError as e:
            print(f"Error calling function {function_name}: {e}")

get_task("What's the weather in Seoul?")

