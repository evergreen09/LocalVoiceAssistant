from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json
from pydantic import BaseModel
import re
from datetime import datetime, timedelta
import ccxt
import asyncio
import time

load_dotenv()
binance = ccxt.binance()

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
        tickerSymobl: "str"
    }
}
"""

# Choosing Function Class
class chooseTask(BaseModel):
    function: str
    parameter: list[str]

def get_crypto_price(ticker: str):
    last_price = binance.fetch_ticker(f'{ticker}/USDT')['last']
    print(f'${last_price}')

def get_location_key(location: str):
    url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={weather_api}&q={location}'
    response = requests.get(url).json()
    key = response[0]['Key']
    return key

def get_weather(location: str):
    key = get_location_key(location)
    url = f'http://dataservice.accuweather.com/currentconditions/v1/{key}?apikey={weather_api}'
    response = requests.get(url).json()
    weather_condition = response[0]['WeatherText']
    temperature_c = response[0]['Temperature']['Metric']['Value']

    print(f'The weather in {location} is {weather_condition} and the temperature is {temperature_c} celcius')

def get_keyword_news(keyword: str):
    date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f'https://newsapi.org/v2/everything?q={keyword}&from={date}&sortBy=relevancy&apiKey={news_api}'
    response = requests.get(url).json()
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
