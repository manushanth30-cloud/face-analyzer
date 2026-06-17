import numpy as np
from scipy.spatial.distance import euclidean


def analyze_nose(landmarks, img_w, img_h):
    """
    Analyze nose proportions from a frontal-facing photo.
    NOTE: Profile classifications (Straight/Concave/Convex) require a side view
    and are intentionally omitted. We measure width, tip, bridge, and nostril metrics.
    """

    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * img_w, p.y * img_h])

    tip       = lm(4)
    bridge_t  = lm(6)
    bridge_b  = lm(197)
    nostril_l = lm(129)
    nostril_r = lm(358)
    base_c    = lm(2)
    base_l    = lm(97)
    base_r    = lm(326)

    face_width  = euclidean(lm(234), lm(454))
    face_height = euclidean(lm(10), lm(152))

    # --- Width to Face Ratio ---
    nose_width  = euclidean(nostril_l, nostril_r)
    width_ratio = nose_width / face_width if face_width > 0 else 0
    if width_ratio < 0.22:
        width_cat = "Narrow"
    elif width_ratio < 0.32:
        width_cat = "Proportionate"
    else:
        width_cat = "Wide"

    # --- Tip Shape (tip width vs bridge width) ---
    tip_width    = euclidean(base_l, base_r)
    bridge_width = euclidean(bridge_t, bridge_b)  # vertical span of bridge
    # Use lateral tip width
    tip_ratio = tip_width / nose_width if nose_width > 0 else 0
    if tip_ratio < 0.75:
        tip_shape = "Refined"
    elif tip_ratio < 0.9:
        tip_shape = "Medium"
    else:
        tip_shape = "Broad"

    # --- Bridge Width ---
    # Compare bridge width (horizontal) at landmark 6 vs 197
    bridge_h_width = abs(bridge_t[0] - bridge_b[0])
    bridge_ratio   = bridge_h_width / nose_width if nose_width > 0 else 0
    if bridge_ratio < 0.35:
        bridge_cat = "Narrow"
    elif bridge_ratio < 0.65:
        bridge_cat = "Medium"
    else:
        bridge_cat = "Wide"

    # --- Bridge Alignment (left/right deviation from center) ---
    center_x = (lm(234)[0] + lm(454)[0]) / 2
    tip_dev  = (tip[0] - center_x) / face_width if face_width > 0 else 0
    if abs(tip_dev) < 0.02:
        bridge_alignment = "Centered"
    elif tip_dev < 0:
        bridge_alignment = "Slight left deviation"
    else:
        bridge_alignment = "Slight right deviation"

    # --- Nostril Flare ---
    nostril_width_ratio = nose_width / face_width if face_width > 0 else 0
    if nostril_width_ratio < 0.22:
        nostril_flare = "Minimal"
    elif nostril_width_ratio < 0.30:
        nostril_flare = "Moderate"
    else:
        nostril_flare = "Wide"

    # --- Nostril Symmetry ---
    nose_cx = (nostril_l[0] + nostril_r[0]) / 2
    l_dev   = abs(nostril_l[0] - nose_cx)
    r_dev   = abs(nostril_r[0] - nose_cx)
    dev_ratio = abs(l_dev - r_dev) / ((l_dev + r_dev) / 2) if (l_dev + r_dev) > 0 else 0
    nostril_symmetry = max(0, min(100, int((1 - dev_ratio) * 100)))

    # --- Nose Length ---
    nose_length = euclidean(bridge_t, base_c)
    length_ratio = nose_length / face_height if face_height > 0 else 0
    if length_ratio < 0.28:
        nose_length_cat = "Short"
    elif length_ratio < 0.38:
        nose_length_cat = "Medium"
    else:
        nose_length_cat = "Long"

    confidence = min(92, 76 + nostril_symmetry // 10)

    return {
        "widthRatio":       width_cat,
        "tipShape":         tip_shape,
        "bridgeWidth":      bridge_cat,
        "bridgeAlignment":  bridge_alignment,
        "nostrilFlare":     nostril_flare,
        "nostrilSymmetry":  nostril_symmetry,
        "length":           nose_length_cat,
        "confidence":       confidence,
        # Internal
        "_noseWidth":       round(float(nose_width), 2),
        "_noseLength":      round(float(nose_length), 2),
    }
