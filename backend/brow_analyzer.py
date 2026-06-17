import numpy as np
from scipy.spatial.distance import euclidean


def analyze_brows(landmarks, img_w, img_h):
    """Analyze eyebrow shape, arch, thickness, height, and symmetry."""

    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * img_w, p.y * img_h])

    # Left brow: inner→peak→outer
    lb = [lm(70), lm(63), lm(105), lm(66), lm(107)]
    # Right brow: inner→peak→outer
    rb = [lm(300), lm(293), lm(334), lm(296), lm(336)]

    # --- Brow Shape ---
    def brow_shape(pts):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        # Fit quadratic; curvature determines shape
        coeffs    = np.polyfit(xs, ys, 2)
        curvature = abs(coeffs[0]) * (max(xs) - min(xs)) ** 2

        # Find arch peak relative position
        peak_idx = int(np.argmin(ys))  # lowest y = highest on image
        rel_pos  = peak_idx / (len(pts) - 1)

        if curvature < 5:
            return "Straight", rel_pos
        elif curvature < 12:
            return "Curved", rel_pos
        else:
            return "Arched", rel_pos

    l_shape, l_peak = brow_shape(lb)
    r_shape, r_peak = brow_shape(rb)
    shape           = l_shape  # use dominant

    # Arch peak position
    avg_peak = (l_peak + r_peak) / 2
    if avg_peak < 0.33:
        arch_peak = "Inner third"
    elif avg_peak < 0.66:
        arch_peak = "Center"
    else:
        arch_peak = "Outer third"

    # --- Brow Thickness (vertical span) ---
    def brow_thickness(pts):
        # Use related eye vs brow landmark vertical gap
        return max(p[1] for p in pts) - min(p[1] for p in pts)

    l_thick = brow_thickness(lb)
    r_thick = brow_thickness(rb)
    avg_thick = (l_thick + r_thick) / 2

    face_h = euclidean(lm(10), lm(152))
    thick_ratio = avg_thick / face_h if face_h > 0 else 0

    if thick_ratio < 0.018:
        thickness = "Thin"
    elif thick_ratio < 0.035:
        thickness = "Medium"
    else:
        thickness = "Thick"

    # --- Brow Height (distance from eye to brow) ---
    brow_center_y  = float(np.mean([p[1] for p in lb + rb]))
    eye_top_y      = float((lm(159)[1] + lm(386)[1]) / 2)
    brow_eye_gap   = eye_top_y - brow_center_y
    ideal_gap      = face_h * 0.055

    if brow_eye_gap < ideal_gap * 0.75:
        brow_height = "Low"
    elif brow_eye_gap > ideal_gap * 1.25:
        brow_height = "High"
    else:
        brow_height = "Ideal"

    # --- Inter-brow Distance ---
    l_inner = lb[0]   # innermost left brow point
    r_inner = rb[0]   # innermost right brow point
    inter_brow = euclidean(l_inner, r_inner)
    eye_width  = euclidean(lm(33), lm(133))

    if inter_brow < eye_width * 0.8:
        inter_brow_dist = "Narrow"
    elif inter_brow > eye_width * 1.4:
        inter_brow_dist = "Wide"
    else:
        inter_brow_dist = "Ideal"

    # --- Brow Symmetry ---
    l_width = euclidean(lb[0], lb[-1])
    r_width = euclidean(rb[0], rb[-1])
    w_diff  = abs(l_width - r_width) / ((l_width + r_width) / 2) if (l_width + r_width) > 0 else 0
    h_diff  = abs(brow_thickness(lb) - brow_thickness(rb)) / max(brow_thickness(lb), brow_thickness(rb) or 1)
    brow_symmetry = max(0, min(100, int((1 - (w_diff + h_diff) / 2) * 100)))

    confidence = min(93, 74 + brow_symmetry // 8)

    return {
        "shape":             shape,
        "thickness":         thickness,
        "archPeakPosition":  arch_peak,
        "height":            brow_height,
        "interBrowDistance": inter_brow_dist,
        "symmetryScore":     brow_symmetry,
        "confidence":        confidence,
    }
