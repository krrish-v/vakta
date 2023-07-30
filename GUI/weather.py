import requests

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": "<API KEY>", "units": "metric"}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        forecast = f"Weather forecast for {city}: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s"
        return forecast
    else:
        return "Unabel to fetch the weather of your city"
