import numpy as np
import cv2
from scipy.spatial.distance import euclidean


def analyze_skin(image_bgr, landmarks, img_w, img_h):
    """
    Analyze skin tone, undertone, evenness, dark circles, and redness.
    Uses LAB colorspace for tone classification and ITA° for undertone.
    """

    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * img_w, p.y * img_h])

    image_lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    def sample_region(center, radius=12):
        """Sample pixels in a circular region."""
        cx, cy = int(center[0]), int(center[1])
        r = int(radius)
        h, w = image_lab.shape[:2]
        pixels = []
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    px, py = cx + dx, cy + dy
                    if 0 <= px < w and 0 <= py < h:
                        pixels.append(image_lab[py, px])
        return np.array(pixels) if pixels else np.zeros((1, 3))

    # Sample cheeks and forehead
    cheek_l_pts  = sample_region(lm(116), 14)
    cheek_r_pts  = sample_region(lm(345), 14)
    forehead_pts = sample_region(lm(151), 14)
    under_l_pts  = sample_region(lm(110), 10)
    under_r_pts  = sample_region(lm(339), 10)

    all_skin = np.vstack([cheek_l_pts, cheek_r_pts, forehead_pts])
    avg_lab  = all_skin.mean(axis=0)   # [L, A, B]

    L_val = float(avg_lab[0])
    A_val = float(avg_lab[1]) - 128    # signed
    B_val = float(avg_lab[2]) - 128    # signed

    # --- Fitzpatrick Scale (based on LAB L*) ---
    L_norm = L_val  # 0-255 range in OpenCV
    if L_norm > 200:
        fitzpatrick = "I"
    elif L_norm > 175:
        fitzpatrick = "II"
    elif L_norm > 145:
        fitzpatrick = "III"
    elif L_norm > 115:
        fitzpatrick = "IV"
    elif L_norm > 85:
        fitzpatrick = "V"
    else:
        fitzpatrick = "VI"

    # --- Skin Tone Label ---
    tone_map = {"I": "Very Light", "II": "Light", "III": "Medium",
                "IV": "Tan", "V": "Deep Brown", "VI": "Deep"}
    skin_tone = tone_map[fitzpatrick]

    # --- Undertone via ITA° (Individual Typology Angle) ---
    # ITA° = arctan((L* - 50) / b*) × (180 / π)
    # ITA° > 28 = Very Light; 10-28 = Light; -10-10 = Neutral; < -30 = Dark
    # Warm = positive b* dominant; Cool = negative b* dominant
    b_star = B_val  # positive = warm (yellow), negative = cool (blue)
    a_star = A_val  # positive = red, negative = green

    if b_star > 5:
        undertone = "Warm"
    elif b_star < -5:
        undertone = "Cool"
    else:
        if a_star > 3:
            undertone = "Warm"  # pinkish = warm tendency
        else:
            undertone = "Neutral"

    # --- Evenness Score (pixel variance in cheek zones) ---
    cheek_combined = np.vstack([cheek_l_pts, cheek_r_pts])
    variance = float(np.var(cheek_combined[:, 0]))  # L channel variance
    evenness_score = max(0, min(100, int(100 - variance / 3)))

    # --- Dark Circles ---
    under_all = np.vstack([under_l_pts, under_r_pts])
    under_L   = float(under_all[:, 0].mean())
    cheek_L   = float(np.vstack([cheek_l_pts, cheek_r_pts])[:, 0].mean())
    dark_diff = cheek_L - under_L  # positive = under-eye is darker

    if dark_diff < 5:
        dark_circles = "None"
    elif dark_diff < 12:
        dark_circles = "Mild"
    elif dark_diff < 22:
        dark_circles = "Moderate"
    else:
        dark_circles = "Prominent"

    # --- Redness Zones (A channel) ---
    avg_A = float(all_skin[:, 1].mean()) - 128
    if avg_A < 8:
        redness = "None"
    elif avg_A < 15:
        redness = "Mild"
    else:
        redness = "Moderate"

    confidence = min(92, 74 + evenness_score // 8)

    return {
        "fitzpatrick":   fitzpatrick,
        "tone":          skin_tone,
        "undertone":     undertone,
        "evennessScore": evenness_score,
        "darkCircles":   dark_circles,
        "rednessZones":  redness,
        "confidence":    confidence,
    }
