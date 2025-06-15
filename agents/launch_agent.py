import requests

class LaunchAgent:
    def get_next_launch(self) -> dict:
        try:
            response = requests.get("https://api.spacexdata.com/v4/launches/next")
            response.raise_for_status()
            launch = response.json()
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
