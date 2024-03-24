# %%
import os
import re
import pandas as pd
from labelExtraction import importFile


def date_as_name(df: pd.DataFrame, path: str) -> str:
    """This function generates a name for the file from which
    the data frame is comming based on the first value of the
    column Date, which is the smallest value.

    Args:
        df (pd.DataFrame): data frame containing a column Date
        path (str): path to the metrics files

    Returns:
        str: file name based on the smalles value of the Date
        column
    """
    date = df["Date"][0]  # Convert day-month-year to year-month-day
    new_name = "DrivingRange_" + re.sub(r"[:.\s]", "_", date) + ".csv"
    new_path = os.path.join(path, new_name)
    return new_path


# Specify the directory path
metricsFolder = (
    "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Metrics"
)

# List all files in the directory
old_paths = [
    os.path.join(metricsFolder, file)
    for file in os.listdir(metricsFolder)
    if file.endswith(".csv")
]

metrics_list = [importFile(path=name) for name in old_paths]
# %%
new_paths = [date_as_name(df=df, path=metricsFolder) for df in metrics_list]
file_paths = list(zip(old_paths, new_paths))


# %%
for old_path, new_path in file_paths:
    os.rename(old_path, new_path)
