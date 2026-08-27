import streamlit as st
import pandas as pd
# =========================
# EXPLORATION SCORE MODEL
# =========================

def calculate_exploration_score(mn, geological, anomaly):
    
    # Normalize each indicator and apply weights
    mn_score = min((mn / 40) * 50, 50)
    geological_score = min((geological / 100) * 30, 30)
    anomaly_score = min((anomaly / 10) * 20, 20)

    total_score = (
        mn_score
        + geological_score
        + anomaly_score
    )

    return round(total_score, 1)

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Manganese Explorer AI",
    page_icon="🔬",
    layout="wide"
)


# =========================
# TITLE SECTION
# =========================

st.title("🔬 Manganese Explorer AI")
st.subheader("AI-Powered Manganese Exploration & Analysis System")
st.success("Welcome! Explore manganese resources using intelligent data analysis.")

st.divider()


# =========================
# MAIN FEATURE SECTIONS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("📍 Location Analysis")
    st.write("Analyze locations using uploaded geological data.")
    if st.button("Analyze Location"):
        st.session_state["show_location"] = True

with col2:
    st.header("📊 Data Analysis")
    st.write("Upload and analyze geological and exploration data.")
    if st.button("Analyze Data"):
        st.session_state["show_data"] = True

with col3:
    st.header("🤖 AI Prediction")
    st.write("Predict manganese exploration potential using geological data.")
    if st.button("Start Prediction"):
        st.session_state["show_prediction"] = True

with col4:
    st.header("📊 Compare")
    st.write("Compare exploration potential between locations.")
    if st.button("Compare Locations"):
        st.session_state["show_compare"] = True


# =========================
# EXPLORATION DASHBOARD BUTTON
# =========================

st.divider()

st.header("📊 Exploration Dashboard")
st.write("View an overall summary of manganese exploration data and recommendations.")

if st.button("Open Dashboard"):
    st.session_state["show_dashboard"] = True


# =========================
# PROJECT WORKFLOW
# =========================

st.divider()

st.header("🔄 How Manganese Explorer AI Works")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.subheader("1️⃣ Upload Data")
    st.write("Upload geological and manganese exploration data in CSV format.")

with step2:
    st.subheader("2️⃣ Analyze")
    st.write("Analyze manganese concentration and geological indicators.")

with step3:
    st.subheader("3️⃣ AI Prediction")
    st.write("Generate exploration potential predictions for each location.")

with step4:
    st.subheader("4️⃣ Recommend")
    st.write("Rank locations and identify the best areas for exploration.")

st.info(
    "💡 **Our Goal:** Support data-driven decision-making for efficient "
    "and sustainable manganese exploration."
)


# =========================
# EXPLORATION RANKING BUTTON
# =========================

st.divider()

st.header("🏆 Smart Exploration Ranking")
st.write(
    "Rank all uploaded locations and identify the highest-priority "
    "areas for manganese exploration."
)

if st.button("View Exploration Ranking"):
    st.session_state["show_ranking"] = True


# =========================
# LOCATION ANALYSIS
# =========================

if st.session_state.get("show_location", False):

    st.divider()
    st.header("📍 Location Analysis")

    st.write(
        "Select a location from the uploaded geological dataset to "
        "generate a data-driven exploration assessment."
    )

    if "dataset" not in st.session_state:

        st.warning(
            "📊 Please upload geological data first using the Data Analysis section."
        )

    else:

        df = st.session_state["dataset"]

        if "Location" not in df.columns:

            st.error("❌ The dataset must contain a 'Location' column.")

        else:

            locations = df["Location"].dropna().unique()

            selected_location = st.selectbox(
                "Select a location:",
                locations,
                key="analysis_location"
            )

            if st.button("Check Manganese Potential"):

                row = df[
                    df["Location"] == selected_location
                ].iloc[0]

                mn = float(row.get("Mn_Percentage", 0))
                geological = float(row.get("Geological_Score", 0))
                anomaly = float(row.get("Soil_Anomaly_Index", 0))

                exploration_score = (
                    mn * 1.2
                    + geological * 0.8
                    + anomaly * 2
                )

                exploration_score = min(
                    round(exploration_score, 1),
                    100
                )

                if exploration_score >= 70:

                    priority = "High"
                    confidence = min(
                        round(70 + exploration_score * 0.25, 1),
                        95
                    )
                    recommendation = (
                        "Strong exploration indicators are present. "
                        "Detailed geological surveys and field validation "
                        "are recommended as the next step."
                    )

                elif exploration_score >= 45:

                    priority = "Medium"
                    confidence = min(
                        round(60 + exploration_score * 0.3, 1),
                        90
                    )
                    recommendation = (
                        "Moderate exploration indicators are present. "
                        "Additional sampling and geological investigation "
                        "are recommended."
                    )

                else:

                    priority = "Low"
                    confidence = min(
                        round(50 + exploration_score * 0.35, 1),
                        80
                    )
                    recommendation = (
                        "Limited exploration indicators are currently available. "
                        "Further investigation should be based on additional "
                        "supporting geological evidence."
                    )

                st.success(f"✅ Analysis completed for {selected_location}!")

                score_col, priority_col, confidence_col = st.columns(3)

                with score_col:
                    st.metric(
                        "Exploration Potential Score",
                        f"{exploration_score}/100"
                    )

                with priority_col:
                    st.metric("Exploration Priority", priority)

                with confidence_col:
                    st.metric(
                        "Assessment Confidence",
                        f"{confidence}%"
                    )

                st.subheader("🔬 Geological Indicators Used")

                ind1, ind2, ind3 = st.columns(3)

                with ind1:
                    st.metric("Manganese %", f"{mn}%")

                with ind2:
                    st.metric("Geological Score", geological)

                with ind3:
                    st.metric("Soil Anomaly Index", anomaly)

                st.subheader("💡 Exploration Recommendation")
                st.write(recommendation)

                st.caption(
                    "Assessment is calculated from the geological indicators "
                    "available in the uploaded dataset and should be validated "
                    "through field surveys."
                )


# =========================
# DATA ANALYSIS
# =========================

if st.session_state.get("show_data", False):

    st.divider()
    st.header("📊 Geological Data Analysis")

    st.write(
        "Upload geological or exploration data in CSV format "
        "for preliminary analysis."
    )

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.session_state["dataset"] = df

        st.success("✅ Data uploaded successfully!")

        st.subheader("📄 Data Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Dataset Summary")
        st.write(f"**Number of records:** {len(df)}")
        st.write(f"**Number of columns:** {len(df.columns)}")

        if st.button("Run Data Analysis"):

            st.info("🔍 Analyzing geological dataset...")

            st.subheader("📋 Analysis Results")
            st.dataframe(
                df.describe(include="all"),
                use_container_width=True
            )

            st.success("✅ Data analysis completed!")

            st.subheader("💡 Key Insights")

            insight1, insight2, insight3 = st.columns(3)

            if "Mn_Percentage" in df.columns:

                average_mn = df["Mn_Percentage"].mean()
                highest_row = df.loc[df["Mn_Percentage"].idxmax()]

                with insight1:
                    st.metric(
                        "Average Manganese %",
                        f"{average_mn:.2f}%"
                    )

                with insight2:
                    if "Location" in df.columns:
                        st.metric(
                            "Highest Manganese Location",
                            str(highest_row["Location"])
                        )

            if "Exploration_Potential" in df.columns:

                high_count = (
                    df["Exploration_Potential"]
                    .astype(str)
                    .str.lower()
                    .eq("high")
                    .sum()
                )

                with insight3:
                    st.metric(
                        "High Potential Locations",
                        int(high_count)
                    )

            if (
                "Location" in df.columns
                and "Mn_Percentage" in df.columns
            ):

                st.subheader("📊 Manganese Percentage by Location")

                chart_data = df.set_index("Location")["Mn_Percentage"]
                st.bar_chart(chart_data)

            st.success("🚀 Insights generated successfully!")
## ==============================
# AI PREDICTION MODULE
# ==============================

if st.session_state.get("show_prediction", False):

    st.divider()
    st.header("🤖 AI Prediction Engine")

    st.write(
        "Select a location from the uploaded geological dataset to generate an "
        "exploration potential prediction."
    )

    if "dataset" not in st.session_state:
        st.warning("📁 Please upload geological data first using the Data Analysis section.")

    else:
        df = st.session_state["dataset"]

        if "Location" not in df.columns:
            st.error("❌ The dataset must contain a 'Location' column.")

        else:
            selected_location = st.selectbox(
                "Select a location for prediction:",
                df["Location"].dropna().unique(),
                key="prediction_location"
            )

            if st.button("Generate AI Prediction"):

                row = df[
                    df["Location"] == selected_location
                ].iloc[0]

                # Get geological indicators safely
                mn = float(row.get("Mn_Percentage", 0))
                geological = float(row.get("Geological_Score", 0))
                anomaly = float(row.get("Soil_Anomaly_Index", 0))

                # Calculate exploration score
                prediction_score = calculate_exploration_score(
                    mn,
                    geological,
                    anomaly
                )

                # Determine exploration potential
                if prediction_score >= 70:
                    potential = "High"
                    recommendation = (
                        "Strong indicators detected. Prioritize this location "
                        "for detailed geological surveys and field validation."
                    )

                elif prediction_score >= 45:
                    potential = "Medium"
                    recommendation = (
                        "Moderate potential detected. Additional sampling and "
                        "geological investigation are recommended."
                    )

                else:
                    potential = "Low"
                    recommendation = (
                        "Limited indicators detected. Consider further exploration "
                        "only where additional supporting evidence is available."
                    )

                # Calculate confidence
                confidence = min(
                    95,
                    round(50 + (prediction_score * 0.35), 1)
                )

                # Display prediction
                st.success("📊 Prediction Generated Successfully!")

                pred1, pred2, pred3 = st.columns(3)

                with pred1:
                    st.metric(
                        "Predicted Potential",
                        potential
                    )

                with pred2:
                    st.metric(
                        "Prediction Score",
                        f"{prediction_score}/100"
                    )

                with pred3:
                    st.metric(
                        "Model Confidence",
                        f"{confidence}%"
                    )

                st.subheader("🔬 AI Exploration Recommendation")
                st.write(recommendation)

                
                # =========================
                # EXPLAINABLE AI SECTION
                # =========================

                st.divider()
                st.subheader("🧠 How the Prediction Works")

                explain1, explain2, explain3 = st.columns(3)

                with explain1:
                    st.metric("🟢 Manganese %", f"{mn}%")
                    st.caption(
                        "Indicates manganese mineral concentration."
                    )

                with explain2:
                    st.metric("🟠 Geological Score", geological)
                    st.caption(
                        "Represents geological suitability."
                    )

                with explain3:
                    st.metric("🔵 Soil Anomaly Index", anomaly)
                    st.caption(
                        "Represents mineral-related soil anomalies."
                    )

                st.info(
                    "🧠 **Model Analysis:** The system combines these "
                    "geological indicators using a transparent weighted scoring "
                    "model and classifies the location as Low, Medium, or High "
                    "exploration potential."
                )

                st.caption(
                    "This is a decision-support prediction based on the uploaded "
                    "dataset and should be validated through detailed surveys "
                    "and field investigation."
                )
                # ==============================
# GEOLOGICAL CONTEXT
# ==============================

            if (
                "dataset" in st.session_state
                and "prediction_location" in st.session_state
            ):

                df_context = st.session_state["dataset"]
                context_location = st.session_state["prediction_location"]

                context_rows = df_context[
                    df_context["Location"] == context_location
                ]

                if not context_rows.empty:

                    row = context_rows.iloc[0]

                    st.divider()
                    st.subheader("📂 Geological Context & Data Transparency")

                    if "Geological_Context" in df_context.columns:
                        st.info(row["Geological_Context"])

                    if "Official_Reference" in df_context.columns:
                        st.write(
                            f"📄 **Reference:** {row['Official_Reference']}"
                        )

                    if "Data_Type" in df_context.columns:
                        st.caption(
                            f"📋 {row['Data_Type']}"
                        )

                # =========================
                # LOCATION MAP
                # =========================

                if (
                    "Latitude" in df.columns
                    and "Longitude" in df.columns
                ):

                    st.divider()
                    st.subheader(
                        "🗺️ Manganese Exploration Locations Map"
                    )

                    st.write(
                        "Geographical distribution of locations from "
                        "the uploaded dataset."
                    )

                    map_data = df[
                        ["Latitude", "Longitude"]
                    ].copy()

                    map_data.columns = ["lat", "lon"]

                    st.map(map_data)


# =========================
# COMPARE LOCATIONS
# =========================

if st.session_state.get("show_compare", False):

    st.divider()
    st.header("📊 Compare Locations")

    st.write(
        "Compare manganese exploration indicators between two locations "
        "from the uploaded geological dataset."
    )

    if "dataset" not in st.session_state:

        st.warning(
            "📊 Please upload geological data first using the Data Analysis section."
        )

    else:

        df = st.session_state["dataset"]

        if "Location" not in df.columns:

            st.error("❌ The dataset must contain a 'Location' column.")

        else:

            locations = df["Location"].dropna().unique()

            compare_col1, compare_col2 = st.columns(2)

            with compare_col1:
                location1 = st.selectbox(
                    "Select First Location",
                    locations,
                    key="location1"
                )

            with compare_col2:
                location2 = st.selectbox(
                    "Select Second Location",
                    locations,
                    key="location2"
                )

            if st.button("Compare Selected Locations"):

                if location1 == location2:

                    st.warning(
                        "⚠️ Please select two different locations."
                    )

                else:

                    row1 = df[
                        df["Location"] == location1
                    ].iloc[0]

                    row2 = df[
                        df["Location"] == location2
                    ].iloc[0]

                    st.success(
                        "📊 Location comparison generated successfully!"
                    )

                    st.subheader(
                        f"🔍 {location1} vs {location2}"
                    )

                    comparison_data = {
                        "Indicator": [
                            "Manganese %",
                            "Geological Score",
                            "Soil Anomaly Index",
                            "Exploration Potential"
                        ],
                        location1: [
                            row1.get("Mn_Percentage", "N/A"),
                            row1.get("Geological_Score", "N/A"),
                            row1.get("Soil_Anomaly_Index", "N/A"),
                            row1.get("Exploration_Potential", "N/A")
                        ],
                        location2: [
                            row2.get("Mn_Percentage", "N/A"),
                            row2.get("Geological_Score", "N/A"),
                            row2.get("Soil_Anomaly_Index", "N/A"),
                            row2.get("Exploration_Potential", "N/A")
                        ]
                    }

                    comparison_df = pd.DataFrame(comparison_data)

                    st.dataframe(
                        comparison_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Comparison insight
                    mn1 = float(row1.get("Mn_Percentage", 0))
                    mn2 = float(row2.get("Mn_Percentage", 0))

                    st.subheader("💡 Comparison Insight")

                    if mn1 > mn2:
                        better_location = location1
                    elif mn2 > mn1:
                        better_location = location2
                    else:
                        better_location = "Both locations"

                    if better_location == "Both locations":

                        st.write(
                            "Both locations show similar manganese concentration "
                            "based on the available dataset."
                        )

                    else:

                        st.write(
                            f"Based on manganese concentration, "
                            f"**{better_location}** shows a stronger preliminary "
                            "indicator for exploration."
                        )
# =========================
# EXPLORATION RANKING
# =========================

if st.session_state.get("show_ranking", False):

    st.divider()
    st.header("🏆 Exploration Ranking")

    st.write(
        "Locations are ranked using manganese concentration, geological "
        "score, and soil anomaly indicators."
    )

    if "dataset" not in st.session_state:

        st.warning(
            "📊 Please upload geological data first using the Data Analysis section."
        )

    else:

        ranking_df = st.session_state["dataset"].copy()

        required_columns = [
            "Location",
            "Mn_Percentage",
            "Geological_Score",
            "Soil_Anomaly_Index"
        ]

        if all(
            column in ranking_df.columns
            for column in required_columns
        ):

            # Calculate exploration score
            ranking_df["Exploration_Score"] = ranking_df.apply(
                lambda row: calculate_exploration_score(
                    row["Mn_Percentage"],
                    row["Geological_Score"],
                    row["Soil_Anomaly_Index"]
                ),
                axis=1
            )

            # Sort locations by score
            ranking_df = ranking_df.sort_values(
                by="Exploration_Score",
                ascending=False
            ).reset_index(drop=True)

            ranking_df["Rank"] = ranking_df.index + 1
            ranking_df["Priority"] = ranking_df["Rank"].apply(
                lambda x: f"Priority {x}"
            )

            st.success(
                "🏆 Exploration ranking generated successfully!"
            )

            st.subheader("🥇 Recommended Exploration Locations")

            display_columns = [
                "Rank",
                "Priority",
                "Location",
                "Mn_Percentage",
                "Geological_Score",
                "Soil_Anomaly_Index",
                "Exploration_Score"
            ]

            st.dataframe(
                ranking_df[display_columns],
                use_container_width=True,
                hide_index=True
            )

            # Top recommendation
            top_location = ranking_df.iloc[0]

            st.subheader("⭐ Top Recommendation")

            rank_col1, rank_col2, rank_col3 = st.columns(3)

            with rank_col1:
                st.metric(
                    "🏆 Top Location",
                    str(top_location["Location"])
                )

            with rank_col2:
                st.metric(
                    "Exploration Score",
                    f'{top_location["Exploration_Score"]}/100'
                )

            with rank_col3:
                st.metric(
                    "Priority",
                    "Priority 1"
                )

            st.info(
                f"💡 **{top_location['Location']}** is currently the "
                "highest-priority location based on the available exploration "
                "indicators."
            )

        else:

            st.error(
                "❌ Dataset is missing one or more required columns for ranking."
            )


# =========================
# EXPLORATION DASHBOARD
# =========================

if st.session_state.get("show_dashboard", False):

    st.divider()
    st.header("📊 Manganese Exploration Dashboard")

    st.write(
        "A consolidated overview of the uploaded geological data and "
        "exploration indicators."
    )

    if "dataset" not in st.session_state:

        st.warning(
            "📊 Please upload geological data first using the Data Analysis section."
        )

    else:

        dashboard_df = st.session_state["dataset"].copy()

        required_columns = [
            "Location",
            "Mn_Percentage",
            "Geological_Score",
            "Soil_Anomaly_Index"
        ]

        if all(
            column in dashboard_df.columns
            for column in required_columns
        ):

            # Calculate exploration score
            dashboard_df["Exploration_Score"] = dashboard_df.apply(
    lambda row: calculate_exploration_score(
        row["Mn_Percentage"],
        row["Geological_Score"],
        row["Soil_Anomaly_Index"]
    ),
    axis=1
)
            total_locations = len(dashboard_df)
            average_mn = dashboard_df["Mn_Percentage"].mean()

            high_potential = (
                dashboard_df["Exploration_Score"] >= 70
            ).sum()

            top_location = dashboard_df.loc[
                dashboard_df["Exploration_Score"].idxmax(),
                "Location"
            ]

            # Dashboard metrics
            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:
                st.metric(
                    "Locations Analyzed",
                    total_locations
                )

            with metric2:
                st.metric(
                    "Average Manganese %",
                    f"{average_mn:.2f}%"
                )

            with metric3:
                st.metric(
                    "High Potential Areas",
                    int(high_potential)
                )

            with metric4:
                st.metric(
                    "Top Location",
                    str(top_location)
                )

            st.divider()

            # Charts
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:

                st.subheader("📊 Manganese Distribution")

                mn_chart = dashboard_df.set_index(
                    "Location"
                )["Mn_Percentage"]

                st.bar_chart(mn_chart)

            with chart_col2:

                st.subheader("🏆 Exploration Scores")

                score_chart = dashboard_df.set_index(
                    "Location"
                )["Exploration_Score"]

                st.bar_chart(score_chart)

            st.divider()

            # Top 3 locations
            st.subheader("🏆 Top 3 Recommended Locations")

            top_three = dashboard_df.sort_values(
                by="Exploration_Score",
                ascending=False
            ).head(3).reset_index(drop=True)

            top1, top2, top3 = st.columns(3)

            for i, column in enumerate([top1, top2, top3]):

                if i < len(top_three):

                    location_data = top_three.iloc[i]

                    with column:

                        st.write(
                            f"**#{i + 1} {location_data['Location']}**"
                        )

                        st.metric(
                            "Exploration Score",
                            f"{location_data['Exploration_Score']}/100"
                        )

                        st.caption(
                            f"Mn: {location_data['Mn_Percentage']}% | "
                            f"Geological Score: "
                            f"{location_data['Geological_Score']}"
                        )

            st.success("📊 Dashboard generated successfully!")

            st.info(
                f"💡 **Key Recommendation:** {top_location} currently "
                "shows the strongest overall exploration indicators based "
                "on the available dataset."
            )

        else:

            st.error(
                "❌ Dataset is missing one or more required columns "
                "for the dashboard."
            )# ==============================
# LOCATION COMPARISON DASHBOARD
# ==============================

st.divider()
st.header("📊 Location Comparison Dashboard")

if "dataset" in st.session_state:

    comparison_df = st.session_state["dataset"]

    required_columns = [
        "Location",
        "Mn_Percentage",
        "Geological_Score",
        "Soil_Anomaly_Index"
    ]

    if all(column in comparison_df.columns for column in required_columns):

        selected_locations = st.multiselect(
            "Select locations to compare:",
            comparison_df["Location"].dropna().unique(),
            default=comparison_df["Location"].dropna().unique()[:3],
            key="comparison_locations"
        )

        if selected_locations:

            filtered_df = comparison_df[
                comparison_df["Location"].isin(selected_locations)
            ].copy()

            # Calculate exploration score for comparison
            filtered_df["Exploration_Score"] = filtered_df.apply(
                lambda row: calculate_exploration_score(
                    float(row.get("Mn_Percentage", 0)),
                    float(row.get("Geological_Score", 0)),
                    float(row.get("Soil_Anomaly_Index", 0))
                ),
                axis=1
            )

            st.subheader("📋 Location Comparison")

            display_columns = [
                "Location",
                "Mn_Percentage",
                "Geological_Score",
                "Soil_Anomaly_Index",
                "Exploration_Score"
            ]

            st.dataframe(
                filtered_df[display_columns],
                use_container_width=True
            )

            st.subheader("📈 Exploration Score Comparison")

            chart_data = filtered_df.set_index(
                "Location"
            )["Exploration_Score"]

            st.bar_chart(chart_data)

            # Identify strongest location
            top_row = filtered_df.loc[
                filtered_df["Exploration_Score"].idxmax()
            ]

            st.success(
                f"🏆 **Top Location:** {top_row['Location']} "
                f"with an Exploration Score of "
                f"{top_row['Exploration_Score']:.1f}/100"
            )

        else:
            st.info("Please select at least one location to compare.")

    else:
        st.warning(
            "⚠️ The dataset does not contain all required columns "
            "for location comparison."
        )

else:
    st.info("📁 Upload and analyze a dataset to use the comparison dashboard.")


# =========================
# FOOTER
# =========================

st.divider()
st.caption("SIH Prototype | Manganese Explorer AI")