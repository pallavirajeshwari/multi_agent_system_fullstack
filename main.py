import json
from agents.planner import PlannerAgent
from agents.weather_agent import WeatherAgent
from agents.analysis_agent import AnalysisAgent
from agents.launch_agent import LaunchAgent

def run_goal(goal_text: str) -> dict:
    """
    Initializes agents and executes plan based on the user's goal.
    """
    # Initialize agents
    weather_agent = WeatherAgent()
    analysis_agent = AnalysisAgent()
    launch_agent = LaunchAgent()

    # Initialize planner with the agents
    planner = PlannerAgent(
        weather_agent=weather_agent,
        analysis_agent=analysis_agent,
        launch_agent=launch_agent
    )

    # Execute the plan
    return planner.execute_plan(goal_text)

# Optional CLI runner for local testing
if __name__ == "__main__":
    print("🚀 Multi-Agent System (CLI Mode)")
    while True:
        try:
            goal = input("\nEnter your goal (or type 'exit' to quit): ").strip()
            if goal.lower() == "exit":
                print("👋 Goodbye!")
                break

            result = run_goal(goal)
            print("\n✅ Plan Executed. Result:\n")
            print(json.dumps(result, indent=2))

        except Exception as e:
            print(f"\n❌ An error occurred:\n{e}")
