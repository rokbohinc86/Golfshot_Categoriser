# %%
import argparse
import cv2
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from eval import ToTensor, Normalize
from model import EventDetector
from test_video import SampleVideo
import torch.nn.functional as F
import sys
import numpy as np
from moviepy.editor import ImageSequenceClip
import matplotlib.pyplot as plt


def init_data(video_path):
    ds = SampleVideo(
        path=video_path,
        transform=transforms.Compose(
            [ToTensor(), Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]
        ),
    )

    dl = DataLoader(dataset=ds, batch_size=1, shuffle=False, drop_last=False)

    return dl


def init_model(modelpath):
    model = EventDetector(
        pretrain=True,
        width_mult=1.0,
        lstm_layers=1,
        lstm_hidden=256,
        bidirectional=True,
        dropout=False,
    )

    model.load_state_dict(torch.load(modelpath)["model_state_dict"])
    model.to(torch.device("cpu"))
    model.eval()

    return model


def calc_probs(dl, model, seq_length):
    probs = []
    for sample in dl:
        images = sample["images"]
        batch = 0
        # full samples do not fit into GPU memory so evaluate sample in 'seq_length' batches
        while batch * seq_length < images.shape[1]:
            if (batch + 1) * seq_length > images.shape[1]:
                image_batch = images[:, batch * seq_length :, :, :, :]
            else:
                image_batch = images[
                    :, batch * seq_length : (batch + 1) * seq_length, :, :, :
                ]
            logits = model(image_batch)

            if batch == 0:
                probs = F.softmax(logits.data, dim=1).cpu().numpy()
            else:
                probs = np.append(probs, F.softmax(logits.data, dim=1).cpu().numpy(), 0)
            batch += 1

    return probs


def get_cron_events(probs):
    cron_events = []
    event = 0
    for i in range(0, probs.shape[1] - 1):
        event = event + np.argmax(probs[event:, i])
        cron_events.append(event)

    return cron_events


def get_event_prob(probs, events):
    confidence = []
    for i, e in enumerate(events):
        confidence.append(round(probs[e, i] * 100))

    return confidence


def copmpose_frames(cap, events):
    """
    Save key frames of the golf shot into a list of rgb object

    Parameters:
    cap (cv2.VideoCapture): An already created VideoCapture object.
    events (list of tuples): List of tuples where each tuple contains a label, a frame index, and a probability.

    Returns:
    List of rgb objects
    """
    # Check if video capture object was successfully opened
    if not cap.isOpened():
        print("Error: Video capture not open.")
        return

    frames = []
    # Loop through each tuple in the events list and process the frames
    for i, frame_index in enumerate(events):
        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        # Read the frame
        ret, frame = cap.read()
        if ret:
            # Convert the image from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
        else:
            print(f"Failed to retrieve frame at index {frame_index}")

    return frames


def export_SwingNet_video(
    inp_video_path: str, out_video_path: str, model_path: str, seq_length: int = 64
) -> None:
    """This function extracts the key frames of a golfshot based on the SwingNet model and exports
        a truncated video consisting only of the key frames to the desired output path.

    Args:
        inp_video_path (str): Path to the input mp4 video
        out_video_path (str): Path to which the output mp4 video should be exported
        model_path (str): Path to the SwingNet model
        seq_length (int): Number of frames to use per forward pass
    """
    # Initialize data and model
    dl = init_data(inp_video_path)
    model = init_model(modelpath=model_path)

    # Calculate key Frames
    probs = calc_probs(dl, model, seq_length)
    events = get_cron_events(probs)

    # Create a mp4 video
    cap = cv2.VideoCapture(inp_video_path)
    frames = copmpose_frames(cap, events)
    clip = ImageSequenceClip(frames, fps=4)
    clip.write_videofile(out_video_path, codec="libx264")



if __name__ == "__main__":
    export_SwingNet_video(
        inp_video_path="/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Videos/1575B739-F5FD-4F2D-9B81-8EBEAC2875712024-04-16/Shot13.mp4",
        out_video_path="/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/DatasetGeneration/SwingNet/output_video.mp4",
        model_path="/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/DatasetGeneration/SwingNet/models/swingnet_2000.pth.tar",
    )

# %%
