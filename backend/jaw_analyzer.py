import numpy as np
from scipy.spatial.distance import euclidean


def analyze_jaw(landmarks, img_w, img_h):
    """Analyze jawline type, gonial angle, chin shape, and jaw symmetry."""

    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * img_w, p.y * img_h])

    # Jawline points (left to chin to right)
    jaw_pts = [
        lm(172), lm(136), lm(150), lm(149),
        lm(176), lm(148), lm(152),
        lm(377), lm(400), lm(378), lm(379), lm(365), lm(397),
    ]

    chin_pts = [lm(152), lm(148), lm(176), lm(377), lm(400)]
    jaw_l    = lm(172)
    jaw_r    = lm(397)
    chin     = lm(152)

    face_height = euclidean(lm(10), lm(152))
    face_width  = euclidean(lm(234), lm(454))

    # --- Gonial Angle (jaw corner to chin) ---
    # Vector from jaw_l to chin and chin to jaw_r
    v1    = jaw_l - chin
    v2    = jaw_r - chin
    cos_a = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
    cos_a = np.clip(cos_a, -1, 1)
    gonial_angle = round(float(np.degrees(np.arccos(cos_a))), 1)
    gonial_str   = f"{gonial_angle}°"

    # --- Jawline Type ---
    jaw_width = euclidean(jaw_l, jaw_r)

    # Measure curvature of jaw by how much points deviate from straight line
    jaw_xs = np.array([p[0] for p in jaw_pts])
    jaw_ys = np.array([p[1] for p in jaw_pts])
    coeffs = np.polyfit(jaw_xs, jaw_ys, 2)
    curvature = abs(coeffs[0]) * (jaw_xs.max() - jaw_xs.min()) ** 2

    if gonial_angle < 110 and curvature < 30:
        jawline_type = "Sharp"
    elif gonial_angle < 120 and curvature < 60:
        jawline_type = "Defined"
    elif gonial_angle < 130:
        jawline_type = "Soft"
    elif curvature > 80:
        jawline_type = "Rounded"
    else:
        jawline_type = "Undefined"

    # --- Chin Shape ---
    chin_width = euclidean(lm(148), lm(377))
    chin_height = abs(chin[1] - lm(176)[1])
    chin_ratio  = chin_width / chin_height if chin_height > 0 else 1

    if chin_ratio < 1.0:
        chin_shape = "Pointed"
    elif chin_ratio < 1.5:
        chin_shape = "Oval"
    elif chin_ratio < 2.0:
        chin_shape = "Round"
    else:
        chin_shape = "Square"

    # --- Chin Projection ---
    # Compare chin x to line between jaw corners
    chin_x  = float(chin[0])
    center_x = (jaw_l[0] + jaw_r[0]) / 2
    chin_dev = abs(chin_x - center_x) / (face_width / 2) if face_width > 0 else 0
    # Projection = how far forward the chin is (approximated by landmark 17 vs 152)
    chin_forward = lm(17)
    proj = abs(chin_forward[1] - chin[1])
    proj_ratio = proj / face_height if face_height > 0 else 0

    if proj_ratio < 0.02:
        chin_projection = "Recessed"
    elif proj_ratio < 0.05:
        chin_projection = "Normal"
    else:
        chin_projection = "Prominent"

    # --- Chin Width ---
    chin_w_ratio = chin_width / face_width if face_width > 0 else 0
    if chin_w_ratio < 0.2:
        chin_width_cat = "Narrow"
    elif chin_w_ratio < 0.32:
        chin_width_cat = "Medium"
    else:
        chin_width_cat = "Wide"

    # --- Jaw Symmetry ---
    center_x = (lm(234)[0] + lm(454)[0]) / 2
    l_dev    = abs(jaw_l[0] - center_x)
    r_dev    = abs(jaw_r[0] - center_x)
    sym_err  = abs(l_dev - r_dev) / ((l_dev + r_dev) / 2) if (l_dev + r_dev) > 0 else 0
    jaw_symmetry = max(0, min(100, int((1 - sym_err) * 100)))

    confidence = min(91, 72 + jaw_symmetry // 8)

    return {
        "type":           jawline_type,
        "gonialAngle":    gonial_str,
        "chinShape":      chin_shape,
        "chinProjection": chin_projection,
        "chinWidth":      chin_width_cat,
        "symmetryScore":  jaw_symmetry,
        "confidence":     confidence,
    }
