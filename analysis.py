"""
analysis.py

This will:
- Load robot_data.csv
- Compute metrics
- Print summary insights
- Save fleet_summary.csv
"""

import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
EXPECTED_RUNTIME_MINUTES = 1440  # runtime of 1 day (1440 min)


# -----------------------------
# LOAD DATA
# -----------------------------
def load_data(filepath="robot_data.csv"):
    df = pd.read_csv(filepath)

    # Ensure datetime format
    df["date"] = pd.to_datetime(df["date"])

    return df


# -----------------------------
# METRIC CALCULATIONS
# -----------------------------
def compute_metrics(df):
    df = df.copy()

    # Uptime %
    df["uptime_pct"] = df["uptime_minutes"] / EXPECTED_RUNTIME_MINUTES

    # Avoid divide-by-zero issues
    df["completion_rate"] = df.apply( #run function
        lambda row: row["tasks_completed"] / row["tasks_assigned"]
        if row["tasks_assigned"] > 0 else 0,
        axis=1 #row by row
    )

    df["error_rate"] = df.apply(
        lambda row: row["error_count"] / row["tasks_assigned"]
        if row["tasks_assigned"] > 0 else 0,
        axis=1
    )

    return df


# -----------------------------
# FLEET-LEVEL SUMMARY (ALL ROBOTS)
# -----------------------------
def compute_fleet_summary(df):
    fleet_summary = df.groupby("date").agg({
        "uptime_minutes": "mean",
        "uptime_pct": "mean",
        "completion_rate": "mean",
        "error_count": "mean",
        "error_rate": "mean"
    }).reset_index()

    return fleet_summary


# -----------------------------
# INSIGHTS / ANALYSIS
# -----------------------------
def get_worst_robots(df, n=5): #top 5 worst performing robots by completion rate
    return (
        df.groupby("robot_id")["completion_rate"]
        .mean()
        .sort_values()
        .head(n)
    )


def error_completion_correlation(df):
    return df[["error_count", "completion_rate"]].corr()


def battery_error_analysis(df):
    return df.groupby("battery_level")["error_count"].mean()


def fleet_health_summary(df):
    summary = {
        "avg_completion_rate": df["completion_rate"].mean(),
        "avg_uptime_pct": df["uptime_pct"].mean(),
        "avg_error_rate": df["error_rate"].mean(),
    }
    return summary


# -----------------------------
# PRINT INSIGHTS (for CLI use)
# -----------------------------
def print_insights(df):
    print("\n=== FLEET HEALTH SUMMARY ===")
    summary = fleet_health_summary(df)

    print(f"Avg Completion Rate: {summary['avg_completion_rate']:.2f}") #limit to 2 digits after decimal 
    print(f"Avg Uptime %: {summary['avg_uptime_pct']:.2f}")
    print(f"Avg Error Rate: {summary['avg_error_rate']:.2f}")

    print("\n=== WORST PERFORMING ROBOTS ===")
    print(get_worst_robots(df))

    print("\n=== ERROR vs COMPLETION CORRELATION ===")
    print(error_completion_correlation(df))


# -----------------------------
# MAIN
# -----------------------------
def main():
    df = load_data()

    df = compute_metrics(df)

    fleet_summary = compute_fleet_summary(df)

    # Save for dashboard use
    fleet_summary.to_csv("fleet_summary.csv", index=False)

    # Print insights to console
    print_insights(df)


if __name__ == "__main__":
    main()