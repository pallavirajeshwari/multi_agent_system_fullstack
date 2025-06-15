import requests
import os

class WeatherAgent:
 
    def __init__(self):
        self.geocoder_api_key = os.getenv("OPENCAGE_API_KEY")  # Store your API key as env var

    def get_coordinates(self, location_name: str):
        try:
            response = requests.get(
                f"https://api.opencagedata.com/geocode/v1/json?q={location_name}&key={self.geocoder_api_key}"
            )
            response.raise_for_status()
            data = response.json()

            if data["results"]:
                geometry = data["results"][0]["geometry"]
                return geometry["lat"], geometry["lng"]

        except Exception as e:
            print(f"[Geocode Error] {e}")
        # Fallback to Cape Canaveral
        return 28.5623, -80.5774

    def get_weather_for_location(self, location_name: str) -> dict:
        lat, lon = self.get_coordinates(location_name)

        try:
            res = requests.get(
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}"
                f"&daily=precipitation_probability_max,windspeed_10m_max"
                f"&timezone=auto"
            )
            res.raise_for_status()
            data = res.json()

            return {
                "forecast": {
                    "precipitation": data["daily"]["precipitation_probability_max"][0],
                    "wind_speed": data["daily"]["windspeed_10m_max"][0]
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
