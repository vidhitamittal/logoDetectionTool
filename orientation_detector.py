# pylint: disable=no-member
import yt_dlp
import subprocess
import csv
import cv2
import os
import time

def save_dimensions_to_csv(url, width, height, ratio, csv_filename="video_dimensions.csv"):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([url, width, height, ratio])
        
def get_video_dimensions(url):
    output_file = "temp_segment.mp4"
    if os.path.exists(output_file):
        os.remove(output_file)


    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'outtmpl': output_file
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    find_crop(output_file)
    cap = cv2.VideoCapture(output_file)
   
    if not cap.isOpened():
        print("nope")
        return None, None
   
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
   
    cap.release()

    ratio = "square"
    if height > width:
        ratio = "vertical"
    elif width > height:
        ratio = "horizontal"
    
    return width, height, ratio


#tried by commenting out 

def find_crop(output_file):
    #output_file = "temp_segment.mp4"
    
    #ydl_opts = {
    #    'quiet': True,
    #    'no_warnings': True,
    #    'outtmpl': output_file
    #}
    #with yt_dlp.YoutubeDL(ydl_opts) as ydl:
     #   ydl.download([url])
        
    commandCrop = (
        f'ffmpeg -i {output_file} -vf cropdetect,metadata=mode=print -f null -'
    )
    subprocess.run(commandCrop, shell = True)
    print('should have printed the crop values.')
    
  #  if os.path.exists(output_file):
   #     os.remove(output_file)
    #    print("Temporary video deleted.")
    



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


        width, height, ratio = get_video_dimensions(url)
        if (width and height):
            save_dimensions_to_csv(video_id, width, height, ratio)

        
        print(f'🪺 Sleep #{count} videos finished')
        time.sleep(2)
        
print("success")


   # instead: for each video in csv, pass through get_dimensions.
    # call find_crop on video
    # find_crop calls crop detect, if crop detection is required, return dimensions of new video
    # call crop on video with new dimensions, save output_file as this now?
    # then do ratio stuff on it and return. 

    #for now: call find_crop on each video
    # this downloads full video..... call crop detect, and do simple print output
# if crop exists, should giv e



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
