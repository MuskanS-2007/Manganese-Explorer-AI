import pandas as pd


def calculate_terrain_suitability(elevation, slope):
    """
    Calculate terrain suitability using real elevation and slope data.

    This is a prototype suitability indicator and does not confirm
    the presence of manganese ore.
    """

    if pd.isna(elevation) or pd.isna(slope):
        return None

    score = 100

    # Moderate terrain is generally more suitable for exploration access
    if slope > 30:
        score -= 40
    elif slope > 20:
        score -= 25
    elif slope > 10:
        score -= 10

    # Extremely high elevation can make exploration more difficult
    if elevation > 1500:
        score -= 20
    elif elevation > 1000:
        score -= 10

    return round(max(score, 0), 1)


def determine_geological_evidence(geological_score):
    """
    Classify geological evidence based on the available geological score.

    This is a prototype exploration indicator and does not confirm
    the presence of manganese ore.
    """

    if pd.isna(geological_score):
        return "Data Unavailable"

    if geological_score >= 85:
        return "Strong Geological Indicator"
    elif geological_score >= 70:
        return "Moderate Geological Indicator"
    else:
        return "Limited Geological Indicator"


def add_geological_evidence(df):
    """
    Add geological evidence and terrain suitability information.

    Geological evidence is presented as a supporting exploration
    indicator and does not confirm manganese mineral occurrence.
    """

    if df is None or df.empty:
        return df

    results = df.copy()

    # Generate geological evidence indicator from available geological data
    if "Geological_Score" in results.columns:
        results["Geological_Evidence"] = results[
            "Geological_Score"
        ].apply(determine_geological_evidence)
    else:
        results["Geological_Evidence"] = "Data Unavailable"

    # Calculate terrain suitability from elevation and slope data
    if (
        "GEE_Elevation_m" in results.columns
        and "GEE_Slope_Degrees" in results.columns
    ):
        results["Terrain_Suitability_Score"] = results.apply(
            lambda row: calculate_terrain_suitability(
                row["GEE_Elevation_m"],
                row["GEE_Slope_Degrees"]
            ),
            axis=1
        )
    else:
        results["Terrain_Suitability_Score"] = None

    return results