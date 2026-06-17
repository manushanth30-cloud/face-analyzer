import numpy as np
from scipy.spatial.distance import euclidean


PHI = 1.618  # Golden ratio


def analyze_harmony(face, eyes, nose, lips, jaw):
    """
    Compute facial harmony scores using golden ratio, neoclassical canons,
    and weighted aggregation.

    Weights:
        goldenRatioScore      : 35%
        overallSymmetry       : 30%
        neoclassicalCompliance: 35%
    """

    # --- Golden Ratio Score ---
    def phi_score(a, b):
        """Return 0-100 score for how close a/b is to PHI."""
        if b == 0:
            return 50
        ratio = a / b
        # Tolerance: within ±0.15 of phi = 100, outside ±0.5 = 0
        diff  = abs(ratio - PHI)
        score = max(0.0, 1.0 - diff / 0.5)
        return int(score * 100)

    fw  = face.get("_faceWidth", 1)
    fh  = face.get("_faceHeight", 1)
    nw  = nose.get("_noseWidth", 1)
    nl  = nose.get("_noseLength", 1)
    ew  = eyes.get("_eyeWidth", 1)
    mw  = lips.get("_mouthWidth", 1)
    ied = eyes.get("_interEyeDist", 1)

    gr_checks = [
        phi_score(fh, fw),        # face length / face width
        phi_score(mw, nw),        # mouth width / nose width
        phi_score(fw, nl),        # face width / nose length
        phi_score(ew, nw),        # eye width / nose width
    ]
    golden_ratio_score = int(np.mean(gr_checks))

    # --- Overall Symmetry ---
    sym_scores = [
        face.get("symmetryScore", 80),
        eyes.get("asymmetryScore", 80),
        lips.get("symmetryScore", 80),
        jaw.get("symmetryScore", 80),
    ]
    overall_symmetry = int(np.mean(sym_scores))

    # --- Neoclassical Canon Checks ---
    def canon_score(a, b, tolerance=0.15):
        if b == 0:
            return 50
        ratio = a / b
        diff  = abs(ratio - 1.0)
        score = max(0.0, 1.0 - diff / tolerance)
        return int(score * 100)

    neo_checks = [
        # Face divides into equal thirds (checked in face_structure)
        100 if face.get("facialThirds") == "Balanced" else 60,
        # Nose width ≈ one eye width
        canon_score(nw, ew),
        # Mouth width ≈ inter-pupil distance (approx inter-eye + eye widths)
        canon_score(mw, ied + ew),
        # Eye width ≈ inter-eye distance
        canon_score(ew, ied),
    ]
    neoclassical_compliance = int(np.mean(neo_checks))

    # --- Facial Harmony Index (weighted) ---
    facial_harmony_index = int(
        golden_ratio_score      * 0.35 +
        overall_symmetry        * 0.30 +
        neoclassical_compliance * 0.35
    )

    return {
        "goldenRatioScore":       golden_ratio_score,
        "overallSymmetry":        overall_symmetry,
        "facialHarmonyIndex":     facial_harmony_index,
        "neoclassicalCompliance": neoclassical_compliance,
    }
