"""
Insight Generator — produces actionable, structured insights.
Each area-to-improve is a rich object with severity, causes, tips, and timeline.
"""

# ── Skincare / improvement timelines ──────────────────────────────────────────
AREA_DETAILS = {
    "asymmetry": {
        "area":     "Facial Asymmetry",
        "severity": "Mild",
        "causes":   ["Natural biological variation", "Habitual side-sleeping", "Muscle imbalance"],
        "tips":     [
            "Face yoga exercises to balance muscle tone",
            "Strategic contouring to visually balance features",
            "Sleep on your back when possible",
            "Facial massage along the weaker side",
        ],
        "timeline": "8–12 weeks of consistent exercise",
    },
    "eye_wide": {
        "area":     "Wide-set Eyes",
        "severity": "Low",
        "causes":   ["Natural bone structure", "Genetic feature"],
        "tips":     [
            "Emphasise inner corner with lighter eyeshadow",
            "Apply eyeliner starting from the inner corner",
            "Keep brow tails from extending too far outward",
            "Use a slightly darker contour at the nose bridge",
        ],
        "timeline": "Immediate with makeup technique",
    },
    "eye_close": {
        "area":     "Close-set Eyes",
        "severity": "Low",
        "causes":   ["Natural bone structure", "Genetic feature"],
        "tips":     [
            "Emphasise outer corners with winged liner",
            "Apply blush horizontally toward the temples",
            "Let brow tails extend naturally outward",
            "Avoid heavy inner-corner products",
        ],
        "timeline": "Immediate with makeup technique",
    },
    "golden_ratio": {
        "area":     "Facial Proportions",
        "severity": "Low",
        "causes":   ["Natural variation in bone structure", "Angle or lens distortion in the photo"],
        "tips":     [
            "Strategic hairstyle to reframe face shape",
            "Contouring and highlighting to balance proportions",
            "Facial exercises to improve muscle tone",
            "Retake the analysis with a front-facing neutral photo",
        ],
        "timeline": "Styling changes: immediate. Structural: long-term",
    },
    "skin_texture": {
        "area":     "Skin Texture & Evenness",
        "severity": "Moderate",
        "causes":   ["Sun exposure", "Dehydration", "Diet", "Hormonal fluctuations"],
        "tips":     [
            "Daily SPF 50+ sunscreen",
            "Chemical exfoliant (AHA/BHA) 2–3× per week",
            "Niacinamide serum to reduce pore appearance",
            "Hyaluronic acid for deep hydration",
            "Retinol at night (start slow: 2× per week)",
        ],
        "timeline": "4–8 weeks with consistent routine",
    },
    "dark_circles": {
        "area":     "Under-eye Darkness",
        "severity": "Moderate",
        "causes":   ["Thin skin under the eyes", "Genetics", "Fatigue", "Dehydration", "Iron deficiency"],
        "tips":     [
            "Vitamin C eye cream in the morning",
            "Cold jade roller or spoon for 5 min daily",
            "Caffeine-based eye cream to reduce puffiness",
            "7–9 hours of quality sleep",
            "Stay hydrated (2L+ water daily)",
        ],
        "timeline": "4–8 weeks with consistent care",
    },
    "redness": {
        "area":     "Skin Redness",
        "severity": "Mild",
        "causes":   ["Rosacea", "Sensitivity", "Diet triggers", "Sun exposure"],
        "tips":     [
            "Green-tinted colour-correcting primer",
            "Centella Asiatica (Cica) calming serum",
            "Avoid hot water when washing face",
            "SPF 50+ daily to prevent worsening",
        ],
        "timeline": "2–4 weeks for initial improvement",
    },
    "brow_symmetry": {
        "area":     "Eyebrow Symmetry",
        "severity": "Low",
        "causes":   ["Natural asymmetry", "Uneven grooming habits"],
        "tips":     [
            "Map brows with a spoolie before grooming",
            "Use a brow pencil to fill gaps on the weaker side",
            "Professional brow threading for precise shaping",
            "Brow serum to promote fuller growth",
        ],
        "timeline": "Immediate with makeup; 4–6 weeks for regrowth",
    },
    "jaw_soft": {
        "area":     "Jaw Definition",
        "severity": "Low",
        "causes":   ["Natural bone structure", "Subcutaneous fat distribution", "Age-related changes"],
        "tips":     [
            "Mewing (proper tongue posture) for long-term reshaping",
            "Jawline contouring with makeup",
            "Strategic beard shaping (men)",
            "Facial exercises targeting the masseter muscle",
            "Reduce sodium to decrease water retention",
        ],
        "timeline": "Styling: immediate. Structural: 3–6 months",
    },
}


# ── Photography tips by face structure ────────────────────────────────────────
def _photography_tips(face, eyes, jaw):
    face_shape = face.get("shape", "Oval")
    jaw_type   = jaw.get("type", "Defined")
    sym_score  = face.get("symmetryScore", 80)

    # Best side: slight asymmetry — favour stronger side
    best_side  = "either side equally (very symmetric face)" if sym_score >= 85 else "your slightly stronger (left or right) side — try both and compare"

    angle_tips = {
        "Oval":    "Slightly above eye level (5–10°) angled down — flatters the balanced proportions.",
        "Round":   "Angle the camera 10–15° above eye level to elongate. Tilt chin slightly down.",
        "Square":  "Camera at eye level or slightly above. A 3/4 angle softens the strong jaw.",
        "Heart":   "Camera at eye level or slightly below. A head-on 3/4 angle balances the forehead.",
        "Diamond": "Camera at eye level. A slight downward tilt adds width to the forehead.",
        "Oblong":  "Camera at eye level, straight-on. Avoid shooting from below — it elongates further.",
    }

    return {
        "bestAngle":          angle_tips.get(face_shape, "Camera at or slightly above eye level, 3/4 turn."),
        "bestSide":           best_side,
        "lightingStyle":      "Soft diffused natural light from a 45° angle (Rembrandt lighting). Avoid direct overhead flash.",
        "lensRecommendation": "85–105mm focal length (portrait lens) to minimise facial distortion. Avoid wide-angle lenses below 35mm.",
        "postingTip":         "Slight smile with relaxed eyes (Duchenne smile). Avoid forced expressions — natural is always more harmonious.",
        "backgroundTip":      "Clean, neutral or blurred background (bokeh). Avoid busy patterns that distract from facial features.",
    }


def generate_insights(face, eyes, brows, nose, lips, jaw, skin, harmony):
    strengths = []
    areas     = []

    # ── Symmetry ──────────────────────────────────────────────
    sym = face.get("symmetryScore", 0)
    if sym >= 80:
        strengths.append("Good overall facial symmetry")
    elif sym < 65:
        d = AREA_DETAILS["asymmetry"].copy()
        d["severity"] = "Moderate" if sym < 55 else "Mild"
        areas.append(d)

    # ── Eye spacing ───────────────────────────────────────────
    spacing = eyes.get("spacing", "")
    if spacing == "Ideal":
        strengths.append("Well balanced eye spacing")
    elif spacing == "Wide-set":
        areas.append(AREA_DETAILS["eye_wide"])
    elif spacing == "Close-set":
        areas.append(AREA_DETAILS["eye_close"])

    # ── Golden ratio ──────────────────────────────────────────
    gr = harmony.get("goldenRatioScore", 0)
    if gr >= 75:
        strengths.append("Proportions close to the golden ratio")
    elif gr < 55:
        areas.append(AREA_DETAILS["golden_ratio"])

    # ── Skin ──────────────────────────────────────────────────
    evenness = skin.get("evennessScore", 0)
    dark     = skin.get("darkCircles", "None")
    redness  = skin.get("rednessZones", "None")

    if evenness >= 75:
        strengths.append("Clear skin with good evenness")
    elif evenness < 55:
        areas.append(AREA_DETAILS["skin_texture"])

    if dark in ("Moderate", "Prominent"):
        d = AREA_DETAILS["dark_circles"].copy()
        d["severity"] = "Moderate" if dark == "Moderate" else "High"
        areas.append(d)
    elif dark == "None" and evenness >= 70:
        strengths.append("Minimal under-eye shadowing")

    if redness == "Moderate":
        areas.append(AREA_DETAILS["redness"])

    # ── Eyebrows ──────────────────────────────────────────────
    brow_sym = brows.get("symmetryScore", 0)
    if brow_sym < 70:
        areas.append(AREA_DETAILS["brow_symmetry"])
    elif brow_sym >= 85:
        strengths.append("Well-shaped, symmetrical eyebrows")

    # ── Jaw ───────────────────────────────────────────────────
    jaw_type = jaw.get("type", "")
    if jaw_type in ("Sharp", "Defined"):
        strengths.append("Well-defined jawline")
    elif jaw_type in ("Soft", "Undefined"):
        areas.append(AREA_DETAILS["jaw_soft"])

    # ── Neoclassical ──────────────────────────────────────────
    neo = harmony.get("neoclassicalCompliance", 0)
    if neo >= 75:
        strengths.append("Follows classical facial proportion canons")

    # ── Eye shape ─────────────────────────────────────────────
    eye_shape = eyes.get("shape", "")
    if eye_shape in ("Almond", "Upturned"):
        strengths.append(f"{eye_shape} eye shape — considered highly photogenic")

    # ── Overall insight paragraph ──────────────────────────────
    harmony_idx = harmony.get("facialHarmonyIndex", 70)
    if harmony_idx >= 85:
        tone = "exceptional"
    elif harmony_idx >= 75:
        tone = "strong"
    elif harmony_idx >= 60:
        tone = "solid"
    else:
        tone = "developing"

    face_shape = face.get("shape", "")
    skin_desc  = skin.get("tone", "")

    improve_str = (
        f" Focusing on {areas[0]['area'].lower()} could further elevate your look."
        if areas else
        " Your features are remarkably well-balanced."
    )

    overall_insight = (
        f"{face_shape} faces are considered well-balanced and versatile. "
        f"You have {tone} facial harmony with {skin_desc.lower()} skin tone.{improve_str}"
    )

    # ── Per-feature confidence ────────────────────────────────
    confidence_by_feature = {
        "faceStructure": face.get("confidence", 80),
        "eyes":          eyes.get("confidence", 80),
        "eyebrows":      brows.get("confidence", 80),
        "nose":          nose.get("confidence", 80),
        "lips":          lips.get("confidence", 80),
        "jaw":           jaw.get("confidence", 80),
        "skin":          skin.get("confidence", 80),
    }

    # ── Photography tips ──────────────────────────────────────
    photo_tips = _photography_tips(face, eyes, jaw)

    return {
        "keyStrengths":        strengths[:5],
        "areasToImprove":      areas[:4],
        "overallInsight":      overall_insight,
        "confidenceByFeature": confidence_by_feature,
        "photographyTips":     photo_tips,
    }
