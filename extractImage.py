import cv2
import csv

# with open('videos.csv', mode ='r')as file: 
#   csvFile = csv.reader(file)
#   for row in csvFile:
#     for col in row:
#         url = "https://www.youtube.com/watch?v=" + col
#         video = cv2.VideoCapture(url)

# the code below works on downloaded videos (e.g. test.mp4)
# I will work on the part above where I can use the video ID's from the csv and 
# download the files to access them within this code after 311 :)

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
