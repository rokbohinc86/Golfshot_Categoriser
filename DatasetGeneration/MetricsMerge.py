import os
import pandas as pd
from typing import List


# %% Shot-shape functions
def shot_direction(
    launch_direction: float, pull_border: float = -5, push_border: float = 5
) -> str:
    """Determine shot direction based on launch direction."""
    if launch_direction < pull_border:
        return "PULL"
    elif launch_direction > push_border:
        return "PUSH"
    else:
        return "STRAIGHT"


def shot_curvature(
    sidespin: float,
    slice_border: float = -800,
    fade_border: float = -300,
    draw_border: float = 300,
    hook_border: float = 800,
) -> str:
    """Determine shot curvature based on sidespin."""
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


def shot_type(direction: str, curvature: str) -> str:
    """Determine shot type based on direction and curvature."""
    if direction == "PULL":
        if curvature == "HOOK":
            return "PULL_HOOK"
        elif curvature == "DRAW":
            return "PULL_DRAW"
        elif curvature == "NEUTRAL":
            return "PULL"
        elif curvature == "FADE":
            return "PULL_FADE"
        elif curvature == "SLICE":
            return "PULL_SLICE"
    elif direction == "STRAIGHT":
        if curvature == "HOOK":
            return "STRAIGHT_HOOK"
        elif curvature == "DRAW":
            return "STRAIGHT_DRAW"
        elif curvature == "NEUTRAL":
            return "STRAIGHT"
        elif curvature == "FADE":
            return "STRAIGHT_FADE"
        elif curvature == "SLICE":
            return "STRAIGHT_SLICE"
    elif direction == "PUSH":
        if curvature == "HOOK":
            return "PUSH_HOOK"
        elif curvature == "DRAW":
            return "PUSH_DRAW"
        elif curvature == "NEUTRAL":
            return "PUSH"
        elif curvature == "FADE":
            return "PUSH_FADE"
        elif curvature == "SLICE":
            return "PUSH_SLICE"
    return "NO_CATEGORY"


# %% File paths
RAW_METRICS_PATH = (
    "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Metrics"
)
EXTRACTED_METRICS_PATH = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/metrics"


# %% Utility functions
def list_csv_files(directory: str) -> List[str]:
    """List all CSV files in the specified directory."""
    return sorted(
        [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if file.endswith(".csv")
        ]
    )


def load_metrics(files: List[str]) -> List[pd.DataFrame]:
    """Load metrics from CSV files into data frames."""
    return [pd.read_csv(file, header=[0], skiprows=[1]) for file in files]


def parse_dates(metrics: List[pd.DataFrame]) -> List[pd.DataFrame]:
    """Parse Date column in different formats."""
    for i, df in enumerate(metrics):
        try:
            metrics[i]["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%y %H:%M:%S")
        except ValueError:
            try:
                metrics[i]["Date"] = pd.to_datetime(
                    df["Date"], format="%d.%m.%Y %H:%M:%S"
                )
            except ValueError:
                print("Unable to parse date strings in DataFrame index:", i)
    return metrics


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and deduplicate the data frame."""
    df = df.round(8)  # Round to handle precision issues

    # Remove trailing whitespaces from string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()

    df = df.drop_duplicates()
    return df.sort_values(by="Date")


def add_shot_types(df: pd.DataFrame) -> pd.DataFrame:
    """Add shot direction, curvature, and type to the data frame."""
    df["shot_direction"] = df["Launch Direction"].apply(shot_direction)
    df["shot_curvature"] = df["Sidespin"].apply(shot_curvature)
    df["shot_type"] = df.apply(
        lambda row: shot_type(row["shot_direction"], row["shot_curvature"]), axis=1
    )
    return df


def export_data(df: pd.DataFrame, path: str):
    """Export the data frame to a CSV file."""
    df.to_csv(path, index=False)


def main():
    # List and load CSV files
    file_paths = list_csv_files(RAW_METRICS_PATH)
    metrics_list = load_metrics(file_paths)

    # Parse dates and clean data
    metrics_list = parse_dates(metrics_list)
    df_metrics = pd.concat(metrics_list)
    df_metrics = clean_data(df_metrics)

    # Add shot types and export data
    df_metrics = add_shot_types(df_metrics)
    export_data(df_metrics, os.path.join(EXTRACTED_METRICS_PATH, "MergedMetrics.csv"))


if __name__ == "__main__":
    main()
