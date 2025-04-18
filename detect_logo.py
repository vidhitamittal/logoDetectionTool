import cv2 as cv
import numpy as np
import os

def load_templates(logos_folder):
    templates = {}
    for filename in os.listdir(logos_folder):
        if filename.endswith(('.jpeg', '.png', '.jpg')):
            name = filename.split('.')[0]
            img = cv.imread(os.path.join(logos_folder, filename), cv.IMREAD_GRAYSCALE)
            templates[name] = img
    return templates


def detect_logos(frame, templates):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
    detected = []

    for logo_name, template in templates.items():
        # Normal Template Matching
        # Resize template if larger than frame
        if template is None:
            continue
        if template.shape[0] > gray.shape[0] or template.shape[1] > gray.shape[1]:
            scale_factor = min(gray.shape[0] / template.shape[0],
                            gray.shape[1] / template.shape[1])
            resized_template = cv.resize(template, (0, 0), fx=scale_factor, fy=scale_factor)
        else:
            resized_template = template

        res = cv.matchTemplate(gray, resized_template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)
        if max_val * 100 >= 70:
            detected.append((logo_name, "Template", max_val * 100))

        # Multi-Scale
        best = 0
        edges = cv.Canny(gray, 50, 200)
        temp_edges = cv.Canny(template, 50, 200)
        for scale in np.linspace(0.5, 2.0, 10):
            try:
                resized = cv.resize(temp_edges, None, fx=scale, fy=scale)
            except Exception:
                continue
            if resized.shape[0] > edges.shape[0] or resized.shape[1] > edges.shape[1]:
                continue
            if template.shape[0] > gray.shape[0] or template.shape[1] > gray.shape[1]:
                scale_factor = min(gray.shape[0] / template.shape[0],
                                gray.shape[1] / template.shape[1])
                resized_template = cv.resize(template, (0, 0), fx=scale_factor, fy=scale_factor)
            else:
                resized_template = template

            res = cv.matchTemplate(gray, resized_template, cv.TM_CCOEFF_NORMED)
            _, val, _, _ = cv.minMaxLoc(res)
            best = max(best, val)
        if best * 100 >= 70:
            detected.append((logo_name, "Multi-Scale", best * 100))

        # ORB
        orb = cv.ORB_create(1500)
        kp1, des1 = orb.detectAndCompute(template, None)
        kp2, des2 = orb.detectAndCompute(gray, None)
        if des1 is not None and des2 is not None:
            bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            if matches:
                score = len(matches) / len(kp1) * 100
                if score >= 20:
                    detected.append((logo_name, "ORB", score))

    return detected
