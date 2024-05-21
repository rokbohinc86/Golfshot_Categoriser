import os
import re
import pandas as pd


def date_as_name(df: pd.DataFrame, path: str) -> str:
    """Generate a file name based on the smallest Date value in the data frame.

    Args:
        df (pd.DataFrame): Data frame containing a column Date
        path (str): Path to the metrics files

    Returns:
        str: File name based on the smallest value of the Date column
    """
    date = df["Date"].iloc[0]  # Get the first (smallest) date value
    new_name = "DrivingRange_" + re.sub(r"[:.\s]", "_", date) + ".csv"
    new_path = os.path.join(path, new_name)
    return new_path


def list_csv_files(directory: str) -> list:
    """List all CSV files in the specified directory.

    Args:
        directory (str): Directory path

    Returns:
        list: List of CSV file paths
    """
    return [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".csv")
    ]


def load_metrics(files: list) -> list:
    """Load metrics from CSV files into data frames.

    Args:
        files (list): List of CSV file paths

    Returns:
        list: List of data frames
    """
    return [pd.read_csv(file, header=[0], skiprows=[1]) for file in files]


def rename_files(file_paths: list):
    """Rename files based on new paths generated from data frame dates.

    Args:
        file_paths (list): List of tuples containing old and new file paths
    """
    for old_path, new_path in file_paths:
        os.rename(old_path, new_path)


def main():
    metrics_folder = (
        "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Metrics"
    )

    # List all CSV files in the directory
    old_paths = list_csv_files(metrics_folder)

    # Load metrics from CSV files
    metrics_list = load_metrics(old_paths)

    # Generate new paths based on the Date column
    new_paths = [date_as_name(df=df, path=metrics_folder) for df in metrics_list]
    file_paths = list(zip(old_paths, new_paths))

    # Rename files
    rename_files(file_paths)


if __name__ == "__main__":
    main()
