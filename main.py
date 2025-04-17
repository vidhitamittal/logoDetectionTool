from detect_logo import detect_logos, load_templates
from extractImageWithYTDLP import get_frames
import multiprocessing as mp
import csv

# Path to your logos folder
logos_folder = "logos"
output_csv = "results.csv"

# Load all logos as grayscale templates
templates = load_templates(logos_folder)

# Get video frame data: [url, first_frame, middle_frame, last_frame]
video_data = get_frames()

def process_video(video_info):
    url, first_frame, middle_frame, last_frame = video_info
    print(f"\nProcessing video: {url}")
    
    frames_dict = {"First": first_frame, "Middle": middle_frame, "Last": last_frame}
    detections_all = []
    logo_detected = False

    for label, frame in frames_dict.items():
        if frame is None:
            print(f"⚠️ {label} frame missing for {url}. Skipping...")
            continue
        
        detections = detect_logos(frame, templates)

        if detections:
            # pick only the highest accuracy detection
            best_detection = max(detections, key=lambda x: x[2])  # x[2] is accuracy %
            logo_detected = True
            detections_all.append((label, best_detection))
            print(f"✅ {label} Frame - Best Logo: {best_detection}")
        else:
            print(f"❌ {label} Frame - No logos detected.")

    return [url, logo_detected, detections_all]
 
if __name__ == "__main__":
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(process_video, video_data)

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Video URL", "Logo Detected", "Detection Details"])
        for r in results:
            writer.writerow([r[0], r[1], str(r[2])])

    print("\n✅ Detection complete. Results saved to:", output_csv)
