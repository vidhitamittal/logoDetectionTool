import cv2 as cv
import yt_dlp
import os
import shutil

def download_and_extract_frames(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    video_path = os.path.join(output_path, 'video.mp4')

    ydl_opts = {
        'outtmpl': video_path,
        'format': 'mp4',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    cap = cv.VideoCapture(video_path)
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    frames_to_capture = [0, total_frames // 2, total_frames - 1]

    frames = []
    for f in frames_to_capture:
        cap.set(cv.CAP_PROP_POS_FRAMES, f)
        success, frame = cap.read()
        frames.append(frame if success else None)

    cap.release()

    # Auto-delete video
    os.remove(video_path)

    return frames
