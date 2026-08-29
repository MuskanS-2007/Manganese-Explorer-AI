import pandas as pd


def classify_reserve_potential(reserve_score):
    """Classify reserve potential based on the calculated score."""

    if reserve_score >= 70:
        return "High"
    elif reserve_score >= 45:
        return "Medium"
    return "Low"


def analyze_reserves(df):
    """
    Analyze geological and real satellite/environmental indicators
    to prioritize manganese reserve locations.
    """

    if df is None or df.empty:
        raise ValueError("No geological data is available for analysis.")

    if "Location" not in df.columns:
        raise ValueError("Missing required column: Location")

    results = df.copy()

    score_components = []
    weights = []

    # ---------- GEOLOGICAL INDICATOR ----------
    if "Geological_Score" in results.columns:
        geological_score = pd.to_numeric(
            results["Geological_Score"],
            errors="coerce"
        ).clip(0, 100)

        if geological_score.notna().any():
            score_components.append(geological_score)
            weights.append(0.60)

    # ---------- SOIL / GEOCHEMICAL ANOMALY ----------
    if "Soil_Anomaly_Index" in results.columns:
        soil_score = (
            pd.to_numeric(
                results["Soil_Anomaly_Index"],
                errors="coerce"
            ).clip(0, 10)
            / 10
            * 100
        )

        if soil_score.notna().any():
            score_components.append(soil_score)
            weights.append(0.40)

    # ---------- REAL SATELLITE NDVI ----------
    if "GEE_NDVI" in results.columns:
        ndvi_score = (
            100
            - (
                pd.to_numeric(
                    results["GEE_NDVI"],
                    errors="coerce"
                ) - 0.45
            ).abs() * 200
        ).clip(0, 100)

        if ndvi_score.notna().any():
            score_components.append(ndvi_score)
            weights.append(0.15)

    # ---------- REAL NASA RAINFALL ----------
    if "NASA_Rainfall_mm" in results.columns:
        rainfall_score = (
            pd.to_numeric(
                results["NASA_Rainfall_mm"],
                errors="coerce"
            ).clip(0, 20)
            / 20
            * 100
        )

        if rainfall_score.notna().any():
            score_components.append(rainfall_score)
            weights.append(0.15)

    # ---------- CHECK AVAILABLE INDICATORS ----------
    if not score_components:
        raise ValueError(
            "The collected data does not contain usable numerical "
            "indicators for reserve analysis."
        )

    # ---------- WEIGHTED SCORE ----------
    weighted_sum = sum(
        component * weight
        for component, weight in zip(score_components, weights)
    )

    total_weight = sum(weights)

    results["Reserve_Potential_Score"] = (
        weighted_sum / total_weight
    ).clip(0, 100).round(1)

    results["Reserve_Potential"] = results[
        "Reserve_Potential_Score"
    ].apply(classify_reserve_potential)

    # ---------- RANK LOCATIONS ----------
    results = results.sort_values(
        by="Reserve_Potential_Score",
        ascending=False
    ).reset_index(drop=True)

    results["Reserve_Rank"] = results.index + 1

    return results