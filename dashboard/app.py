import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Construction Safety Command Center",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# FILE PATHS
# ============================================================

SITE_FILE = "data/processed/site_risk_results.csv"
SAFETY_FILE = "data/processed/worker_safety_results.csv"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_site_data():
    if not os.path.exists(SITE_FILE):
        return pd.DataFrame()

    try:
        df = pd.read_csv(SITE_FILE)

        if df.empty:
            return pd.DataFrame()

        if "risk_score" in df.columns:
            df["risk_score"] = pd.to_numeric(
                df["risk_score"],
                errors="coerce"
            ).fillna(0)

        if "hazard_count" in df.columns:
            df["hazard_count"] = pd.to_numeric(
                df["hazard_count"],
                errors="coerce"
            ).fillna(0)

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                errors="coerce"
            )

        return df

    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_safety_data():
    if not os.path.exists(SAFETY_FILE):
        return pd.DataFrame()

    try:
        df = pd.read_csv(SAFETY_FILE)

        if df.empty:
            return pd.DataFrame()

        if "safety_score" in df.columns:
            df["safety_score"] = pd.to_numeric(
                df["safety_score"],
                errors="coerce"
            ).fillna(0)

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                errors="coerce"
            )

        return df

    except Exception:
        return pd.DataFrame()


site_df = load_site_data()
safety_df = load_safety_data()


# ============================================================
# HEADER
# ============================================================

st.title("🏗️ Construction Safety Command Center")

st.caption(
    "AI-powered site risk monitoring, PPE compliance, "
    "worker safety analysis, and safety alerts"
)

st.divider()


# ============================================================
# CHECK DATA
# ============================================================

if site_df.empty and safety_df.empty:

    st.error(
        "No processed data found. Please run the Site Risk Agent "
        "and Safety Agent first."
    )

    st.stop()


# ============================================================
# TOP KPI SECTION
# ============================================================

if not safety_df.empty:

    total_workers = len(safety_df)

    workers_at_risk = len(
        safety_df[
            safety_df["violations"].fillna("").astype(str).str.strip() != ""
        ]
    )

    critical_alerts = len(
        safety_df[
            safety_df["alert"].astype(str).str.contains(
                "Critical",
                case=False,
                na=False
            )
        ]
    )

    ppe_compliant_workers = len(
        safety_df[
            safety_df["ppe_compliance"].astype(str).str.lower()
            == "compliant"
        ]
    )

    ppe_compliance = (
        (ppe_compliant_workers / total_workers) * 100
        if total_workers > 0
        else 0
    )

else:

    total_workers = 0
    workers_at_risk = 0
    critical_alerts = 0
    ppe_compliance = 0


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "👷 Workers Monitored",
        total_workers,
        "Workers analyzed by Safety Agent"
    )


with col2:
    st.metric(
        "⚠️ Workers At Risk",
        workers_at_risk,
        "Workers requiring attention"
    )


with col3:
    st.metric(
        "🚨 Critical Alerts",
        critical_alerts,
        "Immediate safety attention"
    )


with col4:
    st.metric(
        "🦺 PPE Compliance",
        f"{ppe_compliance:.0f}%",
        "Overall PPE compliance"
    )


st.divider()


# ============================================================
# TABS
# ============================================================

site_tab, safety_tab = st.tabs(
    [
        "🏗️ Site Risk Monitoring",
        "👷 Worker Safety Analytics"
    ]
)


# ============================================================
# SITE RISK MONITORING
# ============================================================

with site_tab:

    st.header("🏗️ Site Risk Monitoring")

    if site_df.empty:

        st.warning(
            "Site risk data is not available."
        )

    else:

        # ----------------------------------------------------
        # SORT DATA BY TIMESTAMP
        # ----------------------------------------------------

        if "timestamp" in site_df.columns:

            site_df = site_df.sort_values(
                "timestamp"
            ).reset_index(drop=True)


        # ----------------------------------------------------
        # SIDEBAR FILTER
        # ----------------------------------------------------

        st.sidebar.header("🔍 Site Filters")

        available_levels = sorted(
            site_df["risk_level"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_level = st.sidebar.selectbox(
            "Risk Level",
            ["All"] + available_levels
        )

        filtered_site_df = site_df.copy()

        if selected_level != "All":

            filtered_site_df = filtered_site_df[
                filtered_site_df["risk_level"]
                == selected_level
            ]


        # ----------------------------------------------------
        # CURRENT SITE CONDITION
        # ----------------------------------------------------

        st.subheader("🚦 Current Site Condition")

        if not filtered_site_df.empty:

            latest_site = filtered_site_df.iloc[-1]

            latest_score = int(
                latest_site["risk_score"]
            )

            latest_level = str(
                latest_site["risk_level"]
            )

            latest_hazards = int(
                latest_site["hazard_count"]
            )


            condition_col1, condition_col2, condition_col3 = st.columns(3)


            with condition_col1:

                st.metric(
                    "Current Risk Score",
                    f"{latest_score}/100",
                    latest_level
                )


            with condition_col2:

                st.metric(
                    "Current Hazards",
                    latest_hazards
                )


            with condition_col3:

                if pd.notna(latest_site["timestamp"]):

                    latest_time = latest_site["timestamp"].strftime(
                        "%d %b %Y, %I:%M %p"
                    )

                else:

                    latest_time = "Unknown"

                st.metric(
                    "Last Assessment",
                    latest_time
                )


            # ------------------------------------------------
            # CURRENT STATUS MESSAGE
            # ------------------------------------------------

            if latest_level.lower() == "critical":

                st.error(
                    "🚨 CRITICAL: Immediate action is required "
                    "at the construction site."
                )

            elif latest_level.lower() == "high":

                st.error(
                    "⚠️ HIGH RISK: Site conditions require "
                    "urgent attention."
                )

            elif latest_level.lower() == "medium":

                st.warning(
                    "🟠 MEDIUM RISK: Review the detected hazards "
                    "and recommended actions."
                )

            elif latest_level.lower() == "low":

                st.info(
                    "🟡 LOW RISK: Minor risks detected. "
                    "Continue monitoring."
                )

            else:

                st.success(
                    "✅ SAFE: No significant hazards detected "
                    "in the latest assessment."
                )


        st.divider()


        # ----------------------------------------------------
        # RISK OVERVIEW
        # ----------------------------------------------------

        st.subheader("📊 Risk Overview")

        risk_counts = (
            filtered_site_df["risk_level"]
            .value_counts()
        )


        risk_col1, risk_col2, risk_col3, risk_col4, risk_col5 = st.columns(5)


        with risk_col1:

            st.metric(
                "🟢 Safe",
                int(risk_counts.get("Safe", 0))
            )


        with risk_col2:

            st.metric(
                "🟡 Low",
                int(risk_counts.get("Low", 0))
            )


        with risk_col3:

            st.metric(
                "🟠 Medium",
                int(risk_counts.get("Medium", 0))
            )


        with risk_col4:

            st.metric(
                "🔴 High",
                int(risk_counts.get("High", 0))
            )


        with risk_col5:

            st.metric(
                "🚨 Critical",
                int(risk_counts.get("Critical", 0))
            )


        st.divider()


        # ----------------------------------------------------
        # WHAT NEEDS ATTENTION
        # ----------------------------------------------------

        st.subheader("⚠️ What Needs Attention")

        attention_df = filtered_site_df[
            filtered_site_df["risk_level"].isin(
                ["Medium", "High", "Critical"]
            )
        ].copy()


        if not attention_df.empty:

            attention_df = attention_df.sort_values(
                "risk_score",
                ascending=False
            )


            display_columns = [
                "timestamp",
                "risk_score",
                "risk_level",
                "hazard_count",
                "hazards"
            ]

            display_columns = [
                column
                for column in display_columns
                if column in attention_df.columns
            ]


            st.dataframe(
                attention_df[display_columns],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No medium, high, or critical site risks "
                "were found."
            )


        st.divider()


        # ----------------------------------------------------
        # RECOMMENDED ACTIONS
        # ----------------------------------------------------

        st.subheader("🛠️ Recommended Actions")

        recommendations = []


        for _, row in filtered_site_df.iterrows():

            if (
                "recommendations" in row
                and pd.notna(row["recommendations"])
            ):

                text = str(
                    row["recommendations"]
                ).strip()

                if text:

                    for recommendation in text.split(";"):

                        recommendation = recommendation.strip()

                        if (
                            recommendation
                            and recommendation not in recommendations
                        ):

                            recommendations.append(
                                recommendation
                            )


        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                st.write(
                    f"**{index}.** {recommendation}"
                )

        else:

            st.success(
                "✅ No immediate corrective actions required."
            )


        st.divider()


        # ----------------------------------------------------
        # DETAILED SITE MONITORING
        # ----------------------------------------------------

        st.subheader("📋 Detailed Site Monitoring")

        detailed_site_df = filtered_site_df.copy()

        if "timestamp" in detailed_site_df.columns:

            detailed_site_df["timestamp"] = (
                detailed_site_df["timestamp"]
                .dt.strftime("%Y-%m-%d %H:%M")
            )


        st.dataframe(
            detailed_site_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# WORKER SAFETY ANALYTICS
# ============================================================

with safety_tab:

    st.header("👷 Worker Safety Analytics")

    if safety_df.empty:

        st.warning(
            "Worker safety data is not available."
        )

    else:

        # ----------------------------------------------------
        # SORT DATA
        # ----------------------------------------------------

        if "timestamp" in safety_df.columns:

            safety_df = safety_df.sort_values(
                "timestamp"
            ).reset_index(drop=True)


        # ----------------------------------------------------
        # SIDEBAR WORKER FILTER
        # ----------------------------------------------------

        st.sidebar.header("👷 Worker Filters")

        available_zones = sorted(
            safety_df["zone"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        selected_zone = st.sidebar.selectbox(
            "Construction Zone",
            ["All"] + available_zones
        )


        filtered_safety_df = safety_df.copy()


        if selected_zone != "All":

            filtered_safety_df = filtered_safety_df[
                filtered_safety_df["zone"]
                == selected_zone
            ]


        # ----------------------------------------------------
        # SAFETY KPI
        # ----------------------------------------------------

        total_filtered_workers = len(
            filtered_safety_df
        )


        average_safety_score = (
            filtered_safety_df["safety_score"].mean()
            if total_filtered_workers > 0
            else 0
        )


        safe_workers = len(
            filtered_safety_df[
                filtered_safety_df["safety_level"]
                == "Safe"
            ]
        )


        critical_workers = len(
            filtered_safety_df[
                filtered_safety_df["safety_level"]
                == "Critical"
            ]
        )


        safety_col1, safety_col2, safety_col3, safety_col4 = st.columns(4)


        with safety_col1:

            st.metric(
                "👷 Workers",
                total_filtered_workers
            )


        with safety_col2:

            st.metric(
                "🛡️ Average Safety Score",
                f"{average_safety_score:.0f}/100"
            )


        with safety_col3:

            st.metric(
                "✅ Safe Workers",
                safe_workers
            )


        with safety_col4:

            st.metric(
                "🚨 Critical Workers",
                critical_workers
            )


        st.divider()


        # ----------------------------------------------------
        # PPE COMPLIANCE
        # ----------------------------------------------------

        st.subheader("🦺 PPE Compliance")


        ppe_compliant = len(
            filtered_safety_df[
                filtered_safety_df["ppe_compliance"]
                .astype(str)
                .str.lower()
                == "compliant"
            ]
        )


        ppe_violation = (
            total_filtered_workers - ppe_compliant
        )


        ppe_col1, ppe_col2, ppe_col3 = st.columns(3)


        with ppe_col1:

            st.metric(
                "✅ PPE Compliant",
                ppe_compliant
            )


        with ppe_col2:

            st.metric(
                "⚠️ PPE Violations",
                ppe_violation
            )


        with ppe_col3:

            compliance_percentage = (
                (ppe_compliant / total_filtered_workers) * 100
                if total_filtered_workers > 0
                else 0
            )

            st.metric(
                "📈 Compliance Rate",
                f"{compliance_percentage:.0f}%"
            )


        st.divider()


        # ----------------------------------------------------
        # ACTIVE SAFETY ALERTS
        # ----------------------------------------------------

        st.subheader("🚨 Active Safety Alerts")


        alert_df = filtered_safety_df[
            filtered_safety_df["alert"]
            .astype(str)
            .str.lower()
            != "no alert"
        ].copy()


        if not alert_df.empty:

            alert_columns = [
                "timestamp",
                "worker_id",
                "zone",
                "safety_score",
                "safety_level",
                "alert",
                "violations"
            ]


            alert_columns = [
                column
                for column in alert_columns
                if column in alert_df.columns
            ]


            alert_df = alert_df.sort_values(
                "safety_score"
            )


            st.dataframe(
                alert_df[alert_columns],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No active worker safety alerts."
            )


        st.divider()


        # ----------------------------------------------------
        # ZONE-WISE SAFETY
        # ----------------------------------------------------

        st.subheader("📍 Zone-wise Safety Status")


        zone_summary = (
            filtered_safety_df
            .groupby("zone")
            .agg(
                Workers=("worker_id", "count"),
                Average_Safety_Score=("safety_score", "mean")
            )
            .reset_index()
        )


        zone_summary["Average_Safety_Score"] = (
            zone_summary["Average_Safety_Score"]
            .round(0)
            .astype(int)
        )


        def zone_status(score):

            if score >= 90:
                return "Safe"

            elif score >= 70:
                return "Low"

            elif score >= 50:
                return "Medium"

            elif score >= 25:
                return "High"

            else:
                return "Critical"


        zone_summary["Status"] = (
            zone_summary["Average_Safety_Score"]
            .apply(zone_status)
        )


        st.dataframe(
            zone_summary,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # ----------------------------------------------------
        # WORKERS REQUIRING ATTENTION
        # ----------------------------------------------------

        st.subheader("⚠️ Workers Requiring Attention")


        worker_attention_df = filtered_safety_df[
            filtered_safety_df["safety_level"].isin(
                ["Medium", "High", "Critical"]
            )
        ].copy()


        if not worker_attention_df.empty:

            attention_columns = [
                "worker_id",
                "zone",
                "safety_score",
                "safety_level",
                "ppe_compliance",
                "violations",
                "alert"
            ]


            attention_columns = [
                column
                for column in attention_columns
                if column in worker_attention_df.columns
            ]


            worker_attention_df = (
                worker_attention_df
                .sort_values(
                    "safety_score"
                )
            )


            st.dataframe(
                worker_attention_df[
                    attention_columns
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No workers currently require additional attention."
            )


        st.divider()


        # ----------------------------------------------------
        # SAFETY RECOMMENDATIONS
        # ----------------------------------------------------

        st.subheader("🛠️ Safety Recommendations")


        safety_recommendations = []


        for _, row in filtered_safety_df.iterrows():

            if (
                "recommendations" in row
                and pd.notna(row["recommendations"])
            ):

                text = str(
                    row["recommendations"]
                ).strip()


                if text:

                    for recommendation in text.split(";"):

                        recommendation = recommendation.strip()


                        if (
                            recommendation
                            and recommendation
                            not in safety_recommendations
                        ):

                            safety_recommendations.append(
                                recommendation
                            )


        if safety_recommendations:

            for index, recommendation in enumerate(
                safety_recommendations,
                start=1
            ):

                st.write(
                    f"**{index}.** {recommendation}"
                )

        else:

            st.success(
                "✅ No additional safety recommendations."
            )


        st.divider()


        # ----------------------------------------------------
        # DETAILED WORKER SAFETY DATA
        # ----------------------------------------------------

        st.subheader("📋 Detailed Worker Safety Analysis")


        detailed_safety_df = filtered_safety_df.copy()


        if "timestamp" in detailed_safety_df.columns:

            detailed_safety_df["timestamp"] = (
                detailed_safety_df["timestamp"]
                .dt.strftime("%Y-%m-%d %H:%M")
            )


        st.dataframe(
            detailed_safety_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏗️ Construction Risk Intelligence Platform | "
    "Site Risk Agent + Safety Agent"
)