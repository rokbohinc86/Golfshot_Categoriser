import argparse
import cv2
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from model import EventDetector
import numpy as np
import torch.nn.functional as F

event_names = {
    0: "Address",
    1: "Toe-up",
    2: "Mid-backswing (arm parallel)",
    3: "Top",
    4: "Mid-downswing (arm parallel)",
    5: "Impact",
    6: "Mid-follow-through (shaft parallel)",
    7: "Finish",
}


class SampleVideo(Dataset):
    def __init__(self, path, input_size=160, transform=None):
        self.path = path
        self.input_size = input_size
        self.transform = transform

    def __len__(self):
        return 1

    def __getitem__(self, idx):
        cap = cv2.VideoCapture(self.path)
        frame_size = [
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        ]
        ratio = self.input_size / max(frame_size)
        new_size = tuple([int(x * ratio) for x in frame_size])
        delta_w = self.input_size - new_size[1]
        delta_h = self.input_size - new_size[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        # preprocess and return frames
        images = []
        for pos in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            _, img = cap.read()
            resized = cv2.resize(img, (new_size[1], new_size[0]))
            b_img = cv2.copyMakeBorder(
                resized,
                top,
                bottom,
                left,
                right,
                cv2.BORDER_CONSTANT,
                value=[0.406 * 255, 0.456 * 255, 0.485 * 255],
            )  # ImageNet means (BGR)

            b_img_rgb = cv2.cvtColor(b_img, cv2.COLOR_BGR2RGB)
            images.append(b_img_rgb)
        cap.release()
        labels = np.zeros(len(images))  # only for compatibility with transforms
        sample = {"images": np.asarray(images), "labels": np.asarray(labels)}
        if self.transform:
            sample = self.transform(sample)
        return sample
