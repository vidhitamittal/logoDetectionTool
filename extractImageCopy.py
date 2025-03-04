# import cv2
# from youtubesearchpython import VideosSearch
from pytube import YouTube
import csv

with open('videos.csv', mode='r') as video:
    
    the_row = next(csv.reader(video))
    
    # im going through the csv file
    i = 0
    for video_id in the_row:
        url = "https://www.youtube.com/watch?v=" + video_id
        print("the url" + url + "\n")
        print("Hi hi I am the detection tool and I'm starting test test")

        youtubeObject = YouTube(url)
        print("working 1")
        try:
            YouTube(url).streams.first().download('save_path')
            print("working 3")
            i = i+1
        except Exception as e:
            print(e)
        print(f"Download {i} is completed successfully")
        break
        # video = cv2.VideoCapture('test.mp4')
        # total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # percentage_intervals = [0, 10, 15, 20, 25, 50, 75, 99]

        # frame_indices = [int(total_frames * (p / 100)) for p in percentage_intervals]
            
        # count = 1
        # for frame_index in frame_indices:
        #     video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        #     success, image = video.read()
        #     if success:
        #         count += 1
        #         cv2.imwrite(f"frame_{count}.jpg", image)
        #     else:
        #         print(f"Failed to retrieve frame at {frame_index}.")
        # video.release()
        # print(f"Extracted {count} frames based on percentage intervals.")
        # break