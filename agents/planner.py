# planner.py
class PlannerAgent:
    """
    Coordinates tasks between agents based on the user goal.
    Determines a sequence of actions (launch, weather, risk analysis) and executes them.
    """
    def __init__(self, weather_agent, analysis_agent, launch_agent):
        self.weather_agent = weather_agent
        self.analysis_agent = analysis_agent
        self.launch_agent = launch_agent

    def parse_goal(self, goal: str) -> list:
        goal = goal.lower()
        plan = []
        if "launch" in goal:
            plan.append("get_launch")
        if "weather" in goal:
            plan.append("get_weather")
        if "delay" in goal or "risk" in goal or "safe" in goal:
            plan.append("analyze_risk")
        return plan

    def execute_plan(self, goal: str) -> dict:
        steps = self.parse_goal(goal)
        result = {}
        launch_data = None
        weather_data = None

        for step in steps:
            if step == "get_launch":
                launch_data = self.launch_agent.get_next_launch()
                result["launch"] = launch_data

            elif step == "get_weather":
                if not launch_data:
                    launch_data = self.launch_agent.get_next_launch()
                    result["launch"] = launch_data
                weather_data = self.weather_agent.get_weather_for_location(launch_data["location"])
                result["weather"] = weather_data

            elif step == "analyze_risk":
                if not weather_data:
                    if not launch_data:
                        launch_data = self.launch_agent.get_next_launch()
                        result["launch"] = launch_data
                    weather_data = self.weather_agent.get_weather_for_location(launch_data["location"])
                    result["weather"] = weather_data
                risk_summary = self.analysis_agent.analyze_risk(weather_data)
                result["risk_analysis"] = risk_summary

        return result


# launch_agent.py
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


# weather_agent.py
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


# analysis_agent.py
class AnalysisAgent:
    def analyze_risk(self, weather_data: dict) -> dict:
        forecast = weather_data.get("forecast", {})
        precipitation = forecast.get("precipitation", 0)
        wind_speed = forecast.get("wind_speed", 0)

        risk = "Low"
        if precipitation > 2 or wind_speed > 10:
            risk = "High"
        elif precipitation > 0.5 or wind_speed > 5:
            risk = "Moderate"

        return {
            "precipitation": precipitation,
            "wind_speed": wind_speed,
            "risk_level": risk
        }


# main.py
import json
import logging
from dotenv import load_dotenv
from agents.planner import PlannerAgent
from agents.weather_agent import WeatherAgent
from agents.analysis_agent import AnalysisAgent
from agents.launch_agent import LaunchAgent

load_dotenv()
logging.basicConfig(level=logging.INFO)

def run_goal(goal_text: str) -> dict:
    weather_agent = WeatherAgent()
    analysis_agent = AnalysisAgent()
    launch_agent = LaunchAgent()

    planner = PlannerAgent(
        weather_agent=weather_agent,
        analysis_agent=analysis_agent,
        launch_agent=launch_agent
    )

    return planner.execute_plan(goal_text)

if __name__ == "__main__":
    print("\U0001F680 Multi-Agent System (CLI Mode)")
    while True:
        try:
            goal = input("\nEnter your goal (or type 'exit' to quit): ").strip()
            if goal.lower() == "exit":
                print("\U0001F44B Goodbye!")
                break

            result = run_goal(goal)
            print("\n✅ Plan Executed. Result:\n")
            print(json.dumps(result, indent=2) if result else "⚠️ No data returned.")

        except Exception as e:
            print(f"\n❌ An error occurred:\n{e}")
