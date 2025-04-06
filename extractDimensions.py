import yt_dlp
import cv2
import os
import csv
import time
import tempfile
import subprocess

def get_frame_from_vid(id, output_path = 'sampleframe.jpg'):
    url = 'https://www.youtube.com/watch?v=' + id
    ydl_opts = {
        'format': 'worstvideo',
        'quiet': True,
        'noplaylist': True,
        'extractaudio': False,
        'outtmpl': tempfile.mktemp()
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # omg they made streams from cs220 in real life
        info_dict = ydl.extract_info(url, download = True)
        video_file = ydl.prepare_filename(info_dict)

    video_length_cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_file
    ]
    video_length = float(subprocess.check_output(video_length_cmd).strip())

    capture_cmd = [
        'ffmpeg', '-i', video_file, '-vf', f"select='eq(n\,{video_length / 2})'", '-vsync', 'vfr', output_path
    ]
    subprocess.run(capture_cmd, check = True)
    subprocess.run(['rm', video_file])
    return output_path

def get_frame_height(image_path): # image as path
    image = cv2.imread(image_path)
    if image is not None:
        return image.shape[0]
    
def get_frame_width(image_path): # image as path
    image = cv2.imread(image_path)
    if image is not None:
        return image.shape[1]

def process_csv(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        writer.writerow(['url', 'width', 'height'])

        row = next(reader)
        for video_id in row:
            url = video_id
            print(f"Processing {url}...")
            try:
                frame_path = get_frame_from_vid(url)
                height = get_frame_height(frame_path)
                width = get_frame_width(frame_path)
                writer.writerow([url, width, height])
                os.remove(frame_path)
            except:
                print('no lol')
            time.sleep(2)

def main():
    input_directory = 'C:\\Users\\echen\\OneDrive\\Desktop\\umass\\2.4 spring 2025\\Computer Science 396A Independent Study\\logoDetectionTool\\videos.csv'
    output_directory = 'dimensions.csv'
    process_csv(input_directory, output_directory) #erm ig just substitute this on ur computer

if __name__ == "__main__":
    main()