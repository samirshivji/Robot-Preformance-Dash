import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

#generate synthetic data for 50 robots over 30 days, save into csv file
def generate_data(num_robots=50, days=30):
    data = []

    start_date = datetime.now() - timedelta(days=days)

    for robot_id in range(num_robots):
        for day in range(days):
            date = start_date + timedelta(days=day)

            tasks_assigned = random.randint(5, 20)
            tasks_completed = max(0, tasks_assigned - random.randint(0, 5))
            error_count = random.randint(0, 3)

            data.append({
                "robot_id": robot_id,
                "date": date,
                "uptime_minutes": random.randint(600, 1440),
                "tasks_assigned": tasks_assigned,
                "tasks_completed": tasks_completed,
                "error_count": error_count,
                "battery_level": random.randint(20, 100)
            })

    return pd.DataFrame(data)

df = generate_data()
df.to_csv("robot_data.csv", index=False)