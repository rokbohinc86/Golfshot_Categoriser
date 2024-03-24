import os.path
import datetime

# Path to the video file
video_path = "data/raw/Videos/9B5AF1E9-AE63-4918-B695-702C0E4364A52023-03-25/Shot20.mp4"

# Get the last modification time of the file
modification_time = os.path.getmtime(video_path)
os.path.getctime
# Convert the modification time to a human-readable format
modification_time_readable = datetime.datetime.fromtimestamp(modification_time)

print(f"The video file was last modified on: {modification_time_readable}")
