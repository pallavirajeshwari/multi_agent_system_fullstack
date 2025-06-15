import requests
import os

class WeatherAgent:
    """
    Retrieves weather data using the OpenWeatherMap API.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "your-api-key-here")  # Replace or load from .env

    def get_weather_for_location(self, city_name: str) -> dict:
        """
        Fetches current weather data for a given city using OpenWeatherMap.
        """
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city_name,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            data = response.json()

            # Extract rainfall (optional field), wind speed
            precipitation = data.get("rain", {}).get("1h", 0)  # fallback to 0 if missing
            wind_speed = data["wind"]["speed"]  # in m/s

            return {
                "forecast": {
                    "precipitation": precipitation * 10,  # roughly approximate to percent chance
                    "wind_speed": wind_speed * 3.6  # convert m/s to km/h
                }
            }

        except Exception as e:
            print(f"[Weather API Error] {e}")
            return {
                "forecast": {
                    "precipitation": 0,
                    "wind_speed": 0,
                    "error": str(e)
                }
            }
