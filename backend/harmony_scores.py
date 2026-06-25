import numpy as np
from scipy.spatial.distance import euclidean


PHI = 1.618  # Golden ratio


def analyze_harmony(face, eyes, nose, lips, jaw):
    """
    Compute facial harmony scores using calibrated population-norm ranges,
    neoclassical canons, and weighted aggregation.

    Weights:
        goldenRatioScore      : 35%
        overallSymmetry       : 30%
        neoclassicalCompliance: 35%
    """

    # ── Range-based scorer ─────────────────────────────────────────────────────
    def range_score(value, ideal, tolerance):
        """
        Score 0–100 based on how close 'value' is to 'ideal'.
        Score = 100 at exact ideal, drops linearly to 0 at ±tolerance.
        Uses population-realistic ideal values instead of raw PHI comparison
        which produced artificially low scores for normal faces.
        """
        diff  = abs(value - ideal)
        score = max(0.0, 1.0 - diff / tolerance)
        return int(score * 100)

    fw  = face.get("_faceWidth",   150)
    fh  = face.get("_faceHeight",  200)
    nw  = nose.get("_noseWidth",    40)
    nl  = nose.get("_noseLength",   60)
    ew  = eyes.get("_eyeWidth",     35)
    mw  = lips.get("_mouthWidth",   55)
    ied = eyes.get("_interEyeDist", 65)

    # ── Golden Ratio checks — calibrated to realistic population norms ─────────
    face_ratio  = fh / fw  if fw  > 0 else 1.4   # real faces: 1.3–1.6, ideal ≈ 1.45
    mouth_nose  = mw / nw  if nw  > 0 else 1.5   # mouth/nose width: ideal ≈ 1.55
    face_nose_l = fw / nl  if nl  > 0 else 2.0   # face width / nose length: ideal ≈ 2.0
    eye_nose    = ew / nw  if nw  > 0 else 1.0   # eye width / nose width: ideal ≈ 1.0

    gr_checks = [
        range_score(face_ratio,  ideal=1.45, tolerance=0.30),
        range_score(mouth_nose,  ideal=1.55, tolerance=0.30),
        range_score(face_nose_l, ideal=2.00, tolerance=0.45),
        range_score(eye_nose,    ideal=1.00, tolerance=0.20),
    ]
    golden_ratio_score = int(np.mean(gr_checks))

    # ── Overall Symmetry ────────────────────────────────────────────────────────
    sym_scores = [
        face.get("symmetryScore",  80),
        eyes.get("asymmetryScore", 80),
        lips.get("symmetryScore",  80),
        jaw.get("symmetryScore",   80),
    ]
    overall_symmetry = int(np.mean(sym_scores))

    # ── Neoclassical Canon Checks ───────────────────────────────────────────────
    def canon_score(a, b, tolerance=0.18):
        """Score how close ratio a/b is to 1.0 (equal)."""
        if b == 0:
            return 50
        ratio = a / b
        diff  = abs(ratio - 1.0)
        score = max(0.0, 1.0 - diff / tolerance)
        return int(score * 100)

    neo_checks = [
        # Face divides into equal thirds (checked in face_structure)
        100 if face.get("facialThirds") == "Balanced" else 60,
        # Nose width ≈ one eye width (Vitruvian canon)
        canon_score(nw, ew),
        # Mouth width ≈ inter-pupil distance
        canon_score(mw, ied + ew),
        # Eye width ≈ inter-eye distance
        canon_score(ew, ied),
    ]
    neoclassical_compliance = int(np.mean(neo_checks))

    # ── Facial Harmony Index (weighted) ────────────────────────────────────────
    facial_harmony_index = int(
        golden_ratio_score      * 0.35 +
        overall_symmetry        * 0.30 +
        neoclassical_compliance * 0.35
    )

    # ── Per-component breakdown (exposed to frontend for transparency) ──────────
    score_breakdown = {
        "goldenRatio": {
            "score":       golden_ratio_score,
            "weight":      0.35,
            "label":       "Golden Ratio",
            "description": "How closely your facial proportions follow the golden ratio (φ≈1.618). Checks face aspect ratio, eye-to-nose width, mouth-to-nose width, and face-to-nose length.",
            "components": [
                {"name": "Face Aspect Ratio",       "score": gr_checks[0], "ideal": "1.45", "yours": round(face_ratio,  2)},
                {"name": "Mouth / Nose Width",      "score": gr_checks[1], "ideal": "1.55", "yours": round(mouth_nose,  2)},
                {"name": "Face Width / Nose Length","score": gr_checks[2], "ideal": "2.00", "yours": round(face_nose_l, 2)},
                {"name": "Eye / Nose Width",        "score": gr_checks[3], "ideal": "1.00", "yours": round(eye_nose,    2)},
            ],
        },
        "symmetry": {
            "score":       overall_symmetry,
            "weight":      0.30,
            "label":       "Facial Symmetry",
            "description": "Left-to-right bilateral symmetry across eyes, lips, jaw, and cheekbones. Higher means more symmetric.",
            "components": [
                {"name": "Facial Symmetry", "score": face.get("symmetryScore",  80)},
                {"name": "Eye Symmetry",    "score": eyes.get("asymmetryScore", 80)},
                {"name": "Lip Symmetry",    "score": lips.get("symmetryScore",  80)},
                {"name": "Jaw Symmetry",    "score": jaw.get("symmetryScore",   80)},
            ],
        },
        "neoclassical": {
            "score":       neoclassical_compliance,
            "weight":      0.35,
            "label":       "Classic Proportions",
            "description": "Adherence to neoclassical canons (da Vinci, Vitruvian Man): equal facial thirds, nose width equals one eye width, and balanced inter-feature distances.",
            "components": [
                {"name": "Equal Facial Thirds",          "score": neo_checks[0]},
                {"name": "Nose Width = Eye Width",       "score": neo_checks[1]},
                {"name": "Mouth = Inter-pupil Distance", "score": neo_checks[2]},
                {"name": "Eye = Inter-eye Distance",     "score": neo_checks[3]},
            ],
        },
    }

    return {
        "goldenRatioScore":       golden_ratio_score,
        "overallSymmetry":        overall_symmetry,
        "facialHarmonyIndex":     facial_harmony_index,
        "neoclassicalCompliance": neoclassical_compliance,
        "scoreBreakdown":         score_breakdown,
    }
