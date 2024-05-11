# %%
import os
import re
import pandas as pd
import datetime
from SwingNet import export_SwingNet_video


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

# %%
export_SwingNet_video(
    inp_video_path="/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Videos/1575B739-F5FD-4F2D-9B81-8EBEAC2875712024-04-16/Shot13.mp4",
    out_video_path="/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/videos/1.mp4",
    model_path="/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/DatasetGeneration/SwingNet/models/swingnet_2000.pth.tar",
)

# %%
