"""
embed_matcher.py
================
Runtime celebrity lookalike matching using real Wikipedia geometry.

At server startup:  load_embed_db() loads celeb_embeddings.pkl into RAM.
Per request:        find_celeb_matches(img_bgr, top_n) returns top-N matches.
"""

import os
import pickle
import logging
from celebrity_matcher import _weighted_similarity, _describe_similarities

log = logging.getLogger(__name__)

_db = None
_ready = False
DB_PATH = os.path.join(os.path.dirname(__file__), "celeb_embeddings.pkl")


def load_embed_db():
    global _db, _ready
    if not os.path.exists(DB_PATH):
        log.warning("celeb_embeddings.pkl not found — using original hardcoded vectors.")
        return False
    try:
        log.info("Loading celeb_embeddings.pkl …")
        with open(DB_PATH, "rb") as f:
            _db = pickle.load(f)
        _ready = True
        log.info("Wikipedia geometry database ready ✓")
        return True
    except Exception as exc:
        log.error("Failed to load DB: %s", exc)
        return False


def find_celeb_matches(user_vector, top_n=5, gender_filter=None):
    """
    Main entry point called from main.py.
    user_vector is the 20-dim geometry vector computed from MediaPipe.
    """
    if not _ready or not _db:
        return None  # Signal main.py to fallback to hardcoded celebrity_matcher

    celebrities = _db.get("celebrities", []) + _db.get("fallbacks", [])
    if not celebrities:
        return None

    results = []
    for celeb in celebrities:
        if gender_filter and celeb.get("gender") != gender_filter:
            continue
        sim = _weighted_similarity(user_vector, celeb["vector"])
        results.append((sim, celeb))

    results.sort(key=lambda x: x[0], reverse=True)
    top = results[:top_n]

    matches = []
    for rank, (sim, celeb) in enumerate(top):
        pct = round(55 + (sim - 0.88) * 250, 1)
        pct = min(87.0, max(48.0, pct))
        if rank > 0 and matches:
            pct = min(pct, matches[0]["matchPercent"] - rank * 5.5)
            pct = max(42.0, round(pct, 1))

        matches.append({
            "name":         celeb["name"],
            "matchPercent": pct,
            "category":     celeb.get("category", "Celebrity"),
            "faceShape":    celeb.get("faceShape") or celeb.get("face_shape", ""),
            "funFact":      celeb.get("funFact") or celeb.get("fun_fact", ""),
            "similarities": _describe_similarities(user_vector, celeb["vector"]),
        })

    return matches
