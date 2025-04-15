# pylint: disable=no-member
import yt_dlp
import subprocess
import csv
import cv2
import os
import time

# Gets the metadata using yt_dlp to extract info and then gets the duration field.
def get_video_duration(url):
    ytdlp_options = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ytdlp_options) as yt:
        info = yt.extract_info(url, download=False)
        return info.get("duration", 0)

def get_frame(url, start_time, output_file):
    # Download a small segment (0.05 seconds) starting at start_time.
    segment_duration = 0.05
    end_time = start_time + segment_duration
    segment_file = "temp_segment.mp4"
    
    # Download only the required section.
    # Note: start_time and end_time are in seconds.
    command = (
        f'yt-dlp --download-sections "*{start_time}-{end_time}" -f best '
        f'-o "{segment_file}" "{url}"'
    )
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Extract a single frame from the downloaded segment.
    # Because the segment’s timeline starts at 0, we seek from 0.
    command = (
        f'ffmpeg -hide_banner -loglevel error -ss 0 -i "{segment_file}" '
        f'-vframes 1 -q:v 2 -pix_fmt yuvj420p "{output_file}"'
    )
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    # Remove the temporary segment file.
    os.remove(segment_file)

def get_frames():
    # This will store arrays for each video's first, middle, and last frames.
    video_frames = []

    with open('videos.csv', mode='r') as video:
        the_row = next(csv.reader(video))
        count = 0

        # Loop through each video ID in the CSV.
        for video_id in the_row:
            count += 1
            url = "https://www.youtube.com/watch?v=" + video_id
            print(f'---------------------------------------------\n🎬 Starting video #{count}\n---------------------------------------------')
            
            # Try to get the video's duration. If an exception occurs, skip the video.
            try:
                duration = get_video_duration(url)
            except Exception as e:
                print(f"❌ Error retrieving duration for video {url}: {e}. Skipping video.")
                continue
            
            # If no valid duration is found, skip the video.
            if not duration or duration <= 0:
                print(f"❌ No valid duration for video {url}. Skipping video.")
                continue

            # Calculate times for first, middle, and last frames.
            first_second = duration * 0.01
            middle_second = duration * 0.5
            last_second = duration * 0.9

            # Temporary filenames for the frame images.
            first_file = f"{video_id}_first.jpg"
            middle_file = f"{video_id}_middle.jpg"
            last_file = f"{video_id}_last.jpg"
            
            try:
                # Download and extract frames.
                get_frame(url, first_second, first_file)
                print(f'🥚 Got first frame for video {count}: {url}')
                get_frame(url, middle_second, middle_file)
                print(f'🐣 Got middle frame for video {count}: {url}')
                get_frame(url, last_second, last_file)
                print(f'🐥 Got last frame for video {count}: {url}')
            except Exception as e:
                print(f"❌ Error retrieving frames for video {url}: {e}. Skipping video.")
                # Remove any files that may have been created.
                for f in [first_file, middle_file, last_file]:
                    if os.path.exists(f):
                        os.remove(f)
                continue

            # Read the images.
            first_img = cv2.imread(first_file)
            middle_img = cv2.imread(middle_file)
            last_img = cv2.imread(last_file)

            # Append the frames along with the video's URL.
            video_frames.append([url, first_img, middle_img, last_img])
            
            # Remove temporary files.
            for f in [first_file, middle_file, last_file]:
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"❌ Error removing temporary file {f}: {e}")

            print(f'🪺 Sleep #{count} videos finished')
            time.sleep(2)
        
    return video_frames
        
print("success")
print('hi github')
