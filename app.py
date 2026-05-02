# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Import your analysis layer
from analysis import load_data, compute_metrics, compute_fleet_summary

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Robot Fleet Dashboard",
    layout="wide"
)

st.title("Robot Fleet Performance Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def get_data():
    df = load_data("robot_data.csv")
    df = compute_metrics(df)
    return df

df = get_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

robot_ids = df["robot_id"].unique()
selected_robot = st.sidebar.selectbox("Select Robot", ["All"] + list(robot_ids))

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

# Apply filters
filtered_df = df.copy()

if selected_robot != "All":
    filtered_df = filtered_df[filtered_df["robot_id"] == selected_robot]

filtered_df = filtered_df[
    (filtered_df["date"] >= pd.to_datetime(date_range[0])) &
    (filtered_df["date"] <= pd.to_datetime(date_range[1]))
]

# -----------------------------
# KPI METRICS
# -----------------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    avg_completion = filtered_df["completion_rate"].mean() #avg competion rate
    st.metric("Avg Completion Rate", f"{avg_completion:.2%}")

with col2:
    avg_uptime = filtered_df["uptime_pct"].mean()
    st.metric("Avg Uptime", f"{avg_uptime:.2%}")

with col3:
    avg_errors = filtered_df["error_count"].mean()
    st.metric("Avg Errors per Run", f"{avg_errors:.2f}")

# -----------------------------
# TIME SERIES (FLEET PERFORMANCE)
# -----------------------------
st.subheader("Fleet Performance Over Time")

fleet_summary = compute_fleet_summary(filtered_df)

fig1 = px.line(
    fleet_summary,
    x="date",
    y="completion_rate",
    title="Completion Rate Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# ERROR VS PERFORMANCE
# -----------------------------
st.subheader("Error Rate vs Completion Rate")

robot_avg = (
    filtered_df.groupby("robot_id")
    .mean(numeric_only=True)
    .reset_index()
)

fig2 = px.scatter(
    robot_avg,
    x="error_count",
    y="completion_rate",
    hover_data=["robot_id"],
    title="Errors vs Completion Rate"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# ROBOT TABLE
# -----------------------------
st.subheader("Robot Data")

st.dataframe(filtered_df.sort_values("date", ascending=False), use_container_width=True)

# -----------------------------
# INSIGHTS PANEL
# -----------------------------
st.subheader("Insights")

if avg_completion < 0.85: #optimal completion rate set to 85%
    st.error("Fleet completion rate is below optimal threshold (85%)")

if avg_errors > 1.5:
    st.warning("Elevated error rates detected across fleet")

if avg_uptime < 0.75:
    st.warning("Low uptime detected, possible reliability issues")

# Top 5 worst robots
st.subheader("Worst Performing Robots")

worst = (
    filtered_df.groupby("robot_id")["completion_rate"]
    .mean()
    .sort_values()
    .head(5)
)

st.write(worst)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with Python, Pandas, and Streamlit")