from typing import Union
from dataclasses import dataclass
from enum import Enum, auto
import datetime


class ShotType(Enum):
    STRAIGHT = auto()
    PULL = auto()
    PUSH = auto()
    PULL_SLICE = auto()
    STRAIGHT_SLICE = auto()
    PUSH_SLICE = auto()
    PULL_FADE = auto()
    STRAIGHT_FADE = auto()
    PUSH_FADE = auto()
    PULL_DRAW = auto()
    STRAIGHT_DRAW = auto()
    PUSH_DRAW = auto()
    PULL_HOOK = auto()
    STRAIGHT_HOOK = auto()
    PUSH_HOOK = auto()

class ShotDirection(Enum):
    STRAIGHT = auto()
    PULL = auto()
    PUSH = auto()

class ShotCurve(Enum):
    SLICE = auto()
    FADE = auto()
    NEUTRAL = auto()
    DRAW = auto()
    HOOK = auto()

@dataclass
class Shot_Direction():
    launchDirection: float
    pull_border: float = -5
    push_border: float = 5

    @property
    def shotDirection(self) -> ShotDirection:
        """This property categorises the direction of the shot
        based on the launch direction

        Returns:
            ShotDirection: _description_
        """
        if self.launchDirection < self.pull_border:
            return ShotDirection.PULL
        elif self.launchDirection > self.push_border:
            return ShotDirection.STRAIGHT
        else:
            return ShotDirection.PUSH
        
@dataclass
class Shot_Curve():
    sidespin: float
    slice_border: float = -800
    fade_border: float = -300
    draw_border: float = 300
    hook_border: float = 800

    @property
    def shotCurve(self) -> ShotCurve:
        """This property categorises the curvature of the shot
        based on the sidespin

        Returns:
            ShotCurve: the of curvature
        """
        if self.sidespin < self.slice_border:
            return ShotCurve.SLICE
        elif self.sidespin < self.fade_border:
            return ShotCurve.FADE
        elif self.sidespin < self.draw_border:
            return ShotCurve.NEUTRAL
        elif self.sidespin < self.hook_border:
            return ShotCurve.DRAW
        else:
            return ShotCurve.HOOK

@dataclass
class GolfShot:
    metricsFile: Union[str, None]
    videoFile: Union[str, None]
    shotTime: datetime.datetime
    shotName: str
    shotCurve: Shot_Curve 
    shotDirection: Shot_Direction

    @property
    def shotType(self) -> ShotType:
        if self.shotCurve == self.shotDirection == ShotDirection.PULL and ShotCurve.HOOK:
            return ShotType.PULL_HOOK
        elif self.shotDirection == ShotDirection.PULL and self.shotCurve == ShotCurve.DRAW:
            return ShotType.PUSH_DRAW
        elif self.shotDirection == ShotDirection.PULL and self.shotCurve == ShotCurve.NEUTRAL:
            return ShotType.PULL
        elif self.shotDirection == ShotDirection.PULL and self.shotCurve == ShotCurve.FADE:
            return ShotType.PULL_FADE
        elif self.shotDirection == ShotDirection.PULL and self.shotCurve == ShotCurve.SLICE:
            return ShotType.PULL_SLICE
        elif self.shotDirection == ShotDirection.STRAIGHT and self.shotCurve == ShotCurve.HOOK:
            return ShotType.STRAIGHT_HOOK
        elif self.shotDirection == ShotDirection.STRAIGHT and self.shotCurve == ShotCurve.DRAW:
            return ShotType.STRAIGHT_DRAW
        elif self.shotDirection == ShotDirection.STRAIGHT and self.shotCurve == ShotCurve.NEUTRAL:
            return ShotType.STRAIGHT
        elif self.shotDirection == ShotDirection.STRAIGHT and self.shotCurve == ShotCurve.FADE:
            return ShotType.STRAIGHT_FADE
        elif self.shotDirection == ShotDirection.STRAIGHT and self.shotCurve == ShotCurve.SLICE:
            return ShotType.STRAIGHT_SLICE
        elif self.shotDirection == ShotDirection.PUSH and self.shotCurve == ShotCurve.HOOK:
            return ShotType.PUSH_HOOK
        elif self.shotDirection == ShotDirection.PUSH and self.shotCurve == ShotCurve.DRAW:
            return ShotType.PUSH_DRAW
        elif self.shotDirection == ShotDirection.PUSH and self.shotCurve == ShotCurve.NEUTRAL:
            return ShotType.PUSH
        elif self.shotDirection == ShotDirection.PUSH and self.shotCurve == ShotCurve.FADE:
            return ShotType.PUSH_FADE
        elif self.shotDirection == ShotDirection.PUSH and self.shotCurve == ShotCurve.SLICE:
            return ShotType.PUSH_SLICE
        else: 
            return ShotType.PUSH_SLICE
        



if __name__ == "__main__":
    shot1 = GolfShot(metricsFile="data/raw/Metrics/DrivingRange-2024-03-03 13:35:37 +0000.csv",
                     videoFile="data/raw/Videos/8E0BF5BE-C759-4DFA-854C-1B1B4360C7482023-03-25/Shot1.mp4",
                     shotCurve=Shot_Curve(sidespin= 300),
                     shotDirection=Shot_Direction(launchDirection=3),
                     shotTime=datetime.datetime.now(),
                     shotName="1")
    