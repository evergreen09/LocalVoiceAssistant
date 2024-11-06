from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json
from pydantic import BaseModel
import re

load_dotenv()

# AccuWeather APIKey
weather_api = os.getenv("ACCUWEATHER_API")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

choose_task_system = """
Use the following step-by-step instructions to respond to user inputs.
Step 1 - The user will provide a query along with a list of functions with its name, description, and parameter(s). Identity the function based on user query and function description. Make sure you only choose a function from the function list provided by the user. Return None if no such functions from the list can fulfill a user query.
Step 2 - Figure out which parameters are required for selected function from previous step. Identify the appropriate value for a parameter or paremeters soley from the user query. Do not hallucinate.
"""

function_list = """
{
    "functionName": "get_weather",
    "description": "Get weather condition and temperature based on the location parameter provided"
    "parameter": {
        "location": "str"
    },
    "functionName": "get_news",
    "description": "Based on the topic parameter provided, the function returns top headline news related to the topic"
    "parameter": {
        "topic": "str"
    },
    "functionName": "get_price",
    "description": "Returns a live price of a ticker symbol. The parameter must be in ticker symbol not the name of the asset, cryptocurrency, or a company like following: JNJ, DIS, INTC, V, KO, BTC, ETH, LTC, DJI."
    "parameter": {
        "ticker": "str"
    }
}
"""

# Choosing Function Class
class chooseTask(BaseModel):
    function: str
    parameter: list[str]

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
    if len(params) == 1:
        argument = params[0]
    print(params, argument)
    print(function_name)
    try:
        function_call = globals()[function_name]
        function_call(argument)
    except AttributeError:
        print(f"Function {function_name} not found.")
    except TypeError as e:
        print(f"Error calling function {function_name}: {e}")

get_task("What's the weather in Busan?")
