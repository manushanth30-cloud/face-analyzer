"""
embed_matcher.py
================
Runtime celebrity lookalike matching using pre-built InsightFace embeddings.

At server startup:  load_embed_db() loads celeb_embeddings.pkl into RAM.
Per request:        find_celeb_matches(img_bgr, top_n) returns top-N matches.

Falls back gracefully to proportion-based matching (from celebrity_matcher.py)
for celebrities whose Wikipedia photo had no detectable face.
"""

import os
import pickle
import logging
import numpy as np

log = logging.getLogger(__name__)

# ── Singleton state ────────────────────────────────────────────────────────────
_db             = None   # loaded payload from celeb_embeddings.pkl
_faiss_index    = None   # reconstructed FAISS index
_insight_app    = None   # InsightFace FaceAnalysis instance
_embed_ready    = False  # True once everything is loaded

DB_PATH = os.path.join(os.path.dirname(__file__), "celeb_embeddings.pkl")


# ── Startup loader ─────────────────────────────────────────────────────────────
def load_embed_db():
    """Load the pre-built embedding database. Call once at server startup."""
    global _db, _faiss_index, _insight_app, _embed_ready

    if not os.path.exists(DB_PATH):
        log.warning("celeb_embeddings.pkl not found — embedding-based matching disabled.")
        return False

    try:
        import faiss
        from insightface.app import FaceAnalysis

        log.info("Loading celeb_embeddings.pkl …")
        with open(DB_PATH, "rb") as f:
            _db = pickle.load(f)

        if _db.get("faiss_index") is not None:
            _faiss_index = faiss.deserialize_index(_db["faiss_index"])
            log.info("FAISS index loaded: %d vectors", _faiss_index.ntotal)

        log.info("Loading InsightFace buffalo_sc …")
        _insight_app = FaceAnalysis(
            name="buffalo_sc",
            providers=["CPUExecutionProvider"],
        )
        _insight_app.prepare(ctx_id=-1, det_size=(320, 320))

        _embed_ready = True
        log.info("Embedding-based matching ready ✓")
        return True

    except Exception as exc:
        log.error("Failed to load embedding DB: %s — using fallback.", exc)
        _embed_ready = False
        return False


# ── Per-request helpers ────────────────────────────────────────────────────────
def _get_user_embedding(img_bgr: np.ndarray):
    """Extract InsightFace embedding from user's photo. Returns (512,) float32 or None."""
    try:
        faces = _insight_app.get(img_bgr)
        if not faces:
            return None
        best = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
        emb  = best.normed_embedding.astype(np.float32)
        return emb
    except Exception as exc:
        log.warning("Embedding extraction failed: %s", exc)
        return None


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity for L2-normalised vectors (= dot product)."""
    return float(np.dot(a, b))


def _describe_match(sim: float) -> str:
    if sim >= 0.60:  return "Striking Match"
    if sim >= 0.50:  return "Strong Match"
    if sim >= 0.40:  return "Good Match"
    if sim >= 0.30:  return "Similar Features"
    return "Partial Match"


def _sim_to_pct(sim: float, rank: int) -> float:
    """Map cosine similarity (0–1) to a human-readable percentage."""
    # InsightFace normed embeddings: same-person ~0.7-0.9, lookalike ~0.3-0.5
    pct = round(30 + sim * 80, 1)
    pct = min(92.0, max(38.0, pct))
    return pct


def _build_similarities(user_emb, celeb):
    """Return 2-3 textual similarity reasons (placeholder — could be feature-level)."""
    reasons = []
    shape = celeb.get("face_shape", "")
    if shape:
        reasons.append(f"Similar {shape.lower()} face shape")
    reasons.append("Matching facial proportions")
    if len(reasons) < 3:
        reasons.append("Similar bone structure")
    return reasons[:3]


# ── Public API ─────────────────────────────────────────────────────────────────
def find_celeb_matches(img_bgr: np.ndarray, top_n: int = 5):
    """
    Main entry point called from main.py.

    Parameters
    ----------
    img_bgr : np.ndarray   OpenCV BGR image of the user's face
    top_n   : int          Number of results to return

    Returns
    -------
    list[dict]  same schema as celebrity_matcher.find_celebrity_matches()
    """
    if not _embed_ready:
        return None  # signal to caller to use proportion fallback

    user_emb = _get_user_embedding(img_bgr)
    if user_emb is None:
        log.info("No face embedding extracted — using proportion fallback.")
        return None

    celebrities = _db.get("celebrities", [])
    if not celebrities:
        return None

    # ── FAISS search (fast) ───────────────────────────────────────────────────
    if _faiss_index is not None and _faiss_index.ntotal > 0:
        import faiss
        q = user_emb.reshape(1, -1).copy()
        faiss.normalize_L2(q)
        sims, idxs = _faiss_index.search(q, min(top_n, _faiss_index.ntotal))
        sims = sims[0]
        idxs = idxs[0]
        top_celebs = [(float(sims[i]), celebrities[idxs[i]]) for i in range(len(idxs)) if idxs[i] >= 0]
    else:
        # ── Brute-force fallback ──────────────────────────────────────────────
        scored = []
        for celeb in celebrities:
            sim = _cosine_sim(user_emb, celeb["embedding"])
            scored.append((sim, celeb))
        scored.sort(key=lambda x: x[0], reverse=True)
        top_celebs = scored[:top_n]

    # ── Format output ─────────────────────────────────────────────────────────
    matches = []
    for rank, (sim, celeb) in enumerate(top_celebs):
        pct = _sim_to_pct(sim, rank)
        if rank > 0 and matches:
            pct = min(pct, matches[0]["matchPercent"] - rank * 4.5)
            pct = max(34.0, round(pct, 1))

        matches.append({
            "name":         celeb["name"],
            "matchPercent": pct,
            "category":     celeb.get("category", "Celebrity"),
            "faceShape":    celeb.get("face_shape", ""),
            "funFact":      celeb.get("fun_fact", ""),
            "similarities": _build_similarities(user_emb, celeb),
            "matchLabel":   _describe_match(sim),
        })

    return matches
