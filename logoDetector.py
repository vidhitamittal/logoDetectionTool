import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Load images
# img = cv.imread('tiktokSS.jpeg', cv.IMREAD_GRAYSCALE)
# img = cv.imread('newTiktokLogo.png', cv.IMREAD_GRAYSCALE)
# img = cv.imread('likee.jpeg', cv.IMREAD_GRAYSCALE)
img = cv.imread('noLogo.png', cv.IMREAD_GRAYSCALE)
template = cv.imread('likeeLogo1.jpeg', cv.IMREAD_GRAYSCALE)
# template = cv.imread('tiktokLogo.jpeg', cv.IMREAD_GRAYSCALE)
# template = cv.imread('tiktokLogo.jpeg', cv.IMREAD_GRAYSCALE)
assert img is not None, "Main image could not be read, check file path!"
assert template is not None, "Template image could not be read, check file path!"

img2 = img.copy()  # Keep original for re-use
w, h = template.shape[::-1]

print("🔍 Starting Template Matching with 6 Methods...")
methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
           'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = getattr(cv, meth)
    
    # Resize template if necessary
    if template.shape[0] > img.shape[0] or template.shape[1] > img.shape[1]:
        scale_factor = min(img.shape[0] / template.shape[0], img.shape[1] / template.shape[1])
        template = cv.resize(template, (0, 0), fx=scale_factor, fy=scale_factor)
        w, h = template.shape[::-1]

    res = cv.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
        match_score = 1 - min_val  # lower is better
    else:
        top_left = max_loc
        match_score = max_val      # higher is better

    accuracy = match_score * 100
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img, top_left, bottom_right, 255, 2)

    plt.figure(figsize=(10, 5))
    plt.subplot(121), plt.imshow(cv.normalize(res, None, 0, 255, cv.NORM_MINMAX), cmap='gray')
    plt.title(f'Matching Result (Accuracy: {accuracy:.2f}%)')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(f'Method: {meth}')
    plt.show()

# ================== Multi-Scale Template Matching ==================
print("\n🔍 Starting Multi-Scale Template Matching with Edge Detection...")

img = img2.copy()
img_edges = cv.Canny(img, 50, 200)
template_edges = cv.Canny(template, 50, 200)

best_match = None
best_top_left = None
best_w, best_h = None, None
best_res = None

for scale in np.linspace(0.5, 2.0, 10):
    resized_template = cv.resize(template_edges, None, fx=scale, fy=scale)
    if resized_template.shape[0] > img_edges.shape[0] or resized_template.shape[1] > img_edges.shape[1]:
        continue

    res = cv.matchTemplate(img_edges, resized_template, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(res)

    if best_match is None or max_val > best_match:
        best_match = max_val
        best_top_left = max_loc
        best_w, best_h = resized_template.shape[::-1]
        best_res = res.copy()

multi_scale_accuracy = best_match * 100 if best_match else 0
print(f"✅ Multi-Scale Matching Accuracy: {multi_scale_accuracy:.2f}%")

if best_top_left:
    bottom_right = (best_top_left[0] + best_w, best_top_left[1] + best_h)
    cv.rectangle(img, best_top_left, bottom_right, 255, 2)

    plt.figure(figsize=(10, 5))
    plt.subplot(121), plt.imshow(cv.normalize(best_res, None, 0, 255, cv.NORM_MINMAX), cmap='gray')
    plt.title(f'Matching Result (Accuracy: {multi_scale_accuracy:.2f}%)')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle('Multi-Scale Template Matching')
    plt.show()
else:
    print("⚠️ No matching logo found in multi-scale test.")

# ================== ORB Feature Matching ==================
print("\n🔍 Starting ORB Feature Matching...")

orb = cv.ORB_create(nfeatures=1500)
kp1, des1 = orb.detectAndCompute(template, None)
kp2, des2 = orb.detectAndCompute(img2, None)

if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
    print("⚠️ ORB feature matching failed: No keypoints detected.")
else:
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if good_matches:
        distances = [m.distance for m in good_matches]
        adaptive_threshold = np.median(distances) * 1.5
        good_matches = [m for m in good_matches if m.distance < adaptive_threshold]

    total_keypoints_template = len(kp1) if kp1 else 1
    orb_matching_accuracy = (len(good_matches) / total_keypoints_template) * 100

    print(f"✅ ORB Matching Accuracy: {orb_matching_accuracy:.2f}% ({len(good_matches)} / {total_keypoints_template} good matches)")

    img_matches = cv.drawMatches(template, kp1, img2, kp2, good_matches[:20], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    plt.figure(figsize=(12, 6))
    plt.imshow(img_matches)
    plt.title(f'ORB Feature Matching (Accuracy: {orb_matching_accuracy:.2f}%)')
    plt.axis('off')
    plt.show()