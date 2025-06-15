import requests

class WeatherAgent:
    """
    Retrieves weather data using Open-Meteo API.
    """
    def get_weather(self, location_name: str) -> dict:
        lat, lon = 28.5623, -80.5774  # Hardcoded for Cape Canaveral as fallback
        try:
            res = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                f"&daily=precipitation_probability_max,windspeed_10m_max&timezone=auto"
            )
            data = res.json()
            return {
                "forecast": {
                    "precipitation": data["daily"]["precipitation_probability_max"][0],
                    "wind_speed": data["daily"]["windspeed_10m_max"][0]
                }
            }
        except Exception as e:
            return {"forecast": {"precipitation": 0, "wind_speed": 0}}
