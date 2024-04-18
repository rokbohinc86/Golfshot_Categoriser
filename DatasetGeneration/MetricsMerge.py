# %%
import os
import pandas as pd

# File paths
rawMetrics = (
    "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Metrics"
)
extractedMetrics = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/metrics"

# %%
# List all files in the directory
file_paths = [
    os.path.join(rawMetrics, file)
    for file in os.listdir(rawMetrics)
    if file.endswith(".csv")
]
file_paths = sorted(file_paths)

# Import file
l_metrics = [pd.read_csv(name, header=[0], skiprows=[1]) for name in file_paths]

# %%
# Convert Date column to datetime - 2 formats in different files
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
# %%
# Export data frame
df_metrics.to_csv(os.path.join(extractedMetrics, "MergedMetrics.csv"))
