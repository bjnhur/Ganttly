import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.colors as mcolors
import numpy as np

# Data for Gantt chart
# Adding a "Description" field for each task
data = [
    {"Category": "Planning", "Task": "Project Kickoff", "Description": "Initial planning and stakeholder alignment", "Start": "2024-01", "End": "2024-03"},
    {"Category": "Planning", "Task": "Requirement Gathering", "Description": "Identifying key features and specifications", "Start": "2024-02", "End": "2024-06"},
    {"Category": "Implementation", "Task": "Core Module Development", "Description": "Building the primary functionalities", "Start": "2024-06", "End": "2024-20"},
    {"Category": "Implementation", "Task": "UI/UX Design", "Description": "Creating user-friendly interfaces", "Start": "2024-07", "End": "2024-15"},
    {"Category": "Implementation", "Task": "Integration Testing", "Description": "Testing system-level interactions", "Start": "2024-16", "End": "2024-25"},
    {"Category": "Documentation", "Task": "User Manual Draft", "Description": "Creating user documentation for open-source use", "Start": "2024-18", "End": "2024-22"},
    {"Category": "Closure", "Task": "Final Review", "Description": "Peer review and quality assurance", "Start": "2024-23", "End": "2024-26"},
    {"Category": "Release", "Task": "Public Release", "Description": "Publishing the project on GitHub", "Start": "2024-27", "End": "2024-30"},
]


# Convert data to DataFrame
def week_to_date(year_week):
    year, week = map(int, year_week.split("-"))
    return datetime.strptime(f"{year} {week} 1", "%Y %W %w")


df = pd.DataFrame(data)
df["Start"] = df["Start"].apply(week_to_date)
df["End"] = df["End"].apply(week_to_date)

# Assign unique positions for tasks
unique_tasks = list(df["Task"])
y_mapping = {task: i for i, task in enumerate(unique_tasks)}

# Define color for categories
category_colors = {"Planning": "#a8d5e2", "Implementation": "#f9d776", "Closure": "#c3e88d", "Review": "#f4a7b9"}  # Added a new category color


# Fallback color for additional categories
def get_category_color(category):
    return category_colors.get(category, "#cccccc")  # Default gray color for unspecified categories


# Define a two-tone color function for mid-progress highlight
def get_two_tone_colors(base_color, duration_weeks):
    start_rgba = np.array(mcolors.to_rgba(base_color))
    mid_rgba = start_rgba * 0.9  # Slightly darker shade for mid-progress
    end_rgba = start_rgba * 0.8  # Darkest shade for the end
    color_list = []
    for week in range(duration_weeks):
        if duration_weeks == 1:
            color_list.append(mcolors.to_hex(start_rgba))
        elif duration_weeks == 2:
            color_list.append(mcolors.to_hex(start_rgba if week == 0 else end_rgba))
        else:
            if week < duration_weeks // 3:
                color_list.append(mcolors.to_hex(start_rgba))
            elif week < 2 * (duration_weeks // 3):
                color_list.append(mcolors.to_hex(mid_rgba))
            else:
                color_list.append(mcolors.to_hex(end_rgba))
    return color_list


# Plotting the Gantt chart
fig, ax = plt.subplots(figsize=(14, 8))

for i, row in df.iterrows():
    if i == 0 or df.iloc[i]["Category"] != df.iloc[i - 1]["Category"]:
        ax.axhline(y=y_mapping[row["Task"]] - 0.5, color="gray", linestyle="--", linewidth=1.5)
    y_pos = y_mapping[row["Task"]]
    duration_weeks = (row["End"] - row["Start"]).days // 7
    base_color = get_category_color(row["Category"])
    two_tone_colors = get_two_tone_colors(base_color, duration_weeks)
    for week in range(duration_weeks):
        ax.barh(y_pos, 7, left=row["Start"] + timedelta(weeks=week), color=two_tone_colors[week], edgecolor="none", height=0.5, linewidth=0, align="center")
    ax.text(row["Start"] + timedelta(days=1), y_pos, row["Description"], va="center", ha="left", fontsize=8, color="black")

# Customizing Y-axis
y_ticks = [y_mapping[task] for task in unique_tasks]
ax.set_yticks(y_ticks)
ax.set_yticklabels(unique_tasks, fontsize=10)

# Customizing X-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_xlim(df["Start"].min() - timedelta(days=7), df["End"].max() + timedelta(days=7))

# Adding gridlines
ax.grid(axis="x", linestyle="--", color="gray", alpha=0.7)

# Adding title and labels
plt.title("Full-Width Yearly Gantt Chart", fontsize=14)
plt.xlabel("Timeline", fontsize=12)
plt.ylabel("Tasks", fontsize=12)
plt.tight_layout()

# Legend
legend_patches = [plt.Rectangle((0, 0), 1, 1, color=color, label=category) for category, color in category_colors.items()]
ax.legend(handles=legend_patches, title="Categories", loc="upper right", fontsize=10, title_fontsize=12)

# Display the chart
plt.show()
