import pandas as pd


def calculate_exploration_score(row):
    """Calculate manganese reserve exploration potential."""
    score = (
        row["Manganese_Percentage"] * 1.2
        + row["Geological_Score"] * 0.8
        + row["Vegetation_Index"] * 10
    )
    return round(min(score, 100), 1)


def analyze_production_risk(row):
    """Analyze the risk of production shortfall."""
    shortfall = max(
        0,
        row["Production_Target_Tonnes"] - row["Actual_Production_Tonnes"]
    )

    shortfall_percentage = (shortfall / row["Production_Target_Tonnes"]) * 100

    risk_score = (
        shortfall_percentage * 2
        + row["Equipment_Downtime_Hours"] * 1.5
        + row["Blasting_Delay_Hours"] * 2
    )

    if risk_score >= 50:
        risk_level = "High"
    elif risk_score >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return round(shortfall_percentage, 1), round(risk_score, 1), risk_level


def generate_recommendation(row, risk_level):
    """Generate corrective recommendations based on constraints."""
    recommendations = []

    if row["Equipment_Downtime_Hours"] >= 12:
        recommendations.append("Schedule preventive maintenance and redeploy backup equipment")

    if row["Blasting_Delay_Hours"] >= 5:
        recommendations.append("Optimize blasting schedule and improve operational coordination")

    if row["Rainfall_mm"] >= 110:
        recommendations.append("Adjust mine schedule based on weather conditions")

    if risk_level == "High":
        recommendations.append("Prioritize immediate production recovery planning")

    if not recommendations:
        recommendations.append("Continue monitoring operations and maintain current plan")

    return "; ".join(recommendations)


def analyze_locations(data):
    """Analyze all locations and return enriched results."""
    results = data.copy()

    results["Exploration_Score"] = results.apply(
        calculate_exploration_score, axis=1
    )

    production_analysis = results.apply(
        analyze_production_risk, axis=1, result_type="expand"
    )
    production_analysis.columns = [
        "Shortfall_Percentage",
        "Production_Risk_Score",
        "Risk_Level"
    ]

    results = pd.concat([results, production_analysis], axis=1)

    results["Recommendation"] = results.apply(
        lambda row: generate_recommendation(row, row["Risk_Level"]),
        axis=1
    )

    return results