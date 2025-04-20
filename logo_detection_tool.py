import os
import cv2 as cv
import numpy as np
import yt_dlp
import subprocess
import csv
import time
import concurrent.futures
from functools import partial

# ------------------- TEMPLATE LOADING -------------------
def load_templates(logos_folder):
    templates = {}
    for filename in os.listdir(logos_folder):
        if filename.lower().endswith(('.jpeg', '.png', '.jpg')):
            name = filename.split('.')[0]
            path = os.path.join(logos_folder, filename)
            img = cv.imread(path, cv.IMREAD_GRAYSCALE)
            if img is None or cv.countNonZero(img) < 50:
                continue
            img = cv.equalizeHist(img)
            img = cv.GaussianBlur(img, (3, 3), 0)
            img = cv.resize(img, (64, 64))
            templates[name] = img
    return templates

# ------------------- LOGO DETECTION -------------------
def detect_logos(frame, templates):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
    gray = cv.equalizeHist(gray)
    gray = cv.GaussianBlur(gray, (3, 3), 0)
    edges = cv.Canny(gray, 50, 200)

    detected = []

    for logo_name, template in templates.items():
        res = cv.matchTemplate(gray, template, cv.TM_CCOEFF_NORMED)
        _, template_score, _, _ = cv.minMaxLoc(res)

        temp_edges = cv.Canny(template, 50, 200)
        best = 0
        for scale in np.linspace(0.5, 2.0, 10):
            try:
                resized = cv.resize(temp_edges, None, fx=scale, fy=scale)
            except:
                continue
            if resized.shape[0] > edges.shape[0] or resized.shape[1] > edges.shape[1]:
                continue
            res = cv.matchTemplate(edges, resized, cv.TM_CCOEFF_NORMED)
            _, val, _, _ = cv.minMaxLoc(res)
            best = max(best, val)
        multiscale_score = best

        orb = cv.ORB_create(1000)
        kp1, des1 = orb.detectAndCompute(template, None)
        kp2, des2 = orb.detectAndCompute(gray, None)
        orb_score = 0
        if des1 is not None and des2 is not None:
            bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            if matches:
                orb_score = len(matches) / len(kp1) * 100

        strong_scores = []
        if template_score * 100 >= 60:
            strong_scores.append(template_score * 100)
        if multiscale_score * 100 >= 60:
            strong_scores.append(multiscale_score * 100)
        if orb_score >= 10:
            strong_scores.append(orb_score)

        if len(strong_scores) >= 1:
            final_score = np.mean(strong_scores)
            detected.append((logo_name, "Combined", final_score))

    return detected

# ------------------- VIDEO FRAME EXTRACTION -------------------
def get_video_duration(url):
    ytdlp_options = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ytdlp_options) as yt:
        info = yt.extract_info(url, download=False)
        return info.get("duration", 0)

def get_frame(url, start_time, output_file):
    segment_duration = 0.05
    end_time = start_time + segment_duration
    segment_file = "temp_segment.mp4"

    command = (
        f'yt-dlp --download-sections "*{start_time}-{end_time}" -f best '
        f'-o "{segment_file}" "{url}"'
    )
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    command = (
        f'ffmpeg -hide_banner -loglevel error -ss 0 -i "{segment_file}" '
        f'-vframes 1 -q:v 2 -pix_fmt yuvj420p "{output_file}"'
    )
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    os.remove(segment_file)

def get_frames():
    video_frames = []

    with open('videos.csv', mode='r') as video:
        the_row = next(csv.reader(video))
        count = 0

        for video_id in the_row:
            count += 1
            url = "https://www.youtube.com/watch?v=" + video_id
            print(f'\n🎬 Starting video #{count}: {url}')

            try:
                duration = get_video_duration(url)
            except Exception:
                continue

            if not duration or duration <= 0:
                continue

            first_second = duration * 0.01
            middle_second = duration * 0.5
            last_second = duration * 0.9

            first_file = f"{video_id}_first.jpg"
            middle_file = f"{video_id}_middle.jpg"
            last_file = f"{video_id}_last.jpg"

            try:
                get_frame(url, first_second, first_file)
                get_frame(url, middle_second, middle_file)
                get_frame(url, last_second, last_file)
            except Exception:
                for f in [first_file, middle_file, last_file]:
                    if os.path.exists(f):
                        os.remove(f)
                continue

            first_img = cv.imread(first_file)
            middle_img = cv.imread(middle_file)
            last_img = cv.imread(last_file)

            video_frames.append([url, first_img, middle_img, last_img])

            for f in [first_file, middle_file, last_file]:
                try:
                    os.remove(f)
                except:
                    continue

            time.sleep(1)

    return video_frames

# ------------------- VIDEO PROCESSING -------------------
def get_top_logos(detections, top_n=2):
    return [d[0] for d in sorted(detections, key=lambda x: -x[2])[:top_n]]

def process_video(video_info, templates):
    url, first_frame, middle_frame, last_frame = video_info
    print(f"\nProcessing video: {url}")

    frames_dict = {"First": first_frame, "Middle": middle_frame, "Last": last_frame}
    detections_all = []
    top_logos_all = []

    for label, frame in frames_dict.items():
        if frame is None:
            detections_all.append((label, None))
            top_logos_all.append(set())
            continue

        detections = detect_logos(frame, templates)

        if detections:
            top_logos = get_top_logos(detections)
            detections_all.append((label, detections[0]))
            top_logos_all.append(set(top_logos))
        else:
            detections_all.append((label, None))
            top_logos_all.append(set())

    common_logos = set.intersection(*top_logos_all)
    logo_detected = len(common_logos) > 0

    return [url, logo_detected, detections_all]

# ------------------- MAIN -------------------
def main():
    logos_folder = "logos"
    output_csv = "results.csv"

    templates = load_templates(logos_folder)
    video_data = get_frames()

    func = partial(process_video, templates=templates)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(func, video_data))

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Video URL", "Logo Detected", "Detection Details"])
        for r in results:
            writer.writerow([r[0], r[1], str(r[2])])

    print("\n✅ Detection complete. Results saved to:", output_csv)

if __name__ == "__main__":
    main()
