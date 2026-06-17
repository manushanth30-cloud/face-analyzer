import numpy as np
from scipy.spatial.distance import euclidean


def analyze_face_structure(landmarks, img_w, img_h):
    """Analyze face shape, symmetry, and proportions using MediaPipe landmarks."""

    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * img_w, p.y * img_h])

    # Key landmark points
    top        = lm(10)
    bottom     = lm(152)
    left       = lm(234)
    right      = lm(454)
    cheek_l    = lm(123)
    cheek_r    = lm(352)
    jaw_l      = lm(172)
    jaw_r      = lm(397)
    forehead_l = lm(103)
    forehead_r = lm(332)

    # Core measurements
    face_height       = euclidean(top, bottom)
    face_width        = euclidean(left, right)
    cheekbone_width   = euclidean(cheek_l, cheek_r)
    jaw_width         = euclidean(jaw_l, jaw_r)
    forehead_width    = euclidean(forehead_l, forehead_r)
    width_to_length   = round(face_width / face_height, 2) if face_height > 0 else 0

    # --- Face Shape ---
    def classify_face_shape():
        ratio             = width_to_length
        jaw_to_cheek      = jaw_width / cheekbone_width if cheekbone_width > 0 else 0
        forehead_to_cheek = forehead_width / cheekbone_width if cheekbone_width > 0 else 0

        if ratio < 0.65:
            return "Oblong"
        elif ratio < 0.75:
            if forehead_to_cheek > 0.9 and jaw_to_cheek < 0.75:
                return "Heart"
            return "Oval"
        elif ratio < 0.85:
            if jaw_to_cheek > 0.85:
                return "Square"
            if cheekbone_width > forehead_width and cheekbone_width > jaw_width:
                return "Diamond"
            return "Oval"
        else:
            return "Round"

    face_shape = classify_face_shape()

    # --- Symmetry Score ---
    center_x = (left[0] + right[0]) / 2
    symmetry_pairs = [
        (lm(33),  lm(263)),   # outer eye corners
        (lm(133), lm(362)),   # inner eye corners
        (lm(61),  lm(291)),   # lip corners
        (lm(172), lm(397)),   # jaw corners
        (cheek_l, cheek_r),   # cheekbones
        (forehead_l, forehead_r),
    ]
    errors = []
    for p1, p2 in symmetry_pairs:
        d1 = abs(p1[0] - center_x)
        d2 = abs(p2[0] - center_x)
        denom = (d1 + d2) / 2
        if denom > 0:
            errors.append(abs(d1 - d2) / denom)

    avg_error      = float(np.mean(errors)) if errors else 0
    symmetry_score = max(0, min(100, int((1 - avg_error) * 100)))

    # --- Facial Thirds ---
    brow_y    = float((lm(107)[1] + lm(336)[1]) / 2)
    nose_y    = float(lm(2)[1])
    top_y     = float(top[1])
    bottom_y  = float(bottom[1])

    t1 = brow_y - top_y
    t2 = nose_y - brow_y
    t3 = bottom_y - nose_y
    ideal = face_height / 3

    ratios = [t1 / ideal, t2 / ideal, t3 / ideal]
    max_r  = max(ratios)
    if max_r == ratios[0] and ratios[0] > 1.15:
        facial_thirds = "Top heavy"
    elif max_r == ratios[2] and ratios[2] > 1.15:
        facial_thirds = "Bottom heavy"
    else:
        facial_thirds = "Balanced"

    # --- Facial Fifths ---
    inter_eye   = euclidean(lm(133), lm(362))
    fifth_ideal = face_width / 5
    if inter_eye > fifth_ideal * 1.2:
        facial_fifths = "Wide-set"
    elif inter_eye < fifth_ideal * 0.8:
        facial_fifths = "Close-set"
    else:
        facial_fifths = "Balanced"

    # --- Cheekbone Prominence ---
    cheek_ratio = cheekbone_width / jaw_width if jaw_width > 0 else 1.0
    if cheek_ratio > 1.15:
        cheekbone_prominence = "High"
    elif cheek_ratio > 1.0:
        cheekbone_prominence = "Medium"
    else:
        cheekbone_prominence = "Low"

    confidence = min(95, 72 + symmetry_score // 6)

    return {
        "shape":               face_shape,
        "symmetryScore":       symmetry_score,
        "facialThirds":        facial_thirds,
        "facialFifths":        facial_fifths,
        "cheekboneProminence": cheekbone_prominence,
        "widthToLengthRatio":  width_to_length,
        "confidence":          confidence,
        # Internal values used by harmony_scores.py
        "_faceWidth":          face_width,
        "_faceHeight":         face_height,
        "_jawWidth":           jaw_width,
        "_cheekboneWidth":     cheekbone_width,
        "_centerX":            float(center_x),
    }
