import os
import requests

class WeatherAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather_for_location(self, location_name: str) -> dict:
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": location_name,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            data = response.json()

            precipitation = data.get("rain", {}).get("1h", 0)
            wind_speed = data.get("wind", {}).get("speed", 0)

            return {
                "forecast": {
                    "precipitation": precipitation,
                    "wind_speed": wind_speed
                }
            }
        except Exception as e:
            return {
                "forecast": {
                    "precipitation": 0,
                    "wind_speed": 0,
                    "error": str(e)
                }
            }
