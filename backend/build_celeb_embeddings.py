"""
build_celeb_embeddings.py
=========================
Build-time script — runs inside Docker during `docker build`.

Steps:
  1. Read celebrity list from celebrity_matcher.py
  2. Download Wikipedia profile thumbnail for each celebrity
  3. Run MediaPipe face_landmarker on the photo to extract all 478 landmarks
  4. Run `build_user_vector` on those landmarks to get a precise 20-dim geometry vector
  5. Save results to celeb_embeddings.pkl

This approach uses 0MB of extra memory, requires no heavy ML dependencies
(unlike InsightFace/ArcFace), and works entirely on the AWS Free Tier.
"""

import os
import sys
import pickle
import urllib.request
import urllib.parse
import json
import time
import logging

import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

# Import celebrity list and vector builder from sibling module
sys.path.insert(0, os.path.dirname(__file__))
from celebrity_matcher import CELEBRITIES, build_user_vector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "celeb_embeddings.pkl")

# ── MediaPipe setup ────────────────────────────────────────────────────────────
def load_mediapipe():
    model_path = os.path.join(os.path.dirname(__file__), "face_landmarker.task")
    if not os.path.exists(model_path):
        urllib.request.urlretrieve(
            "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
            model_path
        )
    
    base_options = mp_python.BaseOptions(
        model_asset_path=model_path,
        delegate=mp_python.BaseOptions.Delegate.CPU,
    )
    face_options = mp_vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
        num_faces=1,
    )
    return mp_vision.FaceLandmarker.create_from_options(face_options)


# ── Wikipedia photo fetcher ────────────────────────────────────────────────────
WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
HEADERS  = {"User-Agent": "FaceAnalyzerApp/1.0 (educational project)"}


def fetch_wiki_thumbnail(name: str) -> bytes | None:
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


def get_geometry_vector(landmarker, raw_bytes: bytes):
    """Run MediaPipe on raw bytes and return the 20-dim vector."""
    arr = np.frombuffer(raw_bytes, dtype=np.uint8)
    img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img_bgr is None:
        return None
        
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    detection = landmarker.detect(mp_image)
    if not detection.face_landmarks:
        return None
        
    landmarks = detection.face_landmarks[0]
    h, w, _ = img_bgr.shape
    
    # Compute the 20-dim geometric vector!
    return build_user_vector(landmarks, w, h)


# ── Main build routine ─────────────────────────────────────────────────────────
def build():
    log.info("Loading MediaPipe Face Landmarker …")
    landmarker = load_mediapipe()
    log.info("MediaPipe ready.")

    results   = []   # successfully processed celebrities
    fallbacks = []   # celebrities that will use original fake vectors

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

        vector = get_geometry_vector(landmarker, raw)
        if vector is None:
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
            "vector":     vector,  # REAL 20-dim Wikipedia geometry
        })
        log.info("  ✓ Processed")

        # Be polite to Wikipedia API
        time.sleep(0.5)

    payload = {
        "celebrities": results,
        "fallbacks":   fallbacks,
        "dim":         20,
    }

    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump(payload, f)

    log.info(
        "Done. Processed: %d  Fallback: %d  Saved to: %s",
        len(results), len(fallbacks), OUTPUT_PATH,
    )


if __name__ == "__main__":
    build()
