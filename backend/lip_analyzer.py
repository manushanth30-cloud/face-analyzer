import numpy as np
from scipy.spatial.distance import euclidean


def analyze_lips(landmarks, img_w, img_h):
    """Analyze lip fullness, proportions, cupid's bow, corner angle, and symmetry."""

    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * img_w, p.y * img_h])

    # Upper lip landmarks
    ul_pts = [lm(61), lm(185), lm(40), lm(39), lm(37), lm(0), lm(267), lm(269), lm(270), lm(291)]
    # Lower lip landmarks
    ll_pts = [lm(61), lm(146), lm(91), lm(181), lm(84), lm(17), lm(314), lm(405), lm(321), lm(291)]
    # Corners
    corner_l = lm(61)
    corner_r = lm(291)

    face_width  = euclidean(lm(234), lm(454))
    face_height = euclidean(lm(10), lm(152))

    # --- Lip Fullness ---
    upper_height = min(p[1] for p in ul_pts) - max(p[1] for p in ul_pts)
    upper_height = abs(upper_height)
    # Use midpoints
    upper_top    = min(ul_pts, key=lambda p: p[1])
    upper_bot    = max(ul_pts, key=lambda p: p[1])
    lower_top    = min(ll_pts, key=lambda p: p[1])
    lower_bot    = max(ll_pts, key=lambda p: p[1])

    upper_h = abs(upper_bot[1] - upper_top[1])
    lower_h = abs(lower_bot[1] - lower_top[1])
    total_h = upper_h + lower_h

    lip_to_face = total_h / face_height if face_height > 0 else 0
    if lip_to_face < 0.06:
        fullness = "Thin"
    elif lip_to_face < 0.09:
        fullness = "Medium"
    elif lip_to_face < 0.12:
        fullness = "Full"
    else:
        fullness = "Very full"

    # --- Upper-Lower Ratio (ideal ~1:1.6) ---
    ul_ratio = round(upper_h / lower_h, 2) if lower_h > 0 else 1.0
    ratio_str = f"1:{round(1/ul_ratio, 1)}" if ul_ratio > 0 else "1:1"

    # --- Mouth Width Ratio ---
    mouth_width = euclidean(corner_l, corner_r)
    mw_ratio    = mouth_width / face_width if face_width > 0 else 0
    if mw_ratio < 0.28:
        mouth_width_cat = "Narrow"
    elif mw_ratio < 0.40:
        mouth_width_cat = "Ideal"
    else:
        mouth_width_cat = "Wide"

    # --- Cupid's Bow ---
    # Peaks of upper lip: points near lm(37) and lm(267) relative to center lm(0)
    bow_l   = lm(37)
    bow_r   = lm(267)
    bow_cen = lm(0)
    # Dip of cupid's bow = how much center (philtrum dip) is below the peaks
    bow_dip = float((bow_l[1] + bow_r[1]) / 2) - float(bow_cen[1])
    if bow_dip < 2:
        cupids_bow = "Flat"
    elif bow_dip < 5:
        cupids_bow = "Moderate"
    else:
        cupids_bow = "Defined"

    # --- Corner Angle (up/neutral/down) ---
    mouth_center_y = float((corner_l[1] + corner_r[1]) / 2)
    mid_upper_y    = float(upper_bot[1])
    corner_angle_v = mouth_center_y - mid_upper_y
    if corner_angle_v < -2:
        corner_angle = "Upturned"
    elif corner_angle_v > 3:
        corner_angle = "Downturned"
    else:
        corner_angle = "Neutral"

    # --- Lip Symmetry ---
    center_x = (lm(234)[0] + lm(454)[0]) / 2
    l_off    = abs(corner_l[0] - center_x)
    r_off    = abs(corner_r[0] - center_x)
    sym_err  = abs(l_off - r_off) / ((l_off + r_off) / 2) if (l_off + r_off) > 0 else 0
    lip_symmetry = max(0, min(100, int((1 - sym_err) * 100)))

    confidence = min(93, 76 + lip_symmetry // 8)

    return {
        "fullness":        fullness,
        "upperLowerRatio": ratio_str,
        "mouthWidthRatio": mouth_width_cat,
        "cupidsBow":       cupids_bow,
        "cornerAngle":     corner_angle,
        "symmetryScore":   lip_symmetry,
        "confidence":      confidence,
        # Internal
        "_mouthWidth":     round(float(mouth_width), 2),
    }
