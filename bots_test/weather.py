import requests

def get_weather(location):
    url = f"https://yahoo-weather5.p.rapidapi.com/weather?location={location}&format=json&u=f"
    headers = {
        "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com",
        "x-rapidapi-key": "f693aebe6emsh24b20d5277b40d4p1dccaajsn867936a8eb25"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def main():
    location = "Moscow"
    weather_data = get_weather(location)
    print(weather_data)

if __name__ == "__main__":
    main()