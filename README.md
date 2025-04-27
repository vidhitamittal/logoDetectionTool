# logoDetectionTool
In collaboration with the Initiative for Digital Public Infrastructure, through UMass CICS's Early Research Scholars Program (CICS 290A and COMPSCI 396A).
Made heavy use of YT-DLP and OpenCV; some experimentation with FFMPEG, although it didn't end up in the final version.

## Orientation Detection
Jashika and Lance's portion of the project. Get the "true" orientation of a set of randomly-sampled videos by downloading them, cropping out pillarboxing, and accessing the metadata of the cropped video.

## Logo Detection
James and Vidhita's portion of the project. Binary classifier - whether or not a given video has a logo from a third-party app.

## Future Work
Optimize orientation detection, as right now it works by downloading the entire video. Detect exactly which logo is displayed, rather than just if there is one or not.
