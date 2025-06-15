import json
from agents.planner import PlannerAgent
from agents.weather_agent import WeatherAgent
from agents.analysis_agent import AnalysisAgent
from agents.launch_agent import LaunchAgent

def run_goal(goal_text):
    # Initialize all agents
    weather_agent = WeatherAgent()
    analysis_agent = AnalysisAgent()
    launch_agent = LaunchAgent()
    
    # Initialize planner with the agents
    planner = PlannerAgent(weather_agent, analysis_agent, launch_agent)
    
    # Run the plan
    result = planner.execute_plan(goal_text)
    return result

# Optional for local testing
if __name__ == "__main__":
    print("🤖 Multi-Agent System (Local CLI Mode)")
    while True:
        try:
            user_input = input("\nEnter your goal (or type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            response = run_goal(user_input)
            print("=== Result ===")
            print(json.dumps(response, indent=2))
        except Exception as e:
            print(f"❌ Error: {e}")
