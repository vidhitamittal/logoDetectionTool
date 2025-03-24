import yt_dlp
import cv2
import os
import csv

def download_video(url, output_path='downloaded_video.mp4'):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download = True)
        video_file = ydl.prepare_filename(info_dict)
    
    return video_file

def get_video_dimensions(video_file):
    cap = cv2.VideoCapture(video_file)
    
    if not cap.isOpened():
        print("nope")
        return None, None
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cap.release()
    return width, height

def process_csv(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline = '') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        writer.writerow(['url', 'width', 'height'])

        for row in reader:
            url = row[0]
            print(f"Processing {url}...")
            downloaded_video = download_video(url)
            width, height = get_video_dimensions(downloaded_video)
            writer.writerow([url, width, height])
            # print(f"{url}: {width}x{height}")
            os.remove(downloaded_video)

def main():
    process_csv(input_directory, output_directory)

if __name__ == "__main__":
    main()
