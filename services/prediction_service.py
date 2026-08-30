import pandas as pd


def predict_reserve_potential(df):
    """
    Predict and classify exploration potential using the
    calculated reserve potential score.

    This prediction is a decision-support indicator and does
    not confirm the presence of manganese reserves.
    """

    if df is None or df.empty:
        return None, "No data available for prediction."

    if "Reserve_Potential_Score" not in df.columns:
        return None, (
            "Reserve potential analysis must be completed "
            "before prediction."
        )

    results = df.copy()

    score = pd.to_numeric(
        results["Reserve_Potential_Score"],
        errors="coerce"
    ).clip(0, 100)

    results["Predicted_Reserve_Score"] = score.round(1)

    def classify_prediction(value):
        if pd.isna(value):
            return "Not Available"
        elif value >= 70:
            return "High"
        elif value >= 45:
            return "Medium"
        return "Low"

    results["AI_Prediction"] = results[
        "Predicted_Reserve_Score"
    ].apply(classify_prediction)

    return results, None