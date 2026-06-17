"""
Rule-based insight generator.
Produces human-readable strengths, areas to improve, and an overall insight paragraph.
"""


def generate_insights(face, eyes, brows, nose, lips, jaw, skin, harmony):
    strengths = []
    areas     = []

    # ── Symmetry ──────────────────────────────────────────────
    sym = face.get("symmetryScore", 0)
    if sym >= 80:
        strengths.append("Good overall facial symmetry")
    elif sym < 65:
        areas.append("Facial asymmetry — consider contouring")

    # ── Eye spacing ───────────────────────────────────────────
    spacing = eyes.get("spacing", "")
    if spacing == "Ideal":
        strengths.append("Well balanced eye spacing")
    elif spacing == "Wide-set":
        areas.append("Wide-set eyes — inner-corner makeup can help")
    elif spacing == "Close-set":
        areas.append("Close-set eyes — outer-emphasis makeup techniques")

    # ── Golden ratio ──────────────────────────────────────────
    gr = harmony.get("goldenRatioScore", 0)
    if gr >= 75:
        strengths.append("Proportions close to the golden ratio")
    elif gr < 55:
        areas.append("Facial proportions deviate from golden ratio")

    # ── Skin ──────────────────────────────────────────────────
    evenness = skin.get("evennessScore", 0)
    dark     = skin.get("darkCircles", "None")
    redness  = skin.get("rednessZones", "None")

    if evenness >= 75:
        strengths.append("Clear skin with good evenness")
    elif evenness < 55:
        areas.append("Skin texture (pores/unevenness)")

    if dark in ("Moderate", "Prominent"):
        areas.append("Under eye brightness")
    elif dark == "None" and evenness >= 70:
        strengths.append("Minimal under-eye shadowing")

    if redness == "Moderate":
        areas.append("Redness zones — tinted moisturizer can help")

    # ── Eyebrows ─────────────────────────────────────────────
    brow_sym = brows.get("symmetryScore", 0)
    if brow_sym < 70:
        areas.append("Eyebrow grooming for better symmetry")
    elif brow_sym >= 85:
        strengths.append("Well-shaped, symmetrical eyebrows")

    # ── Jaw ───────────────────────────────────────────────────
    jaw_type = jaw.get("type", "")
    if jaw_type in ("Sharp", "Defined"):
        strengths.append("Well-defined jawline")
    elif jaw_type in ("Soft", "Undefined"):
        areas.append("Slightly soft jaw definition")

    # ── Neoclassical ─────────────────────────────────────────
    neo = harmony.get("neoclassicalCompliance", 0)
    if neo >= 75:
        strengths.append("Follows classical facial proportion canons")

    # ── Overall Insight Paragraph ─────────────────────────────
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
        f" Focusing on {areas[0].lower()} could further elevate your look."
        if areas else
        " Your features are remarkably well-balanced."
    )

    overall_insight = (
        f"{face_shape} faces are considered well-balanced and versatile. "
        f"You have {tone} facial harmony with {skin_desc.lower()} skin tone.{improve_str}"
    )

    # Limit to top 4 each
    return {
        "keyStrengths":   strengths[:4],
        "areasToImprove": areas[:4],
        "overallInsight": overall_insight,
    }
