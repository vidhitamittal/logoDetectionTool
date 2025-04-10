# pylint: disable=no-member
import yt_dlp
import subprocess
import csv
import cv2
import os
import time
import re

# Gets the metadata with the ytdlp extract info stuff and then it gets the duration field which gives the duration
def get_video_duration(url):
    ytdlp_options = {'quiet': True, 'no_warnings': True,}
    with yt_dlp.YoutubeDL(ytdlp_options) as yt:
        info = yt.extract_info(url, download=False)
        return info.get("duration", 0)



def find_crop(url):
# finish our actual command, figure out output of it
#at least hold: original video dimensions, cropped video dimensions 
#output gives us cropped dimensions, does not crop actual video 
   
   
    commandCrop = (
        'ffmpeg', '-i', f'{url}', '-vf', 'cropdetect','metadata=mode=print', '-f' #, 'null -'

    )
    result = subprocess.run(commandCrop, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, test=True) # DEVNULL

    crop_values = re.findall(r'crop=\d+:\d+:\d+:\d+', result.stderr)

    # Just get the most frequent or last one
    if crop_values:
        print(f"🔍 Suggested crop for {video_id}: {crop_values[-1]}")
    else:
        print(f"⚠️ No crop suggestion found for {video_id}")

    # Clean up
    if os.path.exists(f'{video_id}.mp4'):
        os.remove(f'{video_id}.mp4')





# this is gonna have arrays of each videos first, middle, and last frames    
video_frames = []

with open('videos.csv', mode='r') as video:
    
    the_row = next(csv.reader(video))
    count = 0
    
    # im going through the csv file
    for video_id in the_row:
        count+=1
        
        url = "https://www.youtube.com/watch?v=" + video_id
        print(f'---------------------------------------------\n🎬 Starting video #{count}\n---------------------------------------------')
        


        find_crop(url)

        
        print(f'🪺 Sleep #{count} videos finished')
        time.sleep(2)
        
print("success")
        