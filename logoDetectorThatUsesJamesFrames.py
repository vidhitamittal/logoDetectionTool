import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from extractImageWithYTDLP import get_frames

# Load the template in grayscale.
template = cv.imread('likeeLogo1.jpeg', cv.IMREAD_GRAYSCALE)
assert template is not None, "Template image could not be read, check file path!"
template_original = template.copy()

# Define detection thresholds (adjustable)
template_matching_threshold = 80.0  # For the six-method template matching
multi_scale_threshold = 70.0          # For multi-scale template matching with edge detection
orb_threshold = 20.0                  # For ORB feature matching

# Get all video frames (each element: [video_url, first_frame, middle_frame, last_frame])
video_frames = get_frames()

# This list will hold the final results as [video_url, logo_detected (True/False)]
results = []

for video_info in video_frames:
    url, first_frame, middle_frame, last_frame = video_info
    print(f'\n\nProcessing video: {url}')
    
    video_detected = False  # Flag to mark if any frame in this video detects a logo
    # Create a dictionary to label the three frames.
    frames_dict = {'First': first_frame, 'Middle': middle_frame, 'Last': last_frame}

    for frame_label, frame in frames_dict.items():
        # Check if the frame was correctly captured.
        if frame is None:
            print(f"⚠️ {frame_label} frame is invalid for video: {url}. Skipping...")
            continue
        
        # Convert the frame to grayscale if necessary.
        if len(frame.shape) == 3:
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        else:
            gray_frame = frame

        # Make a backup copy of the frame for drawing purposes.
        img_original = gray_frame.copy()

        # ======================= Template Matching with 6 Methods =======================
        print(f"🔍 Processing {frame_label} frame with Template Matching (6 methods)...")
        max_template_accuracy = 0  # We'll record the highest accuracy among the 6 methods.
        methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
                   'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']
        for meth in methods:
            method_func = getattr(cv, meth)
            img = img_original.copy()

            # Ensure the template fits inside the frame.
            current_template = template_original.copy()
            if current_template.shape[0] > img.shape[0] or current_template.shape[1] > img.shape[1]:
                scale_factor = min(img.shape[0] / current_template.shape[0],
                                   img.shape[1] / current_template.shape[1])
                current_template = cv.resize(current_template, (0, 0), fx=scale_factor, fy=scale_factor)
            t_w, t_h = current_template.shape[::-1]

            res = cv.matchTemplate(img, current_template, method_func)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if method_func in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left = min_loc
                match_score = 1 - min_val  # Lower is better, so we invert the score.
            else:
                top_left = max_loc
                match_score = max_val      # Higher is better.

            accuracy = match_score * 100
            if accuracy > max_template_accuracy:
                max_template_accuracy = accuracy

            bottom_right = (top_left[0] + t_w, top_left[1] + t_h)
            cv.rectangle(img, top_left, bottom_right, 255, 2)

            plt.figure(figsize=(10, 5))
            plt.subplot(121)
            plt.imshow(cv.normalize(res, None, 0, 255, cv.NORM_MINMAX), cmap='gray')
            plt.title(f'TM Result\n(Method: {meth}\nAcc: {accuracy:.2f}%)')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122)
            plt.imshow(img, cmap='gray')
            plt.title('Detected Region')
            plt.xticks([]), plt.yticks([])
            plt.suptitle(f'{url} | {frame_label} Frame | Template Matching')
            plt.show()

        print(f"{frame_label} frame - Highest Template Matching Accuracy: {max_template_accuracy:.2f}%")

        # =================== Multi-Scale Template Matching with Edge Detection ===================
        print(f"🔍 Processing {frame_label} frame with Multi-Scale Template Matching...")
        img = img_original.copy()
        img_edges = cv.Canny(img, 50, 200)
        template_edges = cv.Canny(template_original, 50, 200)
        best_match = None
        best_top_left = None
        best_t_w, best_t_h = None, None
        best_res = None

        for scale in np.linspace(0.5, 2.0, 10):
            try:
                resized_template = cv.resize(template_edges, None, fx=scale, fy=scale)
            except Exception:
                continue
            if resized_template.shape[0] > img_edges.shape[0] or resized_template.shape[1] > img_edges.shape[1]:
                continue

            res = cv.matchTemplate(img_edges, resized_template, cv.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv.minMaxLoc(res)
            if best_match is None or max_val > best_match:
                best_match = max_val
                best_top_left = max_loc
                best_t_w, best_t_h = resized_template.shape[::-1]
                best_res = res.copy()

        multi_scale_accuracy = best_match * 100 if best_match is not None else 0
        print(f"{frame_label} frame - Multi-Scale Matching Accuracy: {multi_scale_accuracy:.2f}%")

        if best_top_left:
            bottom_right = (best_top_left[0] + best_t_w, best_top_left[1] + best_t_h)
            cv.rectangle(img, best_top_left, bottom_right, 255, 2)
            plt.figure(figsize=(10, 5))
            plt.subplot(121)
            plt.imshow(cv.normalize(best_res, None, 0, 255, cv.NORM_MINMAX), cmap='gray')
            plt.title(f'Multi-Scale Result\nAcc: {multi_scale_accuracy:.2f}%')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122)
            plt.imshow(img, cmap='gray')
            plt.title('Detected Region')
            plt.xticks([]), plt.yticks([])
            plt.suptitle(f'{url} | {frame_label} Frame | Multi-Scale Matching')
            plt.show()
        else:
            print(f"⚠️ No multi-scale matching region found for {frame_label} frame.")

        # ========================== ORB Feature Matching ==========================
        print(f"🔍 Processing {frame_label} frame with ORB Feature Matching...")
        orb = cv.ORB_create(nfeatures=1500)
        kp_template, des_template = orb.detectAndCompute(template_original, None)
        kp_frame, des_frame = orb.detectAndCompute(img_original, None)
        orb_accuracy = 0.0

        if des_template is not None and des_frame is not None and len(des_template) > 0:
            bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
            matches = bf.knnMatch(des_template, des_frame, k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
            if good_matches:
                distances = [m.distance for m in good_matches]
                adaptive_threshold = np.median(distances) * 1.5
                good_matches = [m for m in good_matches if m.distance < adaptive_threshold]
            total_kp_template = len(kp_template) if kp_template is not None else 1
            orb_accuracy = (len(good_matches) / total_kp_template) * 100

        print(f"{frame_label} frame - ORB Matching Accuracy: {orb_accuracy:.2f}%")

        if des_template is not None and des_frame is not None and len(des_template) > 0:
            img_matches = cv.drawMatches(template_original, kp_template, img_original, kp_frame,
                                         good_matches[:20], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            plt.figure(figsize=(12, 6))
            plt.imshow(img_matches)
            plt.title(f'ORB Feature Matching\n{frame_label} Frame\nAcc: {orb_accuracy:.2f}%')
            plt.axis('off')
            plt.suptitle(f'{url} | {frame_label} Frame | ORB Matching')
            plt.show()

        # ===================== Decision Logic for This Frame =====================
        # If any of the detection methods exceed their thresholds, we flag this frame.
        frame_detected = (max_template_accuracy >= template_matching_threshold or
                          multi_scale_accuracy >= multi_scale_threshold or
                          orb_accuracy >= orb_threshold)
        print(f"{frame_label} frame detection status: {'Logo Detected' if frame_detected else 'No Logo Detected'}")
        if frame_detected:
            video_detected = True
            # Optionally, break out if you only need one positive frame per video.
            # break

    results.append([url, video_detected])
    print(f"Final detection for video {url}: {'Logo Detected' if video_detected else 'No Logo Detected'}")

print("\nFinal Logo Detection Results per Video:")
for video_url, detected in results:
    print(f"Video: {video_url} -> Logo detected: {detected}")
