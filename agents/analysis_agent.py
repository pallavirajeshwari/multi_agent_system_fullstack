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
