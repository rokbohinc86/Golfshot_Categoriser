# Golfshot_Categoriser

## Problem Definition

This is a computer vision application for the categorization of golf shot types. The algorithm focuses only on the horizontal classification of the shot and does not consider the length of the shot or its vertical shape. Based on a video of a golf swing the
model predicts one of the following golf shot shapes/types:

- pull hook
- pull draw
- pull
- pull fade
- pull slice
- straight hook
- straight draw
- straight
- straight fade
- straight slice
- push hook
- push draw
- push
- push fade
- push slice


## Data

Data will be collected via the Garmin R10 golf shot tracking monitor. This device can be used to record videos and various golf shot metrics. The application involves pairing it with a mobile phone where the Garmin Golf App is installed. The metrics of the driving range session, containing several shots, as well as individual golf shots can be downloaded via the Garmin Golf App. It can be however tedious to download the videos individually. Also, there is no clear key on how to link them to the metrics when downloading them individually. The data on the mobile device cannot be directly accessed. However, linking it with a computer all videos can be accessed. I have done this with the iMazing app on my MacBook.  The videos can be linked with the metric data based on the creation date.

### iMazing

In the free version you get a limited amount of videos you can extract and copy to mac. I have bought a pro licence for 65 CHF (one time price), which lets you use the software to download any amount of videos for up to three devices.

- Open the App
- Create a backup of the device
- In the iMazing app, select the device you have made a backup and go undder File System -> Apps -> Golf -> Backups -> Document
- The metric files are stored in this path
- The videos are stored under the subfolder "output"

### Metrics

The metrics file is a CSV file with each row representing a different shot in the session. The columns contain the following parameters: Date	Player	Club Name	Club Type	Club Speed	Attack Angle	Club Path	Club Face	Face to Path	Ball Speed	Smash Factor	Launch Angle	Launch Direction	Backspin	Sidespin	Spin Rate	Spin Rate Type	Spin Axis	Apex Height	Carry Distance	Carry Deviation Angle	Carry Deviation Distance	Total Distance	Total Deviation Angle	Total Deviation Distance	Note	Tag	Air Density	Temperature	Air Pressure	Relative Humidity. Excluding external factors, such as wind and temperature, the ball flight can be extrapolated with the following parameters:

- Launch Direction
- Launch Angle
- Ball Speed
- Backspin
- Sidespin

To characterize the type of golf shot I mainly need the Launch Direction and Sidespin. Of course, the amount of shaping is a function of the air resistance which is a nonlinear function (I think quadratic should be applicable in this speed regime), but I neglect these effects. The Launch Direction describes if the shot is a pull, push, or a straight shot. The amount of Sidespin determines if the shape is a hook, draw, straight, fade or slice. Here I have to make a rule of thumb on when to classify a shot based on the two parameters. Below is a guideline:

- Launch Direction  ( < -5 ° = pull, straight, > 5 ° = push)
- Sidespin  ( < -800 rpm = slice,  -800 rpm < < -300 rpm = fade, -300 rpm < < 300 rpm = straight, 300 rpm < < 800 rpm = draw, > 800 rpm = hook)

#### Extraction of labels

1 Place the driving range file from Garmin under data/raw/Metrics.
2 Run labelProcessing.py to create the labels of the golf shots. The file will be saved under data/extraced/labels.


### Videos

The general problem with machine learning being applied to videos is that all videos have to be of the same shape, this means resolution and the number of frames. Different numbers of frames can be problematic when the velocity of golf swings varies. Therefore not all frames can be taken as the input. [McNally et. al.](https://arxiv.org/abs/1903.06528) developed a lightweight ML model for finding key positions in a golf swing. The positions were labeled:

- Address 
- Toe-up
- Mid-backswing
- Top, 
- Mid- downswing
- Impact
- Mid-follow-through
- Finish

The model correctly detects eight golf swing events at an average rate of 76.1%, and six out of eight events at a rate of 91.8%. The idea is to extract these 8 characteristic frames for all videos collected in practice sessions with a mobile device via the Garmin Golf App. 

Predicting key frames from a Garmin Golf video runs without a problem by executing test_video.py.

## To Do
- Write a script that takes the path to directories with golf shot videos as an input parameter and for each video extracts and saves the 8 key frames.
- Create a data set of about 1000 videos. Make sure to record videos with various offsets and angles (although this could also be achieved with augmentation), positions on the driving range, etc. 
