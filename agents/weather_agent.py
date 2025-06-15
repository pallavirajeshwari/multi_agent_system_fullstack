import requests
import os

class WeatherAgent:
    """
    Retrieves weather data using the OpenWeatherMap API.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "your-api-key-here")  # Fallback for local dev
        if not self.api_key or self.api_key == "your-api-key-here":
            raise ValueError("OpenWeatherMap API key is missing. Set the OPENWEATHER_API_KEY environment variable.")

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
                },
                timeout=10  # add timeout for network resilience
            )
            response.raise_for_status()
            data = response.json()

            # Extract optional rain data and wind speed
            precipitation = data.get("rain", {}).get("1h", 0.0)  # mm in the last hour
            wind_speed = data.get("wind", {}).get("speed", 0.0)  # m/s

            return {
                "forecast": {
                    "precipitation": round(precipitation * 10, 1),  # convert mm to approx. % chance
                    "wind_speed": round(wind_speed * 3.6, 1)  # m/s to km/h
                }
            }

        except Exception as e:
            print(f"[WeatherAgent Error] {e}")
            return {
                "forecast": {
                    "precipitation": 0,
                    "wind_speed": 0,
                    "error": str(e)
                }
            }
