class AnalysisAgent:
    """
    Assesses launch delay risk based on weather conditions.
    """

    def analyze(self, weather: dict) -> dict:
        forecast = weather.get("forecast", {})
        precip = forecast.get("precipitation", 0)
        wind = forecast.get("wind_speed", 0)

        risk = "Low"
        reasons = []

        # Evaluate precipitation risk
        if precip > 50:
            risk = "High"
            reasons.append(f"High precipitation probability: {precip}%")
        elif precip > 30:
            risk = "Medium"
            reasons.append(f"Moderate precipitation probability: {precip}%")

        # Evaluate wind risk (escalate only if not already High)
        if wind > 40:
            risk = "High"
            reasons.append(f"High wind speed: {wind} km/h")
        elif wind > 25 and risk != "High":
            risk = "Medium"
            reasons.append(f"Moderate wind speed: {wind} km/h")

        return {
            "risk": risk,
            "reasons": reasons if reasons else ["Weather conditions appear favorable."]
        }

    # Alias for compatibility
    analyze_risk = analyze
