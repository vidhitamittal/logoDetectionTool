# pylint: disable=no-member
import cv2
import csv


video = cv2.VideoCapture('test.mp4')
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

percentage_intervals = [0, 10, 15, 20, 25, 50, 75, 99]

frame_indices = [int(total_frames * (p / 100)) for p in percentage_intervals]

count = 1
for frame_index in frame_indices:
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    success, image = video.read()
    if success:
        count += 1
        cv2.imwrite(f"frame_{count}.jpg", image)
    else:
        print(f"Failed to retrieve frame at {frame_index}.")
video.release()
print(f"Extracted {count} frames based on percentage intervals.")
