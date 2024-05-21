import csv
import os
import pandas as pd
import numpy as np
import datetime
import sys

# Adding project path to system path
project_path = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/DatasetGeneration/SwingNet"
if project_path not in sys.path:
    sys.path.append(project_path)

# Importing necessary functions from SwingNet package
from SwingNet.ExtractFrames import export_SwingNet_videos

def load_metrics(metrics_path):
    """Load and preprocess metrics data."""
    df_metrics = pd.read_csv(metrics_path, header=[0], skiprows=[1])
    df_metrics["Date"] = pd.to_datetime(df_metrics["Date"])
    return df_metrics

def load_videos(videos_folder):
    """Collect video file paths and their modification dates."""
    video_paths = []
    for root, dirs, files in os.walk(videos_folder):
        for file in files:
            if file.endswith(".mp4"):
                video_paths.append(os.path.join(root, file))
    
    df_videos = pd.DataFrame({"videoPath": video_paths})
    df_videos["Date"] = [
        datetime.datetime.fromtimestamp(os.path.getmtime(path))
        for path in df_videos["videoPath"]
    ]
    return df_videos.sort_values(by="Date")

def merge_data(df_videos, df_metrics, tolerance='2s'):
    """Merge video and metrics data based on timestamps."""
    return pd.merge_asof(
        df_videos,
        df_metrics,
        on="Date",
        suffixes=("_videos", "_metrics"),
        tolerance=pd.Timedelta(tolerance),
        direction="nearest",
    )

def filter_shots(data, club_type="7 Iron", filters=[("Apex Height", 10),("Carry Distance", 90)]):
    """Filter shots based on club type and specific criteria."""
    data_filtered = data[data["Club Type"] == club_type]
    for column, value in filters:
        data_filtered = data_filtered[data_filtered[column] > value]
    return data_filtered

def prepare_export_paths(data, export_base_path):
    """Prepare export paths for each video."""
    data["shot_number"] = range(1, len(data) + 1)
    data["export_path"] = export_base_path + data["shot_number"].astype(str) + ".mp4"
    return data

def main():
    metrics_path = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/metrics/MergedMetrics.csv"
    videos_folder = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Videos"
    export_base_path = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/videos/"
    model_path = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/DatasetGeneration/SwingNet/models/swingnet_2000.pth.tar"
    label_path = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/labels/labels.csv"

    # Load and preprocess data
    df_metrics = load_metrics(metrics_path)
    df_videos = load_videos(videos_folder)

    # Merge data
    merged_data = merge_data(df_videos, df_metrics)

    # Filter shots and prepare export paths
    filtered_data = filter_shots(merged_data)
    prepared_data = prepare_export_paths(filtered_data, export_base_path)

    # Export videos using SwingNet
    video_paths = list(zip(prepared_data["videoPath"], prepared_data["export_path"]))
    export_SwingNet_videos(video_paths=video_paths, modelpath=model_path)

    # Save labels
    prepared_data[["shot_type"]].to_csv(label_path, index=False, sep=",", mode="w")

if __name__ == "__main__":
    main()