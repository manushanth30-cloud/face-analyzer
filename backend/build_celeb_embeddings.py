"""
build_celeb_embeddings.py
=========================
Build-time script — runs inside Docker during `docker build`.

Steps:
  1. Read celebrity list from celebrity_matcher.py
  2. Download Wikipedia profile thumbnail for each celebrity
  3. Run InsightFace (buffalo_sc) to extract 512-dim face embedding
  4. Save results to celeb_embeddings.pkl

Celebrities that fail (no Wikipedia photo, no face detected) are kept
in a fallback list — the runtime matcher will use geometric proportion
vectors for them instead.
"""

import os
import io
import sys
import pickle
import urllib.request
import urllib.parse
import json
import time
import logging

import numpy as np
import cv2
from insightface.app import FaceAnalysis

# Import celebrity list from sibling module
sys.path.insert(0, os.path.dirname(__file__))
from celebrity_matcher import CELEBRITIES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "celeb_embeddings.pkl")

# ── InsightFace setup ──────────────────────────────────────────────────────────
def load_insight_app():
    app = FaceAnalysis(
        name="buffalo_sc",
        providers=["CPUExecutionProvider"],
    )
    app.prepare(ctx_id=-1, det_size=(320, 320))
    return app


# ── Wikipedia photo fetcher ────────────────────────────────────────────────────
WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
HEADERS  = {"User-Agent": "FaceAnalyzerApp/1.0 (educational project)"}


def fetch_wiki_thumbnail(name: str, size: int = 400) -> bytes | None:
    """Download the Wikipedia article thumbnail for `name`. Returns raw image bytes or None."""
    slug = urllib.parse.quote(name.replace(" ", "_"))
    url  = WIKI_API.format(slug)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        thumb = data.get("thumbnail") or data.get("originalimage")
        if not thumb:
            return None
        img_url = thumb["source"]
        req2 = urllib.request.Request(img_url, headers=HEADERS)
        with urllib.request.urlopen(req2, timeout=15) as resp2:
            return resp2.read()
    except Exception as exc:
        log.debug("Wiki fetch failed for %s: %s", name, exc)
        return None


def bytes_to_bgr(raw: bytes) -> np.ndarray | None:
    """Convert raw image bytes to OpenCV BGR array."""
    arr = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def get_embedding(app: FaceAnalysis, img_bgr: np.ndarray) -> np.ndarray | None:
    """Run InsightFace and return the largest-face embedding, or None."""
    faces = app.get(img_bgr)
    if not faces:
        return None
    # Pick the face with the largest bounding box
    best = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    emb  = best.normed_embedding  # already L2-normalised, 512-dim
    return emb.astype(np.float32)


# ── Main build routine ─────────────────────────────────────────────────────────
def build():
    log.info("Loading InsightFace buffalo_sc …")
    app = load_insight_app()
    log.info("InsightFace ready.")

    results   = []   # successfully embedded celebrities
    fallbacks = []   # celebrities that will use proportion vectors

    total = len(CELEBRITIES)
    for i, celeb in enumerate(CELEBRITIES):
        name = celeb["name"]
        log.info("[%d/%d] %s", i + 1, total, name)

        raw = fetch_wiki_thumbnail(name)
        if raw is None:
            log.warning("  ✗ No Wikipedia photo — using fallback")
            fallbacks.append(celeb)
            time.sleep(0.3)
            continue

        img = bytes_to_bgr(raw)
        if img is None:
            log.warning("  ✗ Could not decode image — using fallback")
            fallbacks.append(celeb)
            continue

        emb = get_embedding(app, img)
        if emb is None:
            log.warning("  ✗ No face detected — using fallback")
            fallbacks.append(celeb)
            time.sleep(0.3)
            continue

        results.append({
            "name":       name,
            "gender":     celeb.get("gender", "M"),
            "category":   celeb.get("category", "Celebrity"),
            "face_shape": celeb.get("face_shape", "Oval"),
            "fun_fact":   celeb.get("fun_fact", ""),
            "embedding":  emb,          # np.ndarray shape (512,)
            "vector":     celeb.get("vector", []),  # proportion fallback
        })
        log.info("  ✓ Embedded (%d-dim)", emb.shape[0])

        # Be polite to Wikipedia API
        time.sleep(0.5)

    # Build FAISS index for fast search
    import faiss
    if results:
        matrix = np.stack([r["embedding"] for r in results]).astype(np.float32)
        faiss.normalize_L2(matrix)
        index  = faiss.IndexFlatIP(matrix.shape[1])  # inner product = cosine on L2-normed
        index.add(matrix)
    else:
        index = None

    payload = {
        "celebrities": results,
        "fallbacks":   fallbacks,
        "faiss_index": faiss.serialize_index(index) if index else None,
        "dim":         512,
    }

    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump(payload, f)

    log.info(
        "Done. Embedded: %d  Fallback: %d  Saved to: %s",
        len(results), len(fallbacks), OUTPUT_PATH,
    )


if __name__ == "__main__":
    build()
