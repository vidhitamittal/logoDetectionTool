# from detect_logo import detect_logos, load_templates
# from extractImageWithYTDLP import get_frames
# import csv

# # Path to your logos folder
# logos_folder = "logos"
# output_csv = "results.csv"

# # Load all logos as grayscale templates
# templates = load_templates(logos_folder)

# # Get video frame data: [url, first_frame, middle_frame, last_frame]
# video_data = get_frames()

# def process_video(video_info):
#     url, first_frame, middle_frame, last_frame = video_info
#     print(f"\nProcessing video: {url}")
    
#     frames_dict = {"First": first_frame, "Middle": middle_frame, "Last": last_frame}
#     detections_all = []
#     best_logos = []

#     for label, frame in frames_dict.items():
#         if frame is None:
#             print(f"⚠️ {label} frame missing for {url}. Skipping...")
#             detections_all.append((label, None))
#             best_logos.append(None)
#             continue
        
#         detections = detect_logos(frame, templates)

#         if detections:
#             best_detection = max(detections, key=lambda x: x[2])  # highest accuracy
#             detections_all.append((label, best_detection))
#             best_logos.append(best_detection[0])  # just the logo name
#             print(f"✅ {label} Frame - Best Logo: {best_detection}")
#         else:
#             print(f"❌ {label} Frame - No logos detected.")
#             detections_all.append((label, None))
#             best_logos.append(None)

#     # Check if all 3 logos are non-None and the same
#     logo_detected = (
#         all(l is not None for l in best_logos)
#         and best_logos.count(best_logos[0]) == 3
#     )

#     return [url, logo_detected, detections_all]

# results = []
# for video_info in video_data:
#     result = process_video(video_info)
#     results.append(result)

# # Save to CSV
# with open(output_csv, "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["Video URL", "Logo Detected", "Detection Details"])
#     for r in results:
#         writer.writerow([r[0], r[1], str(r[2])])

#     print("\n✅ Detection complete. Results saved to:", output_csv)

from detect_logo import detect_logos, load_templates
from extractImageWithYTDLP import get_frames
import csv

logos_folder = "logos"
output_csv = "results.csv"

templates = load_templates(logos_folder)
video_data = get_frames()

def get_top_logos(detections, top_n=2):
    return [d[0] for d in sorted(detections, key=lambda x: -x[2])[:top_n]]

def process_video(video_info):
    url, first_frame, middle_frame, last_frame = video_info
    print(f"\nProcessing video: {url}")
    
    frames_dict = {"First": first_frame, "Middle": middle_frame, "Last": last_frame}
    detections_all = []
    top_logos_all = []

    for label, frame in frames_dict.items():
        if frame is None:
            print(f"⚠️ {label} frame missing for {url}. Skipping...")
            detections_all.append((label, None))
            top_logos_all.append(set())
            continue

        detections = detect_logos(frame, templates)

        if detections:
            top_logos = get_top_logos(detections)
            detections_all.append((label, detections[0]))  # store best
            top_logos_all.append(set(top_logos))
            print(f"✅ {label} Frame - Top Logos: {top_logos}")
        else:
            print(f"❌ {label} Frame - No logos detected.")
            detections_all.append((label, None))
            top_logos_all.append(set())

    # Check if any logo appears in all 3 sets
    common_logos = set.intersection(*top_logos_all)
    logo_detected = len(common_logos) > 0

    return [url, logo_detected, detections_all]

# Process all videos
results = []
for video_info in video_data:
    result = process_video(video_info)
    results.append(result)

# Save results
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Video URL", "Logo Detected", "Detection Details"])
    for r in results:
        writer.writerow([r[0], r[1], str(r[2])])

print("\n✅ Detection complete. Results saved to:", output_csv)
