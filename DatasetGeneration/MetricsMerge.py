# %% Libraries
import os
import pandas as pd
from enum import Enum, auto


# %% Shot-shape functions


def shot_direction(
    launchDirection: float, pull_border: float = -5, push_border: float = 5
):
    if launchDirection < pull_border:
        return "PULL"
    elif launchDirection > push_border:
        return "PUSH"
    else:
        return "STRAIGHT"


def shot_curvature(
    sidespin: float,
    slice_border: float = -800,
    fade_border: float = -300,
    draw_border: float = 300,
    hook_border: float = 800,
):
    if sidespin < slice_border:
        return "SLICE"
    elif sidespin < fade_border:
        return "FADE"
    elif sidespin < draw_border:
        return "NEUTRAL"
    elif sidespin < hook_border:
        return "DRAW"
    else:
        return "HOOK"


def shotType(shot_direction, shot_curvature):
    if shot_direction == "PULL" and shot_curvature == "HOOK":
        return "PULL_HOOK"
    elif shot_direction == "PULL" and shot_curvature == "DRAW":
        return "PULL_DRAW"
    elif shot_direction == "PULL" and shot_curvature == "NEUTRAL":
        return "PULL"
    elif shot_direction == "PULL" and shot_curvature == "FADE":
        return "PULL_FADE"
    elif shot_direction == "PULL" and shot_curvature == "SLICE":
        return "PULL_SLICE"
    elif shot_direction == "STRAIGHT" and shot_curvature == "HOOK":
        return "STRAIGHT_HOOK"
    elif shot_direction == "STRAIGHT" and shot_curvature == "DRAW":
        return "STRAIGHT_DRAW"
    elif shot_direction == "STRAIGHT" and shot_curvature == "NEUTRAL":
        return "STRAIGHT"
    elif shot_direction == "STRAIGHT" and shot_curvature == "FADE":
        return "STRAIGHT_FADE"
    elif shot_direction == "STRAIGHT" and shot_curvature == "SLICE":
        return "STRAIGHT_SLICE"
    elif shot_direction == "PUSH" and shot_curvature == "HOOK":
        return "PUSH_HOOK"
    elif shot_direction == "PUSH" and shot_curvature == "DRAW":
        return "PUSH_DRAW"
    elif shot_direction == "PUSH" and shot_curvature == "NEUTRAL":
        return "PUSH"
    elif shot_direction == "PUSH" and shot_curvature == "FADE":
        return "PUSH_FADE"
    elif shot_direction == "PUSH" and shot_curvature == "SLICE":
        return "PUSH_SLICE"
    else:
        return "NO_CATEGORY"


# %% File paths
rawMetrics = (
    "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Metrics"
)
extractedMetrics = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/metrics"


# %% Import files
# List all files in the directory
file_paths = [
    os.path.join(rawMetrics, file)
    for file in os.listdir(rawMetrics)
    if file.endswith(".csv")
]
file_paths = sorted(file_paths)

# Import file
l_metrics = [pd.read_csv(name, header=[0], skiprows=[1]) for name in file_paths]

# %% Convert Date column to datetime - 2 formats in different files
for i, df in enumerate(l_metrics):
    try:
        l_metrics[i]["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%y %H:%M:%S")
    except ValueError:
        try:
            l_metrics[i]["Date"] = pd.to_datetime(
                df["Date"], format="%d.%m.%Y %H:%M:%S"
            )
        except ValueError:
            # Handle parsing failure
            print("Unable to parse date strings in DataFrame index:", i)


# %%
# Concat together
df_metrics = pd.concat(l_metrics)

# In case there I have uploaded the same file twice (it will have a different fileName), I have to delete duplicates
df_metrics = df_metrics.round(
    8
)  # If two files of the same session have different format
df_metrics = df_metrics.map(
    lambda x: x.strip() if isinstance(x, str) else x
)  # Remove trailing whitespaces from all columns
df_metrics = df_metrics.drop_duplicates()

# Sort by Date
df_metrics = df_metrics.sort_values(by="Date")

# %% Add Shot type to the data frame
df_metrics["shot_direction"] = df_metrics["Launch Direction"].apply(shot_direction)
df_metrics["shot_curvature"] = df_metrics["Sidespin"].apply(shot_curvature)
df_metrics["shot_type"] = df_metrics.apply(
    lambda row: shotType(row["shot_direction"], row["shot_curvature"]), axis=1
)

# %% Export data frame
df_metrics.to_csv(os.path.join(extractedMetrics, "MergedMetrics.csv"))

# %%
