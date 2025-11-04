import requests

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