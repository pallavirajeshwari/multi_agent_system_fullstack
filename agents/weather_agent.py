import requests

class WeatherAgent:
    """
    Retrieves weather data using Open-Meteo API.
    """
    def get_weather_for_location(self, location_name: str) -> dict:
        # Fallback to Cape Canaveral coordinates
        lat, lon = 28.5623, -80.5774

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
