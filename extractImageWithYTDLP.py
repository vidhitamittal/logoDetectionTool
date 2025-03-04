# pylint: disable=no-member
import yt_dlp
import subprocess
import csv
import cv2
import os

# Gets the metadata with the ytdlp extract info stuff and then it gets the duration field which gives the duration
def get_video_duration(url):
    ytdlp_options = {}
    with yt_dlp.YoutubeDL(ytdlp_options) as yt:
        info = yt.extract_info(url, download=False)
        return info.get("duration", 0)

# just runs the ytdlp frame download command except through code using subprocess
def get_frame(url, start_time, output_file):
    command = (
        f'yt-dlp -f best -o - "{url}" | '
        f'ffmpeg -hide_banner -loglevel error -ss {start_time} -t 5 -i pipe:0 -vframes 1 "{output_file}"'
    )
    subprocess.call(command, shell=True)
    
# this is gonna have arrays of each videos first, middle, and last frames    
video_frames = []

with open('videos.csv', mode='r') as video:
    
    the_row = next(csv.reader(video))
    
    # im going through the csv file
    for video_id in the_row:
        url = "https://www.youtube.com/watch?v=" + video_id
        print("Hi hi I am the detection tool and I'm starting test test")
        
        duration = get_video_duration(url)
        
        first_second = duration * .01
        middle_second = duration *.5
        last_second = duration * .999
        
        # temporarily making images of the files
        first_file = f"{video_id}_first.jpg"
        middle_file = f"{video_id}_middle.jpg"
        last_file = f"{video_id}_last.jpg"
        
        # get the frames from the beginning middle and end.
        get_frame(url, first_second, first_file)
        get_frame(url, middle_second, middle_file)
        get_frame(url, last_second, last_file)
    
        first_img = cv2.imread(first_file)
        middle_img = cv2.imread(middle_file)
        last_img = cv2.imread(last_file)
        
        # put all the frames in an array with the url so we know which videos have the frames
        video_frames.append([url ,first_img, middle_img, last_img])
        
        # get rid of the temporary files.
        os.remove(first_file)
        os.remove(middle_file)
        os.remove(last_file)
        
print("success")
        