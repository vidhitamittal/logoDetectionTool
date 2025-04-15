
# # pylint: disable=no-member
# import yt_dlp
# import subprocess
# import csv
# import cv2
# import os
# import time

# # Gets the metadata with the ytdlp extract info stuff and then it gets the duration field which gives the duration
# def get_video_duration(url):
#     ytdlp_options = {'quiet': True, 'no_warnings': True,}
#     with yt_dlp.YoutubeDL(ytdlp_options) as yt:
#         info = yt.extract_info(url, download=False)
#         return info.get("duration", 0)

# def get_frame(url, start_time, output_file):
#     # download a small segment .05 seconds starting at start_time.
#     segment_duration = .05
#     end_time = start_time + segment_duration
#     segment_file = "temp_segment.mp4"
    
#     # Download only the required section.
#     # Note: start_time and end_time are in seconds.
#     command = (
#         f'yt-dlp --download-sections "*{start_time}-{end_time}" -f best '
#         f'-o "{segment_file}" "{url}"'
#     )
#     subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    
#     # Now extract a single frame from the downloaded segment.
#     # Because the segment’s timeline starts at 0, we seek from 0 (or a small offset if desired).
#     command = (
#         f'ffmpeg -hide_banner -loglevel error -ss 0 -i "{segment_file}" '
#         f'-vframes 1 -q:v 2 -pix_fmt yuvj420p "{output_file}"'
#     )
#     subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
#     # Remove the temporary segment file.
#     os.remove(segment_file)
    
# # this is gonna have arrays of each videos first, middle, and last frames    
# video_frames = []

# with open('videos.csv', mode='r') as video:
    
#     the_row = next(csv.reader(video))
#     count = 0
    
#     # im going through the csv file
#     for video_id in the_row:
#         count+=1
        
#         url = "https://www.youtube.com/watch?v=" + video_id
#         print(f'---------------------------------------------\n🎬 Starting video #{count}\n---------------------------------------------')
        
#         duration = get_video_duration(url)
        
#         first_second = duration * .01
#         middle_second = duration *.5
#         last_second = duration * .9
        
#         # temporarily making images of the files
#         first_file = f"{video_id}_first.jpg"
#         middle_file = f"{video_id}_middle.jpg"
#         last_file = f"{video_id}_last.jpg"
        
#         # get the frames from the beginning middle and end.
#         get_frame(url, first_second, first_file)
#         print(f'🥚 Got first frame for video {count}: {url}')
#         get_frame(url, middle_second, middle_file)
#         print(f'🐣 Got middle frame for video {count}: {url}')
#         get_frame(url, last_second, last_file)
#         print(f'🐥 Got last frame for video {count}: {url}')
    
#         first_img = cv2.imread(first_file)
#         middle_img = cv2.imread(middle_file)
#         last_img = cv2.imread(last_file)
        
#         # put all the frames in an array with the url so we know which videos have the frames
#         video_frames.append([url ,first_img, middle_img, last_img])
        
#         # get rid of the temporary files.
#         os.remove(first_file)
#         os.remove(middle_file)
#         os.remove(last_file)
        
#         print(f'🪺 Sleep #{count} videos finished')
#         time.sleep(2)
        
# print("success")
        
        
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

def save_dimensions_to_csv(url, width, height, csv_filename="video_dimensions.csv"):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([url, width, height])


def get_video_dimensions(url):
    output_file = "temp_segment.mp4"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'outtmpl': output_file 
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    cap = cv2.VideoCapture(output_file)
   
    if not cap.isOpened():
        print("nope")
        return None, None
   
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
   
    cap.release()
    print(width, height)
    return width, height


def find_crop(url, video_id):
# finish our actual command, figure out output of it
#at least hold: original video dimensions, cropped video dimensions 
#output gives us cropped dimensions, does not crop actual video 
    output_file = "temp_segment.mp4"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'outtmpl': output_file
       # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'  # Optional: gets best MP4
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
  
   
   #we need to download each video, pass into crop detect
    commandCrop = (
        'ffmpeg', '-i', output_file, '-vf', 'cropdetect',  '-frames:v', '100', '-f' , 'null -'

    )
    subprocess.run(commandCrop)
    
    if os.path.exists(output_file):
        os.remove(output_file)
        print("Temporary video deleted.")
    
    #boolean in csv: is it cropped. log the console output there. handle errors properly if ur fancy?
    #crop detect is giving dimensions in the console. to catch this, 
    # u can use dummy variables, 
    
    
    #result = subprocess.run(commandCrop, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True) # DEVNULL

    #crop_values = re.findall(r'crop=\d+:\d+:\d+:\d+', result.stderr)
    #print(crop_values)
    # Just get the most frequent or last one
    #if crop_values:
    #    print(f"Suggested crop for {video_id}: {crop_values}")
    #else:
    #    print(f"No crop suggestion found for {video_id}")

    # Clean up
    #if os.path.exists(f'{video_id}.mp4'):
    #    os.remove(f'{video_id}.mp4')
#check onedrive? consider turning that off for this project 



# this is gonna have arrays of each videos first, middle, and last frames    
video_frames = []

with open('videos.csv', mode='r') as video:
    #goes through each video in videos.csv
    the_row = next(csv.reader(video))
    count = 0
    
    # im going through the csv file
    for video_id in the_row:
        count+=1
        
        url = "https://www.youtube.com/watch?v=" + video_id
        print(f'---------------------------------------------\n🎬 Starting video #{count}\n---------------------------------------------')
        #creates url


      # save output of find_crop 
        #find_crop(url, video_id)

        width, height = get_video_dimensions(url)
        if (width and height):
            save_dimensions_to_csv(video_id, width, height)

        
        print(f'🪺 Sleep #{count} videos finished')
        time.sleep(2)
        
print("success")
