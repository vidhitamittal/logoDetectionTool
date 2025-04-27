# pylint: disable=no-member
import yt_dlp
import subprocess
import csv
import cv2
import os
import time

# Gets the metadata with the ytdlp extract info stuff and then it gets the duration field which gives the duration
def get_video_duration(url):
    ytdlp_options = {'quiet': True, 'no_warnings': True,}
    with yt_dlp.YoutubeDL(ytdlp_options) as yt:
        info = yt.extract_info(url, download=False)
        return info.get("duration", 0)

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

with open('vidhita_hindi_10.csv', mode='r') as video:
    the_row = next(csv.reader(video))
    count = 0
    
    # im going through the csv file
    for video_id in the_row:
        count+=1
        try:
            url = "https://www.youtube.com/watch?v=" + video_id
            print(f'---------------------------------------------\n🎬 Starting video #{count}, {video_id}\n---------------------------------------------')
            #creates url


            # save output of find_crop 
            #find_crop(url, video_id)

            width, height, ratio = get_video_dimensions(url)
            if (width and height):
                save_dimensions_to_csv(video_id, width, height, ratio)

        
            print(f'🪺 Sleep #{count} videos finished')
            time.sleep(2)
        except:
            print('nope lol')
        
print("success")