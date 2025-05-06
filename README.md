# logoDetectionTool
In collaboration with the Initiative for Digital Public Infrastructure, through UMass CICS's Early Research Scholars Program (CICS 290A and COMPSCI 396A).

Given a YouTube video, how can we tell if it's reposted from another platform? We identified two important characteristics: a) orientation, because lots of content is reposted from platforms optimized for a mobile phone; and b) a watermark or logo, since when you download videos from other platforms, those platforms often add their logo in the download process. Our orientation detector ended up being more accurate and faster (99% accuracy) than our logo detector (85%), so in data collection, we first ran the orientation detector, then ran the logo detector on any videos that came back as vertical.

We made heavy use of YT-DLP and OpenCV, which you should install in order to use our tools. YT-DLP updates frequently, so make sure your version is up-to-date. We also experimented with FFMPEG, although it didn't end up in the final version.

## Orientation Detection
Jashika and Lance's portion of the project. The orientation detector gets the "true" orientation of a set of randomly-sampled videos by downloading them, cropping out pillarboxing, and accessing the metadata of the cropped video. To run the orientation detector, upload a CSV of your choice where ONLY video IDs (not full URLs) are all in one row, and input the name of the CSV file in line 82. The detector will skip over any videos that are not accessible (private account, deleted video, etc.) and output a CSV only for the videos that worked with columns for the video ID, width in px, height in px, and orientation.

We tested the accuracy of this tool by taking a handful of videos we'd ran it on (300 of 738) and checking if the determined orientation seemed accurate. In this sample, the tool worked correctly for all cases except one video, which was a compilation of other videos with varying orientations.

## Logo Detection
James and Vidhita's portion of the project. The Binary Classifier is a tool that checks whether a given video has a logo or not. We use the OpenCV (cv2) and the ORB feature matching test to check whether a video has a logo. The tool first uses YT-DLP to download a tiny part of the video which ffmpeg then acts on and extracts frames from. Our tool extracts 3 frames from a video, namely beginning, middle and end. The frames are then put through the OpenCV and ORB feature templates. The tool then checks which logo was best detected and if the accuracy percentage of the detection is more than 60%, it says that the video contains a logo, and otherwise it says false. 

## Future Work
Optimize orientation detection, as right now it works by downloading the entire video. The logo detection tool does not currently accurately detect which logo was found in a video so out future work is to make the detector more accurate with logo detection as well as just improve accuracy in detecting whether there is a logo to begin with or not.

## Installation of requirements to run the tools
We have added a requirements.txt on the main branch which can be installed using the command: pip install -r requirements.txt
This will allow the user to get the required libraries to run the tools easily. 
