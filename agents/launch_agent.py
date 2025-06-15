import requests

class LaunchAgent:
    """
    Fetches next launch data from the SpaceX API and resolves launchpad location.
    """
    def get_next_launch(self) -> dict:
        try:
            # Get launch info
            response = requests.get("https://api.spacexdata.com/v4/launches/next")
            response.raise_for_status()
            launch = response.json()

            # Get launchpad info to resolve location
            launchpad_id = launch.get("launchpad", "")
            location = self.resolve_launchpad_location(launchpad_id)

            return {
                "name": launch.get("name", "Unknown"),
                "date": launch.get("date_utc", "Unknown"),
                "location": location or "Cape Canaveral"
            }
        except Exception as e:
            return {
                "name": "Unknown",
                "date": "Unknown",
                "location": "Cape Canaveral",
                "error": str(e)
            }

    def resolve_launchpad_location(self, launchpad_id: str) -> str:
        try:
            response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}")
            response.raise_for_status()
            launchpad = response.json()
            return launchpad.get("locality", "Cape Canaveral")
        except:
            return "Cape Canaveral"


class WeatherAgent:
    """
    Retrieves weather data for a given location using OpenWeatherMap API.
    """
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
