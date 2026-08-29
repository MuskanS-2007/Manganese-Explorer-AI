import pandas as pd


def generate_recommendations(df):
    results = df.copy()
    recommendations = []

    for _, row in results.iterrows():

        target = row.get("Target_Production", 0)
        actual = row.get("Actual_Production", 0)

        if target and target > 0:
            shortfall_percentage = max(
    0,
    ((target - actual) / target) * 100
)
        else:
            shortfall_percentage = 0

        prediction = row.get(
            "AI_Prediction",
            row.get("Reserve_Potential", "Medium")
        )

        if shortfall_percentage >= 15:
            recommendation = (
                "Critical production gap detected: inspect equipment, "
                "optimize operations, and allocate additional resources."
            )
            priority = "High"

        elif shortfall_percentage >= 10:
            recommendation = (
                "Moderate production shortfall: review operational efficiency "
                "and schedule preventive maintenance."
            )
            priority = "Medium"

        elif prediction == "High":
            recommendation = (
                "Strong reserve potential detected: prioritize detailed "
                "exploration and consider increasing resource allocation."
            )
            priority = "Medium"

        else:
            recommendation = (
                "Production is stable: continue monitoring operations "
                "and maintain current exploration activities."
            )
            priority = "Low"

        recommendations.append({
            "Recommendation": recommendation,
            "Action_Priority": priority
        })

    recommendation_df = pd.DataFrame(recommendations)

    return pd.concat(
        [results.reset_index(drop=True), recommendation_df],
        axis=1
    )