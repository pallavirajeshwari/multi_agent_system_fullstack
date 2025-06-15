import requests
import os

class WeatherAgent:
    """
    Retrieves weather data based on a location using OpenCage (for geocoding)
    and Open-Meteo (for weather forecast).
    """
    def __init__(self):
        self.geocoder_api_key = os.getenv("OPENCAGE_API_KEY")  # Store in .env for security

    def get_coordinates(self, location_name: str):
        """
        Converts a location name into latitude and longitude using OpenCage API.
        Falls back to Cape Canaveral if lookup fails.
        """
        try:
            response = requests.get(
                f"https://api.opencagedata.com/geocode/v1/json",
                params={"q": location_name, "key": self.geocoder_api_key}
            )
            response.raise_for_status()
            data = response.json()

            if data.get("results"):
                geometry = data["results"][0]["geometry"]
                return geometry["lat"], geometry["lng"]
            else:
                print(f"[Geocode Warning] No results found for: {location_name}")
        except Exception as e:
            print(f"[Geocode Error] {e}")

        print("[Fallback] Using default coordinates for Cape Canaveral.")
        return 28.5623, -80.5774  # Default: Cape Canaveral

    def get_weather_for_location(self, location_name: str) -> dict:
        """
        Fetches weather forecast for a given location.
        """
        lat, lon = self.get_coordinates(location_name)

        try:
            res = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "precipitation_probability_max,windspeed_10m_max",
                    "timezone": "auto"
                }
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
            print(f"[Weather API Error] {e}")
            return {
                "forecast": {
                    "precipitation": 0,
                    "wind_speed": 0,
                    "error": str(e)
                }
            }
