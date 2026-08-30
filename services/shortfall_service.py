import pandas as pd


def analyze_shortfall(df):
    """
    Analyze production performance and predict production
    shortfall risk using available production indicators.
    """

    required_columns = ["Target_Production", "Actual_Production"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return None, f"Missing required columns: {', '.join(missing_columns)}"

    results = df.copy()

    # Calculate production gap
    results["Production_Shortfall"] = (
        results["Target_Production"] - results["Actual_Production"]
    ).clip(lower=0)

    # Calculate shortfall percentage
    results["Shortfall_Percentage"] = (
        results["Production_Shortfall"]
        / results["Target_Production"].replace(0, 1)
        * 100
    ).round(2)

    # Predict production risk level
    def classify_risk(row):
        percentage = row["Shortfall_Percentage"]

        if percentage >= 30:
            return "High"
        elif percentage >= 15:
            return "Medium"
        return "Low"

    results["Shortfall_Risk"] = results.apply(
        classify_risk,
        axis=1
    )

    # Early warning status for decision makers
    def get_alert(risk):
        if risk == "High":
            return "Immediate corrective action required"
        elif risk == "Medium":
            return "Production risk detected - monitoring required"
        return "Production performance within acceptable range"

    results["Risk_Alert"] = results["Shortfall_Risk"].apply(
        get_alert
    )

    return results, None