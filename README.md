# Robot Fleet Performance Analysis

## Project Overview

This project analyzes the operational performance of a fleet of 50 robots over a 30-day period. The goal was to identify patterns and correlations between key metrics including uptime, battery level, error count, and task completion rate to better understand what factors drive robot performance and reliability.

The dataset was simulated to reflect real-world conditions, where factors such as prolonged uptime and low battery levels are expected to increase error rates and reduce task completion. Each robot was assigned a unique reliability profile to introduce realistic variance across the fleet.

### Tools & Technologies

- **Python** — data generation and preprocessing
- **Pandas** — data manipulation and analysis
- **Plotly Express** — interactive charting and visualization
- **Streamlit** — dashboard interface for exploring the data
- **Jupyter Notebook** — exploratory data analysis

---

## Analysis & Findings

### Fleet Performance Over Time

> _Describe what trends you observed across the fleet over the 30-day period. Did errors increase over time? Did battery levels decline? Were there any noticeable dips or spikes in task completion on certain days?_

**Findings:**
Within my "Completion Rate Over Time" line graph, I found that overall complation rate declined overtime. My next objective was to find out what factors played a role in the decline of performance. My initial thoughts were that the decline in performance could be from any of the following reasons: battery percentage, total uptime, system errors, hardware complications, process complications

---

### Error Count vs Completion Rate

> _Describe the relationship between error count and task completion rate. Was there a clear negative correlation? Did robots with higher error counts consistently complete fewer tasks? Were there any outliers?_

**Findings:**
I used a scatter plot graph to visualize the correlation between the average error count per unique robot and their average completion rate. With the dataset I analyzed, I found that as the error counts increased, the completion rate decreased. This means that the errors were causing problems such as downtime and failed processes. This shows to be one of the reasons complaetion rates were declining. My next thought was to find out what the root cause of these errors could have possibly been, could it be avoidable or were these errors strictly unpredictable?

---

### Uptime vs Error Count

> _Describe what the scatter plot revealed about the relationship between uptime and errors. Did robots with longer runtimes tend to produce more errors? Was the correlation strong or weak? Did certain robots cluster differently?_

**Findings:**
In my "Uptime vs Error Count" graph, I plotted every error and where it was in terms of uptime in respect to each robot. From this graph I was able to see a slight increase in errors towards the higher uptime values. This is consistent with my fidings on how when uptime increases, error counts increase. One thing that this could indicate is that as uptime increases, battery life decreases and posssible leads to higher error counts. 
---

### Average Uptime vs Average Errors

> _Describe what this chart showed when looking at per-robot averages. Did robots with consistently high average uptime also have the highest average error counts? Were any robots high uptime but low error — and what might explain that?_

**Findings:**
This graph was interesting. As I looked it over, I found that as uptime increased, the error counts seems to stay consitent throughout. Within the graph I was able to see that towards the mid ranges of uptime, there seems to be more total errors logged which could indicate failures in battery life or uptime complications. 
---

### Average Uptime vs Completion Rate

> _Describe the relationship between average uptime and how much work robots actually finished. Did more uptime translate to better completion, or did fatigue/errors erode that advantage? What does this suggest about optimal operating hours?_

**Findings:**
Within my "Avg Uptime vs Completion Rate" graph I was able to identify a slight "V" shaped trend line. This could be due to the fact that as the robots batterys depleated, they were recharged and took a break, which inturn could have increased their completion rate after the fact. 
---

### Average Battery Level vs Error Count

> _Describe the relationship between average battery level and how many errors were logged._

**Findings:**
In the Bettery Level vs Error Count graph I was able to find a clear correlation to decreasing battery life and increasing error counts. This finding is consistent with my other findings from the previous graphs and leads me to believe that the battery life has plays a vital role to overall fleet performance.  
---

## Robot Performance Breakdown

### Worst 5 Robots

> _Identify the 5 worst-performing robots based on your chosen criteria (e.g. highest error count, lowest completion rate, or a combination). For each robot, describe what stood out in the data and what might explain their poor performance._

| Robot ID | Avg Uptime (min) | Avg Error Count | Avg Completion Rate | Notes |
|----------|-----------------|-----------------|---------------------|-------|
|    10    |                 |                 |                     |       |
|    4     |                 |                 |                     |       |
|    37    |                 |                 |                     |       |
|    6     |                 |                 |                     |       |
|    29    |                 |                 |                     |       |

**Findings:**
I identified the top 5 worst robots in the fleet and analyzed them individually to see how their individual stats align with my findings from above. 
robot_id: 10 -> 
robot_id: 4  -> 
robot_id: 37 -> 
robot_id: 29 -> 
---

### Best 5 Robots

> _Identify the 5 best-performing robots. What made them stand out? Were they consistently low on errors, high on completions, or both? Did their uptime or battery patterns differ from the worst performers?_

| Robot ID | Avg Uptime (min) | Avg Error Count | Avg Completion Rate | Notes |
|----------|-----------------|-----------------|---------------------|-------|
|    34    |                 |                 |                     |       |
|    42    |                 |                 |                     |       |
|    37    |                 |                 |                     |       |
|    6     |                 |                 |                     |       |
|    29    |                 |                 |                     |       |

**Findings:**

---

## Summary & Conclusions

> _Wrap up your overall takeaways from the analysis. What were the most significant correlations you found? What would you recommend based on the data — for example, should robots be taken offline after a certain uptime threshold, or flagged for maintenance when battery drops below a certain level?_

**Conclusions:**
