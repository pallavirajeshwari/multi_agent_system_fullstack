import logging

class PlannerAgent:
    ...

    def parse_goal(self, goal: str) -> list:
        goal = goal.lower()
        plan = []
        if "launch" in goal:
            plan.append("get_launch")
        if "weather" in goal:
            plan.append("get_weather")
        if "delay" in goal or "risk" in goal or "safe" in goal:
            plan.append("analyze_risk")
        logging.info(f"[PlannerAgent] Goal parsed into steps: {plan}")
        return plan

    def execute_plan(self, goal: str) -> dict:
        steps = self.parse_goal(goal)
        result = {}
        launch_data = None
        weather_data = None

        for step in steps:
            logging.info(f"[PlannerAgent] Executing step: {step}")
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

        logging.info(f"[PlannerAgent] Final result: {result}")
        return result
