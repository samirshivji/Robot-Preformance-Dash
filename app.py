# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Import your analysis layer
from analysis import load_data, compute_metrics, compute_fleet_summary

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(                                                                 #set page (tab) title and layout
    page_title="Robot Fleet Dashboard",
    layout="wide"
)

st.title("Robot Fleet Performance Dashboard") #set page title

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data                                                                      #cache data loading for performance
def get_data():
    df = load_data("robot_data_realistic.csv")
    df = compute_metrics(df)
    return df

df = get_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

robot_ids = df["robot_id"].unique()                                                 #get unique robot IDs for filter options
selected_robot = st.sidebar.selectbox("Select Robot", ["All"] + list(robot_ids))    #add options for "All" and individual robots into sidebar selectbox 

date_range = st.sidebar.date_input(                                                 #add date range filter to sidebar, with min and max dates from the data as defaults
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
    avg_completion = filtered_df["completion_rate"].mean() 
    st.metric("Avg Completion Rate", f"{avg_completion:.2%}")                       #display avg completion rate as percentage with 2 decimal places

with col2:
    avg_uptime = filtered_df["uptime_pct"].mean()
    st.metric("Avg Uptime", f"{avg_uptime:.2%}")                                    #display avg uptime as percentage with 2 decimal places

with col3:
    avg_errors = filtered_df["error_count"].mean()
    st.metric("Avg Errors per Run", f"{avg_errors:.2f}")                            #display avg errors per run with 2 decimal places

# -----------------------------
# TIME SERIES (FLEET PERFORMANCE)
# -----------------------------
#Fig 1: Line chart of completion rate over time
st.subheader("Fleet Performance Over Time")

fleet_summary = compute_fleet_summary(filtered_df)

fig1 = px.line(                                                                     #create line chart of completion rate over time using plotly express, with date on x-axis and completion_rate on y-axis
    fleet_summary,
    x="date",
    y="completion_rate",
    title="Completion Rate Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# ERROR VS PERFORMANCE
# -----------------------------
#Fig 2: Scatter plot of error count vs completion rate
st.subheader("Error Count vs Completion Rate")

robot_avg = (                                                                      #calculate average error count and completion rate for each robot
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
# UPTIME VS ERROR COUNT
# -----------------------------
#Fig 3: Scatter plot of uptime vs error count
st.subheader("Uptime vs Error Count")

robot_uptime_error_data = filtered_df[["robot_id", "uptime_minutes", "error_count"]]      

fig3 = px.scatter(
    robot_uptime_error_data,
    x="uptime_minutes",
    y="error_count",
    hover_data=["robot_id"],
    title="Uptime vs Error Count"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# AVG UPTIME VS AVG ERROR COUNT
# -----------------------------
#Fig 4: Scatter plot of avg uptime vs avg error count
st.subheader("Avg Uptime vs Avg Errors")

robot_uptime_error_data = (
    filtered_df.groupby("robot_id")[["uptime_minutes", "error_count"]]
    .mean()
    .reset_index()             
)

fig4 = px.scatter(
    robot_uptime_error_data,
    x="uptime_minutes",
    y="error_count",
    hover_data=["robot_id"],
    title="Avg Uptime vs Avg Errors"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# AVG UPTIME VS COMPLETION RATE
# -----------------------------
#Fig 4: Scatter plot of avg uptime vs avg completion rate

st.subheader("Avg Uptime vs Completion Rate")

robot_uptime_completion_data = (
    filtered_df.groupby("robot_id")[["uptime_minutes", "completion_rate"]]
    .mean()
    .reset_index()             
)

fig5 = px.scatter(
    robot_uptime_completion_data,
    x="uptime_minutes",
    y="completion_rate",
    hover_data=["robot_id"],
    title="Avg Uptime vs Completion Rate"
)

st.plotly_chart(fig5, use_container_width=True)


# -----------------------------
# Battery Percentage VS ERROR COUNT
# -----------------------------
#Fig 6: Scatter plot of battery percentage vs error count

st.subheader("Battery Level vs Error Count")

battery_error_data = (
    filtered_df.groupby("battery_level")["error_count"]
    .mean()
    .reset_index()
)

fig6 = px.scatter(
    battery_error_data,
    x="battery_level",
    y="error_count",
    title="Battery Level vs Error Count"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# ROBOT TABLE
# -----------------------------
st.subheader("Robot Data")

st.dataframe(filtered_df.sort_values("date", ascending=False), use_container_width=True)        #Display filtered robot data in a table, sorted by date in descending order

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

worst = (                                                                                       #calculate top 5 worst performing robots by completion rate                                      
    filtered_df.groupby("robot_id")["completion_rate"]
    .mean()
    .sort_values()
    .head(5)
)

st.write(worst)

#Top 5 best robots

st.subheader("Best Performing Robots")

best = (                                                                                        #calculate top 5 best performing robots by completion rate
    filtered_df.groupby("robot_id")["completion_rate"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

st.write(best)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with Python, Pandas, and Streamlit")