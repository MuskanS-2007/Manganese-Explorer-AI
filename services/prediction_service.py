import pandas as pd


def predict_reserve_potential(df):
    """
    Predict reserve potential using available geological
    and environmental indicators.
    """

    results = df.copy()

    if "Reserve_Potential_Score" in results.columns:
        score = results["Reserve_Potential_Score"]
    elif "Geological_Score" in results.columns:
        score = results["Geological_Score"]
    else:
        return None, "No suitable data available for prediction."

    results["Predicted_Reserve_Score"] = score.clip(0, 100)

    def classify_prediction(value):
        if value >= 70:
            return "High"
        elif value >= 40:
            return "Medium"
        return "Low"

    results["AI_Prediction"] = results[
        "Predicted_Reserve_Score"
    ].apply(classify_prediction)

    return results, None