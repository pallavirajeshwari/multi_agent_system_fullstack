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
        """
        Parses the user's goal and returns a list of action steps.
        """
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
        """
        Executes the plan generated from the goal.
        """
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
                    result["launch"] = launch_data  # ensure launch info is returned
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
