import asyncio
import base64
import io
import os
import urllib.request

import cv2
import mediapipe as mp
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from PIL import Image

from brow_analyzer import analyze_brows
from eye_analyzer import analyze_eyes
from face_structure import analyze_face_structure
from harmony_scores import analyze_harmony
from insight_generator import generate_insights
from jaw_analyzer import analyze_jaw
from lip_analyzer import analyze_lips
from nose_analyzer import analyze_nose
from skin_analyzer import analyze_skin

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(title="Facial Feature Analysis API", version="1.0.0")

CORS_ORIGIN = os.getenv("BACKEND_CORS_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024   # 10 MB
SEMAPHORE     = asyncio.Semaphore(2)  # max 2 concurrent analyses

# ── MediaPipe Tasks setup ─────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "face_landmarker.task")
MODEL_URL  = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("[setup] Downloading face_landmarker.task model (~30 MB)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("[setup] Model downloaded.")

_base_options  = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
_face_options  = mp_vision.FaceLandmarkerOptions(
    base_options=_base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1,
)
face_landmarker = mp_vision.FaceLandmarker.create_from_options(_face_options)


# ── Helpers ───────────────────────────────────────────────────────────────────
def landmarks_to_list(landmarks, img_w, img_h):
    """Convert MediaPipe Tasks landmarks (NormalizedLandmark) to serializable list."""
    return [
        {"x": round(lm.x * img_w, 2), "y": round(lm.y * img_h, 2), "z": round(lm.z, 4)}
        for lm in landmarks
    ]


def confidence_overall(results: dict) -> int:
    scores = []
    for section in results.values():
        if isinstance(section, dict) and "confidence" in section:
            scores.append(section["confidence"])
    return int(np.mean(scores)) if scores else 80


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # File size check
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Image too large. Max size is 10 MB.")

    # Validate image
    try:
        pil_img = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    async with SEMAPHORE:
        return await asyncio.get_event_loop().run_in_executor(None, _run_analysis, pil_img, content)


def _run_analysis(pil_img: Image.Image, raw_bytes: bytes):
    # Convert to OpenCV BGR
    img_rgb = np.array(pil_img)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    img_h, img_w = img_bgr.shape[:2]

    # Run MediaPipe Tasks FaceLandmarker
    mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    detection = face_landmarker.detect(mp_image)
    if not detection.face_landmarks:
        raise HTTPException(status_code=422, detail="No face detected. Please upload a clear front-facing photo.")

    landmarks = detection.face_landmarks[0]

    # Run all 8 analyzers
    face   = analyze_face_structure(landmarks, img_w, img_h)
    eyes   = analyze_eyes(landmarks, img_w, img_h)
    brows  = analyze_brows(landmarks, img_w, img_h)
    nose   = analyze_nose(landmarks, img_w, img_h)
    lips_r = analyze_lips(landmarks, img_w, img_h)
    jaw    = analyze_jaw(landmarks, img_w, img_h)
    skin   = analyze_skin(img_bgr, landmarks, img_w, img_h)
    harmony = analyze_harmony(face, eyes, nose, lips_r, jaw)

    # Generate insights
    insights = generate_insights(face, eyes, brows, nose, lips_r, jaw, skin, harmony)

    # Build landmark list for frontend overlay
    lm_list = landmarks_to_list(landmarks, img_w, img_h)

    # Encode original image as base64 for frontend display
    img_b64 = base64.b64encode(raw_bytes).decode("utf-8")
    mime     = "image/jpeg"

    # Strip internal keys (prefixed with _)
    def clean(d):
        return {k: v for k, v in d.items() if not k.startswith("_")}

    face_clean  = clean(face)
    eyes_clean  = clean(eyes)
    nose_clean  = clean(nose)

    response = {
        "imageDimensions": {"width": img_w, "height": img_h},
        "imageBase64":     img_b64,
        "imageMime":       mime,
        "landmarks":       lm_list,
        "confidenceOverall": confidence_overall({
            "face": face, "eyes": eyes, "brows": brows,
            "nose": nose, "lips": lips_r, "jaw": jaw, "skin": skin,
        }),
        "faceStructure": face_clean,
        "eyes":          eyes_clean,
        "eyebrows":      clean(brows),
        "nose":          nose_clean,
        "lips":          clean(lips_r),
        "jaw":           clean(jaw),
        "skin":          clean(skin),
        "harmonyScores": harmony,
        "insights":      insights,
    }
    return response
