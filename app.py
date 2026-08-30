import streamlit as st
import folium
from streamlit_folium import st_folium

from services.reserve_service import analyze_reserves
from services.prediction_service import predict_reserve_potential
from services.shortfall_service import analyze_shortfall
from services.recommendation_service import generate_recommendations
from services.data_service import fetch_online_data
from services.geological_service import add_geological_evidence


# ==========================================
# SIH 2026 | MANGANESE EXPLORER AI
# Problem Statement ID: 26009
# ==========================================

st.set_page_config(
    page_title="Manganese Explorer AI",
    page_icon="⛏️",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("⛏️ Manganese Explorer AI")

st.subheader(
    "AI/ML & Space Technology for Manganese Reserve "
    "Identification and Production Intelligence"
)

st.success(
    "Smart India Hackathon 2026 | Problem Statement 26009 | "
    "Using AI/ML and Space Technology to Identify Manganese "
    "Reserves and Overcome Production Shortfalls"
)

st.divider()


# ==========================================
# INTRODUCTION
# ==========================================

st.header("🌍 Intelligent Manganese Decision Support System")

st.write("""
This platform integrates geological, satellite/space technology,
historical production, and operational data to support intelligent
decision-making for manganese exploration and mining operations.
""")


# ==========================================
# MAIN MODULES
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("🗺️ Reserve Identification")
    st.write(
        "Identify potential manganese reserve locations using "
        "geological and surface indicators."
    )

with col2:
    st.subheader("🤖 AI/ML Prediction")
    st.write(
        "Predict manganese reserve potential and classify locations "
        "based on available data."
    )

with col3:
    st.subheader("📉 Shortfall Prediction")
    st.write(
        "Identify possible production shortfalls using production "
        "and operational indicators."
    )

with col4:
    st.subheader("💡 Corrective Actions")
    st.write(
        "Provide intelligent recommendations to reduce production "
        "risks and improve continuity."
    )


st.divider()


# ==========================================
# RESERVE IDENTIFICATION & MAPPING
# ==========================================

st.header("🗺️ AI Reserve Identification & Mapping")

st.write(
    "Automatically analyze available geological, environmental, "
    "and satellite data to identify and prioritize potential "
    "manganese reserve locations."
)

st.info(
    "🛰️ Live Environmental Data: Recent precipitation data is "
    "retrieved from NASA based on the geographical coordinates "
    "of each analyzed location."
)


# ==========================================
# COMPLETE ANALYSIS PIPELINE
# ==========================================

if st.button("🔍 Run Complete Manganese Intelligence Analysis"):

    try:
        with st.spinner(
            "Fetching available data and running AI analysis..."
        ):

            # 1. Fetch data automatically
            data = fetch_online_data()

            # 2. Add geological evidence
            data = add_geological_evidence(data)

            # Store original analysis data
            st.session_state["analysis_data"] = data.copy()

            # 3. Reserve identification
            reserve_results = analyze_reserves(data)

            # IMPORTANT: Store reserve results for table and map
            st.session_state["reserve_results"] = (
                reserve_results.copy()
            )

            # 4. AI reserve prediction
            predicted_df, prediction_error = (
                predict_reserve_potential(reserve_results.copy())
            )

            if prediction_error:
                raise ValueError(prediction_error)

            st.session_state["predicted_df"] = predicted_df.copy()

            # 5. Production shortfall analysis
            shortfall_df, shortfall_error = (
                analyze_shortfall(predicted_df.copy())
            )

            if shortfall_error:
                raise ValueError(shortfall_error)

            st.session_state["shortfall_df"] = shortfall_df.copy()

            # 6. Smart recommendations
            recommendation_df = generate_recommendations(
                shortfall_df.copy()
            )

            st.session_state["recommendation_df"] = (
                recommendation_df.copy()
            )

        st.success(
            "✅ Complete manganese intelligence analysis completed!"
        )

    except Exception as error:
        st.error(f"❌ Analysis failed: {error}")


# ==========================================
# DISPLAY RESERVE IDENTIFICATION RESULTS
# ==========================================

reserve_results = st.session_state.get("reserve_results")

if reserve_results is not None and not reserve_results.empty:

    st.subheader("📍 Manganese Exploration Priority Locations")

    # Show important information in the main dashboard
    display_columns = [
        "Location",
       
        "GEE_NDVI",
        "NASA_Rainfall_mm",
        "Terrain_Suitability_Score",
        "Reserve_Potential"
    ]

    # Keep only columns that are available
    available_columns = [
        column for column in display_columns
        if column in reserve_results.columns
    ]

    display_results = reserve_results[available_columns].copy()

    display_results = display_results.rename(
        columns={
        "Reserve_Potential": "Exploration_Priority"
    }
)

    st.dataframe(
    display_results,
    width="stretch",
    hide_index=True
)

     # Optional detailed data section
    with st.expander("🔬 View Complete Satellite & Environmental Data"):

        detailed_results = reserve_results.copy()

        detailed_results = detailed_results.rename(
            columns={
                "Reserve_Potential": "Exploration_Priority",
                "Reserve_Potential_Score": "Exploration_Priority_Score"
            }
        )

        st.dataframe(
            detailed_results,
            width="stretch",
            hide_index=True
        )
else:
    st.info(
        "🔍 Run the Complete Manganese Intelligence Analysis "
        "to view potential reserve locations."
    )

# ==========================================
# AI/ML PREDICTION
# ==========================================

st.divider()

st.header("🤖 AI/ML Reserve Prediction")

st.write(
    "AI-assisted prediction of manganese reserve potential based on "
    "the analyzed geological and environmental data."
)

if "predicted_df" in st.session_state:

    predicted_df = st.session_state["predicted_df"]

    st.success(
        "AI reserve potential prediction completed successfully!"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "High Potential Predictions",
            int(
                (predicted_df["AI_Prediction"] == "High").sum()
            )
        )

    with col2:
        st.metric(
            "Average Predicted Score",
            f'{predicted_df["Predicted_Reserve_Score"].mean():.1f}'
        )

    st.subheader("🤖 AI Prediction Results")

    display_columns = [
        "Location",
        "Predicted_Reserve_Score",
        "AI_Prediction"
    ]

    available_columns = [
        column for column in display_columns
        if column in predicted_df.columns
    ]

    st.dataframe(
        predicted_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

    if (
        "Location" in predicted_df.columns
        and "Predicted_Reserve_Score" in predicted_df.columns
    ):

        st.subheader("📊 Predicted Reserve Potential")

        chart_data = predicted_df.set_index("Location")[
            "Predicted_Reserve_Score"
        ]

        st.bar_chart(chart_data)

else:
    st.info(
        "🔍 Run the Complete Manganese Intelligence Analysis "
        "to generate AI predictions."
    )


# ==========================================
# PRODUCTION SHORTFALL PREDICTION
# ==========================================

st.divider()

st.header("📉 Production Shortfall Prediction")

st.write(
    "Analyze production performance to identify potential shortfalls "
    "and operational risks."
)

if "shortfall_df" in st.session_state:

    shortfall_df = st.session_state["shortfall_df"]

    st.success(
        "Production shortfall analysis completed successfully!"
    )

    if "Production_Shortfall" in shortfall_df.columns:
        total_shortfall = (
            shortfall_df["Production_Shortfall"].sum()
        )
    else:
        total_shortfall = 0

    if "Shortfall_Risk" in shortfall_df.columns:
        high_risk_count = (
            shortfall_df["Shortfall_Risk"] == "High"
        ).sum()
    else:
        high_risk_count = 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Production Shortfall",
            f"{total_shortfall:.2f}"
        )

    with col2:
        st.metric(
            "High-Risk Locations",
            int(high_risk_count)
        )

    st.subheader("⚠️ Production Shortfall Results")

    display_columns = [
        "Location",
        "Target_Production",
        "Actual_Production",
        "Production_Shortfall",
        "Shortfall_Percentage",
        "Shortfall_Risk"
        "Risk_Alert"
    ]

    available_columns = [
        column for column in display_columns
        if column in shortfall_df.columns
    ]

    st.dataframe(
        shortfall_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

    if (
        "Location" in shortfall_df.columns
        and "Production_Shortfall" in shortfall_df.columns
    ):

        st.subheader("📊 Production Shortfall by Location")

        chart_data = shortfall_df.set_index("Location")[
            "Production_Shortfall"
        ]

        st.bar_chart(chart_data)

else:
    st.info(
        "🔍 Run the Complete Manganese Intelligence Analysis "
        "to analyze production shortfalls."
    )


# ==========================================
# CORRECTIVE ACTIONS & SMART RECOMMENDATIONS
# ==========================================

st.divider()

st.header("💡 Corrective Actions & Smart Recommendations")

st.write(
    "AI-supported recommendations based on production performance "
    "and manganese reserve potential."
)

if "recommendation_df" in st.session_state:

    recommendation_df = st.session_state["recommendation_df"]

    st.success(
        "Smart recommendations generated successfully!"
    )

    if "Action_Priority" in recommendation_df.columns:

        high_priority = (
            recommendation_df["Action_Priority"] == "High"
        ).sum()

        medium_priority = (
            recommendation_df["Action_Priority"] == "Medium"
        ).sum()

        low_priority = (
            recommendation_df["Action_Priority"] == "Low"
        ).sum()

    else:
        high_priority = 0
        medium_priority = 0
        low_priority = 0

    col1, col2, col3 = st.columns(3)

    col1.metric("🔴 High Priority Actions", int(high_priority))
    col2.metric("🟡 Medium Priority Actions", int(medium_priority))
    col3.metric("🟢 Low Priority Actions", int(low_priority))

    st.subheader("📋 Recommended Actions by Location")

    display_columns = [
        "Location",
        "Recommendation",
        "Action_Priority"
    ]

    available_columns = [
        column for column in display_columns
        if column in recommendation_df.columns
    ]

    st.dataframe(
        recommendation_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "🔍 Run the Complete Manganese Intelligence Analysis "
        "to generate smart recommendations."
    )


# ==========================================
# INTEGRATED INTELLIGENCE DASHBOARD
# ==========================================

st.divider()

st.header("📊 Integrated Intelligence Dashboard")

st.info(
    "Unified overview of manganese reserve potential, production "
    "performance, and AI-supported corrective actions."
)

dashboard_data = st.session_state.get("analysis_data")

if dashboard_data is not None:

    total_locations = len(dashboard_data)
    high_reserve_count = 0
    high_production_risk = 0
    priority_actions_count = 0

    # Reserve prediction metrics
    if "predicted_df" in st.session_state:

        predicted_df = st.session_state["predicted_df"]

        if "AI_Prediction" in predicted_df.columns:
            high_reserve_count = (
                predicted_df["AI_Prediction"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("high")
                .sum()
            )

    # Production risk metrics
    if "shortfall_df" in st.session_state:

        shortfall_df = st.session_state["shortfall_df"]

        if "Shortfall_Risk" in shortfall_df.columns:
            high_production_risk = (
                shortfall_df["Shortfall_Risk"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("high")
                .sum()
            )

    # Recommendation metrics
    if "recommendation_df" in st.session_state:

        recommendation_df = st.session_state["recommendation_df"]

        if "Action_Priority" in recommendation_df.columns:
            priority_actions_count = (
                recommendation_df["Action_Priority"]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["high", "medium"])
                .sum()
            )

    # ---------- METRIC CARDS ----------

    st.subheader("📌 Overall Analysis Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📍 Locations Analyzed", total_locations)

    with col2:
        st.metric(
            "🟢 High Reserve Potential",
            int(high_reserve_count)
        )

    with col3:
        st.metric(
            "⚠️ High Production Risk",
            int(high_production_risk)
        )

    with col4:
        st.metric(
            "💡 Priority Actions",
            int(priority_actions_count)
        )
        # ---------- LOCATION-WISE INTELLIGENCE ----------

    st.divider()
    st.subheader("🎯 Location-wise Intelligence Summary")

    if (
        "predicted_df" in st.session_state
        and "shortfall_df" in st.session_state
        and "recommendation_df" in st.session_state
    ):

        intelligence_df = st.session_state[
            "recommendation_df"
        ].copy()

        display_columns = [
            "Location",
            "AI_Prediction",
            "Predicted_Reserve_Score",
            "Shortfall_Percentage",
            "Shortfall_Risk",
            "Action_Priority",
            "Recommendation"
        ]

        available_columns = [
            column for column in display_columns
            if column in intelligence_df.columns
        ]

        st.dataframe(
            intelligence_df[available_columns],
            width="stretch",
            hide_index=True
        )

    else:
        st.info(
            "Complete intelligence results will appear here "
            "after running the analysis."
        )
    # ---------- VISUALIZATIONS ----------

    st.divider()
    st.subheader("📈 Integrated Analysis Visualizations")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        if "predicted_df" in st.session_state:

            predicted_df = st.session_state["predicted_df"]

            if (
                "Location" in predicted_df.columns
                and "Predicted_Reserve_Score"
                in predicted_df.columns
            ):
                st.caption("🗺️ Reserve Potential by Location")

                st.bar_chart(
                    predicted_df.set_index("Location")[
                        "Predicted_Reserve_Score"
                    ]
                )

        else:
            st.info(
                "Reserve prediction results will appear here."
            )

    with chart_col2:

        if "shortfall_df" in st.session_state:

            shortfall_df = st.session_state["shortfall_df"]

            if (
                "Location" in shortfall_df.columns
                and "Production_Shortfall"
                in shortfall_df.columns
            ):
                st.caption("📉 Production Shortfall by Location")

                st.bar_chart(
                    shortfall_df.set_index("Location")[
                        "Production_Shortfall"
                    ]
                )

        else:
            st.info(
                "Production shortfall results will appear here."
            )

else:
    st.warning(
        "🔍 Run the analysis to unlock the Integrated "
        "Intelligence Dashboard."
    )


# ==========================================
# INTERACTIVE MAP VIEW
# ==========================================

st.divider()

st.header("🗺️ Geographical Intelligence Map")

st.write(
    "Interactive visualization of analyzed manganese locations "
    "across India."
)

map_data = st.session_state.get("recommendation_df")

if (
    map_data is not None
    and not map_data.empty
    and "Latitude" in map_data.columns
    and "Longitude" in map_data.columns
):

    # Center map around analyzed locations
    map_center = [
        map_data["Latitude"].mean(),
        map_data["Longitude"].mean()
    ]

    manganese_map = folium.Map(
        location=map_center,
        zoom_start=5,
        tiles="OpenStreetMap"
    )

    # Add a marker for every location
    for _, row in map_data.iterrows():

        location_name = row.get(
            "Location",
            "Unknown Location"
        )

        reserve_potential = row.get(
            "Reserve_Potential",
            "Not Available"
        )

        reserve_score = row.get(
            "Reserve_Potential_Score",
            "Not Available"
        )

        popup_text = f"""
        <b>📍 {location_name}</b><br>
        🟢 <b>Reserve Potential:</b> {reserve_potential}<br>
        📊 <b>Reserve Score:</b> {reserve_score}<br>
        """

        folium.Marker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            popup=folium.Popup(
                popup_text,
                max_width=300
            ),
            tooltip=location_name
        ).add_to(manganese_map)

    st_folium(
        manganese_map,
        width=None,
        height=500,
        returned_objects=[]
    )

    st.caption(
        "📍 Click any marker to view geological intelligence "
        "for that location."
    )

else:
    st.info(
        "🔍 Run the Complete Manganese Intelligence Analysis "
        "to view the geographical intelligence map."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "SIH Prototype | Manganese Explorer AI | "
    "Ministry of Steel | MOIL Ltd."
)