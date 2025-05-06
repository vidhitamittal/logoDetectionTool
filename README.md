# logoDetectionTool
In collaboration with the Initiative for Digital Public Infrastructure, through UMass CICS's Early Research Scholars Program (CICS 290A and COMPSCI 396A).

Given a YouTube video, how can we tell if it's reposted from another platform? We identified two important characteristics: a) orienation, because lots of content is reposted from platforms optimized for a mobile phone; and b) a watermark or logo, since when you download videos from other platforms, those platforms often add their logo in the download process. Our orientation detector ended up being more accurate and faster (99% accuracy) than our logo detector (85%), so in data collection, we first ran the orientation detector, then ran the logo detector on any videos that came back as vertical.

We made heavy use of YT-DLP and OpenCV, which you should install in order to use our tools. YT-DLP updates frequently, so make sure your version is up-to-date. We also experimented with FFMPEG, although it didn't end up in the final version.

## Orientation Detection
Jashika and Lance's portion of the project. The orientation detector gets the "true" orientation of a set of randomly-sampled videos by downloading them, cropping out pillarboxing, and accessing the metadata of the cropped video. To run the orientation detector, upload a CSV of your choice where ONLY video IDs (not full URLs) are all in one row, and input the name of the CSV file in line 82. The detector will skip over any videos that are not accessible (private account, deleted video, etc.) and output a CSV only for the videos that worked with columns for the video ID, width in px, height in px, and orientation.

## Logo Detection
James and Vidhita's portion of the project. Binary classifier - whether or not a given video has a logo from a third-party app.

## Future Work
Optimize orientation detection, as right now it works by downloading the entire video. Detect exactly which logo is displayed, rather than just if there is one or not.
