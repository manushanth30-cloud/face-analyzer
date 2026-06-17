import numpy as np
from scipy.spatial.distance import euclidean


def analyze_eyes(landmarks, img_w, img_h):
    """Analyze eye shape, canthal tilt, spacing, size, and lid visibility."""

    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * img_w, p.y * img_h])

    # Left eye landmarks
    l_outer  = lm(33)
    l_inner  = lm(133)
    l_top    = lm(159)
    l_bot    = lm(145)
    l_top2   = lm(160)
    l_bot2   = lm(144)

    # Right eye landmarks
    r_outer  = lm(263)
    r_inner  = lm(362)
    r_top    = lm(386)
    r_bot    = lm(374)
    r_top2   = lm(387)
    r_bot2   = lm(373)

    # --- Eye dimensions ---
    l_width  = euclidean(l_outer, l_inner)
    r_width  = euclidean(r_outer, r_inner)
    l_height = euclidean(l_top, l_bot)
    r_height = euclidean(r_top, r_bot)

    avg_width  = (l_width + r_width) / 2
    avg_height = (l_height + r_height) / 2

    # --- Canthal Tilt ---
    # Angle of line from inner to outer corner (positive = upturned)
    def tilt_angle(inner, outer):
        dx = outer[0] - inner[0]
        dy = outer[1] - inner[1]
        angle = np.degrees(np.arctan2(-dy, abs(dx)))
        return round(float(angle), 1)

    left_tilt  = tilt_angle(l_inner, l_outer)
    right_tilt = tilt_angle(r_inner, r_outer)
    canthal_tilt = round((left_tilt + right_tilt) / 2, 1)
    canthal_str  = f"+{canthal_tilt}°" if canthal_tilt >= 0 else f"{canthal_tilt}°"

    # --- Eye Shape ---
    hw_ratio = avg_height / avg_width if avg_width > 0 else 0

    def classify_shape():
        if hw_ratio > 0.38:
            if canthal_tilt > 3:
                return "Almond"
            return "Round"
        elif hw_ratio > 0.28:
            if canthal_tilt < -2:
                return "Downturned"
            elif canthal_tilt > 4:
                return "Upturned"
            return "Almond"
        else:
            # Check for monolid / hooded using lid visibility approximation
            l_lid = lm(161)[1] - l_top[1]
            if l_lid < 2:
                return "Monolid"
            if l_lid < 4:
                return "Hooded"
            return "Downturned"

    eye_shape = classify_shape()

    # --- Eye Spacing ---
    face_width  = euclidean(lm(234), lm(454))
    inter_eye   = euclidean(l_inner, r_inner)
    fifth_ideal = face_width / 5

    if inter_eye > fifth_ideal * 1.2:
        spacing = "Wide-set"
    elif inter_eye < fifth_ideal * 0.8:
        spacing = "Close-set"
    else:
        spacing = "Ideal"

    # --- Eye Size Ratio relative to face ---
    eye_to_face = avg_width / face_width if face_width > 0 else 0
    if eye_to_face > 0.175:
        size_ratio = "Large"
    elif eye_to_face > 0.13:
        size_ratio = "Medium"
    else:
        size_ratio = "Small"

    # --- Lid Visibility (approximate using landmark vertical gap) ---
    l_lid_gap = abs(lm(161)[1] - l_top[1])
    if l_lid_gap < 2.5:
        lid_visibility = "Hooded"
    elif l_lid_gap < 5:
        lid_visibility = "Partially hooded"
    else:
        lid_visibility = "Visible"

    # --- Asymmetry Score ---
    width_diff  = abs(l_width - r_width) / ((l_width + r_width) / 2) if (l_width + r_width) > 0 else 0
    height_diff = abs(l_height - r_height) / ((l_height + r_height) / 2) if (l_height + r_height) > 0 else 0
    avg_diff    = (width_diff + height_diff) / 2
    asymmetry_score = max(0, min(100, int((1 - avg_diff) * 100)))

    confidence = min(94, 78 + int(asymmetry_score / 10))

    return {
        "shape":          eye_shape,
        "canthalTilt":    canthal_str,
        "spacing":        spacing,
        "sizeRatio":      size_ratio,
        "lidVisibility":  lid_visibility,
        "asymmetryScore": asymmetry_score,
        "confidence":     confidence,
        # Internal
        "_eyeWidth":      round(avg_width, 2),
        "_interEyeDist":  round(float(inter_eye), 2),
    }
