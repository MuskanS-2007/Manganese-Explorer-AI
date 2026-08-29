import pandas as pd


def analyze_shortfall(df):
    """
    Analyze production data and identify possible production shortfalls.
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
    )

    # Negative gap means production exceeded the target
    results["Production_Shortfall"] = results["Production_Shortfall"].clip(lower=0)

    # Calculate percentage shortfall
    results["Shortfall_Percentage"] = (
        results["Production_Shortfall"]
        / results["Target_Production"].replace(0, 1)
        * 100
    ).round(2)

    # Classify production risk
    def classify_risk(percentage):
        if percentage >= 30:
            return "High"
        elif percentage >= 15:
            return "Medium"
        return "Low"

    results["Shortfall_Risk"] = results["Shortfall_Percentage"].apply(
        classify_risk
    )

    return results, None