import requests

class LaunchAgent:
    """
    Fetches next launch data from the SpaceX API.
    """
    def get_next_launch(self) -> dict:
        try:
            response = requests.get("https://api.spacexdata.com/v4/launches/next")
            response.raise_for_status()
            launch = response.json()

            return {
                "name": launch.get("name", "Unknown"),
                "date": launch.get("date_utc", "Unknown"),
                "location": launch.get("launchpad", "5e9e4502f509094188566f88")  # Default launchpad ID
            }
        except Exception as e:
            return {
                "name": "Unknown",
                "date": "Unknown",
                "location": "5e9e4502f509094188566f88",
                "error": str(e)
            }
