import requests
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings

_ = load_dotenv(find_dotenv())

'''
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

API_KEY = "cf39c9ce6431bd6c53143b1ed54dc663"

def find_weather(city: str) -> dict:
    units = "metric"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units,
    }
    response = requests.get(BASE_URL, params)
    result = response.json()
    return result

output = find_weather('Cairo')
print(output)

'''

# Define the output schema for the tool
class WeatherForecast(BaseModel):
    location: str
    description: str
    temperature_celsius: float

weather_agent = Agent(
    model='groq:llama-3.3-70b-versatile',
    model_settings=ModelSettings(temperature=0.2),
    output_type=str,
    system_prompt=("You are a helpful weather assistant. Use 'get_weather_forecast' tool "
    "to find current weather conditions for any city.Provide clean and friendly answers."),
)

# weather forecast tool
@weather_agent.tool
def get_weather_forecast(ctx: RunContext, city: str) -> WeatherForecast:
    url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "cf39c9ce6431bd6c53143b1ed54dc663"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
    }
    response = requests.get(url, params)
    result = response.json()

    return WeatherForecast(
        location=result["name"],
        description=result["weather"][0]["description"].capitalize(),
        temperature_celsius=result["main"]["temp"]
    )

question = input("Ask about the weather:  ")
response = weather_agent.run_sync(question)
print("Forecast: ", response.output)