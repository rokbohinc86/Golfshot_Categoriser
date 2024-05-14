# %%
import os
import re
import pandas as pd
import datetime
import sys

project_path = '/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/DatasetGeneration/SwingNet'

if project_path not in sys.path:
    sys.path.append(project_path)

# SwingNet package files
from SwingNet.ExtractFrames import export_SwingNet_videos


# %% Metrics
# Import file
metricsFolder = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/metrics/MergedMetrics.csv"
df_metrics = pd.read_csv(metricsFolder, header=[0], skiprows=[1])

# Format date
df_metrics["Date"] = pd.to_datetime(df_metrics["Date"])


# %% Videos
videosFolder = (
    "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Videos"
)

video_paths = []
# Walk through all subdirectories and collect file paths
for root, dirs, files in os.walk(videosFolder):
    for file in files:
        if file.endswith(".mp4"):
            video_paths.append(os.path.join(root, file))

df_videos = pd.DataFrame({"videoPath": video_paths})
df_videos["Date"] = [
    datetime.datetime.fromtimestamp(os.path.getmtime(path))
    for path in df_videos["videoPath"]
]
df_videos = df_videos.sort_values(by="Date")


# %% Merge
merged = pd.merge_asof(
    df_videos,
    df_metrics,
    on="Date",
    suffixes=("_videos", "_metrics"),
    tolerance=pd.Timedelta("2s"),
    direction="nearest",
)


data_7i = merged[merged['Club Type'] == "7 Iron"]
# Add shot_number in order to make sure the videos and the lables are refferencing the same shot
# Adding row number column starting from 1
data_7i['shot_number'] = range(1, len(data_7i) + 1)
export_path = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/videos/" 
data_7i['export_path'] = export_path + data_7i['shot_number'].astype(str) + ".mp4"


# %%
if __name__ == "__main__":
    video_paths = list(zip(data_7i["videoPath"], data_7i['export_path']))
    modelpath = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/DatasetGeneration/SwingNet/models/swingnet_2000.pth.tar"
    export_SwingNet_videos(video_paths = video_paths,
                           modelpath = modelpath)