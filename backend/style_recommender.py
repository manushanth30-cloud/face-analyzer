"""
Style Recommender — generates personalized style & grooming recommendations
based on facial analysis results (face shape, skin tone, eye shape, jaw, etc.)
"""

# ── Makeup recommendations by face shape ──────────────────────────────────────
MAKEUP_BY_SHAPE = {
    "Oval": {
        "foundation": "Any formula works — your balanced proportions suit all finishes.",
        "contour":    "Light contour along temples to maintain the oval's natural harmony.",
        "blush":      "Apply blush on the apples of cheeks and blend upward toward temples.",
        "highlight":  "Center of forehead, bridge of nose, and Cupid's bow.",
        "eyeshadow":  "Any style flatters — try a soft smoky eye or cut-crease to play up your symmetry.",
        "eyeliner":   "Winged liner or tight-line for depth — both work beautifully.",
        "lip":        "Any lip shape works; try an ombre to add dimension.",
    },
    "Round": {
        "foundation": "Matte finish to reduce shine and add structure.",
        "contour":    "Contour along the temples and jawline to elongate. Avoid blush on cheeks.",
        "blush":      "Apply high on cheekbones in a C-shape toward temples.",
        "highlight":  "Vertical strip down the center of the face to elongate.",
        "eyeshadow":  "Elongated cat-eye or almond shape to stretch the eye horizontally.",
        "eyeliner":   "Extend liner beyond outer corner with a slight upward flick.",
        "lip":        "Ombre from center outward to add definition without width.",
    },
    "Square": {
        "foundation": "Luminous or dewy to soften angular features.",
        "contour":    "Soften corners of forehead and jaw with contour. Blend well.",
        "blush":      "Round circular application on apples of cheeks — avoid angular placement.",
        "highlight":  "Center of nose and brow bone to draw attention upward.",
        "eyeshadow":  "Soft, rounded blended shadow — avoid sharp angles.",
        "eyeliner":   "Rounded liner on upper lid to soften the square jaw.",
        "lip":        "Fuller rounded lip shape; avoid overly defined corners.",
    },
    "Heart": {
        "foundation": "Any finish — your face shape is naturally photogenic.",
        "contour":    "Contour the forehead sides to reduce width. Add subtle contour under cheekbones.",
        "blush":      "Below the cheekbones and sweep toward ears to balance the wide forehead.",
        "highlight":  "Chin and Cupid's bow to add attention downward.",
        "eyeshadow":  "Soft, horizontally spread shadow to balance the wide forehead.",
        "eyeliner":   "Lower lash line liner to add width to the lower face.",
        "lip":        "Accentuate the natural Cupid's bow — a strong lip is your signature.",
    },
    "Diamond": {
        "foundation": "Satin finish to let your high cheekbones shine.",
        "contour":    "Soften the wide cheekbones with light contour. Add width at forehead and chin.",
        "blush":      "Light swipe on cheekbones blending upward — less is more.",
        "highlight":  "Forehead and chin to add width at extremities.",
        "eyeshadow":  "Horizontally spread shadow to balance the narrow forehead.",
        "eyeliner":   "Winged liner extending outward to broaden the eye area.",
        "lip":        "Defined, full lip shape to add volume to the narrow chin.",
    },
    "Oblong": {
        "foundation": "Matte finish to avoid elongating the face further.",
        "contour":    "Contour hairline and chin to shorten. Blush horizontally to add width.",
        "blush":      "Apply horizontally across cheeks to add width — avoid vertical placement.",
        "highlight":  "Sides of temples and chin for added width.",
        "eyeshadow":  "Wide, horizontally blended shadow — avoid tall eye looks.",
        "eyeliner":   "Horizontal liner across upper and lower lash line.",
        "lip":        "Full lips with defined corners to add width.",
    },
}

# ── Eyebrow recommendations ───────────────────────────────────────────────────
EYEBROW_BY_SHAPE = {
    "Oval":    "High arched brows with a sharp peak — any brow style flatters. Try a natural feathered brow.",
    "Round":   "High, angled arch to elongate and add definition. Avoid thin or flat brows.",
    "Square":  "Softly arched, slightly curved brows to soften the angular jaw. Avoid sharply angular brows.",
    "Heart":   "Low, gently arched brows to balance the wide forehead. Soft and natural.",
    "Diamond": "Curved, softly arched brows to balance prominent cheekbones.",
    "Oblong":  "Flat, horizontal brows with minimal arch to add width and reduce length.",
}

# ── Hairstyle recommendations ─────────────────────────────────────────────────
HAIRSTYLE_WOMEN = {
    "Oval":    ["Beach waves", "Sleek ponytail", "Long layers", "Blunt bob", "Any style — you can pull it all off!"],
    "Round":   ["Long layers below the chin", "Side-swept bangs", "High ponytail", "Textured lob", "Avoid chin-length bobs"],
    "Square":  ["Soft waves", "Side parts", "Layered cuts below the jaw", "Wispy fringe", "Avoid blunt cuts at jaw level"],
    "Heart":   ["Long layers starting below the chin", "Side-swept bangs", "Lob or shoulder-length", "Avoid volume at the crown"],
    "Diamond": ["Chin-length bob", "Blunt bangs", "Mid-length with volume at jaw", "Avoid too much volume at cheeks"],
    "Oblong":  ["Blunt bobs", "Curtain bangs", "Beachy waves with volume at sides", "Avoid super long straight styles"],
}

HAIRSTYLE_MEN = {
    "Oval":    ["Quiff", "Textured crop", "Side part", "Pompadour", "French crop — almost any style works"],
    "Round":   ["High fade with volume on top", "Quiff", "Textured undercut", "Avoid buzz cuts or styles that add width at sides"],
    "Square":  ["Side part", "Textured fringe", "Longer on top, tapered sides", "Avoid flat-top or wide styles"],
    "Heart":   ["Mid-length with fringe", "Textured crop", "Side sweep", "Avoid very short or very tall styles"],
    "Diamond": ["Textured crop with fade", "Side part", "Avoid styles with lots of side volume"],
    "Oblong":  ["Side part with fringe", "Textured quiff", "Avoid tall styles that add length — keep volume at sides"],
}

# ── Hair color recommendations by skin tone ───────────────────────────────────
HAIR_COLOR_BY_SKIN = {
    "I":   ["Ash blonde", "Platinum", "Light golden brown", "Rose gold"],
    "II":  ["Golden blonde", "Honey blonde", "Warm brown", "Strawberry blonde"],
    "III": ["Caramel", "Chestnut", "Rich brown", "Dark copper"],
    "IV":  ["Dark chocolate", "Mahogany", "Deep auburn", "Rich black with warm undertones"],
    "V":   ["Jet black", "Deep espresso", "Dark auburn", "Burgundy"],
    "VI":  ["Natural black", "Blue-black", "Deep plum", "Chocolate brown"],
}

# ── Glasses recommendations ───────────────────────────────────────────────────
GLASSES_WOMEN = {
    "Oval":    "Cat-eye or round frames — your balanced face handles both beautifully.",
    "Round":   "Angular or rectangular frames to add definition and elongate the face.",
    "Square":  "Round or oval frames to soften the angular jawline.",
    "Heart":   "Bottom-heavy or rimless frames to balance the wide forehead.",
    "Diamond": "Oval or rimless frames to soften prominent cheekbones.",
    "Oblong":  "Wide frames or decorative temples to add width and break up the length.",
}

GLASSES_MEN = {
    "Oval":    "Aviators, wayfarers, or round frames — most styles work perfectly.",
    "Round":   "Square or rectangular frames to add definition and structure.",
    "Square":  "Round or oval frames to soften the strong jaw.",
    "Heart":   "Light, small rectangular frames or rimless glasses.",
    "Diamond": "Oval frames or subtle wayfarers — avoid bold wide frames.",
    "Oblong":  "Wide, bold frames like wayfarers to add width and shorten appearance.",
}

# ── Color palette for clothing (by skin tone) ─────────────────────────────────
COLOR_PALETTE_BY_SKIN = {
    "I": {
        "best":   ["Soft pink", "Light blue", "Lavender", "Warm white", "Mint green"],
        "avoid":  ["Neon yellow", "Overly bright orange"],
        "neutrals": ["Off-white", "Light grey", "Blush beige"],
        "tip":    "Your fair skin glows in soft pastels and cool tones. Avoid overly saturated colors.",
    },
    "II": {
        "best":   ["Peach", "Coral", "Warm yellow", "Sage green", "Sky blue"],
        "avoid":  ["Dark muddy tones"],
        "neutrals": ["Cream", "Camel", "Light khaki"],
        "tip":    "Warm and peachy tones complement your skin beautifully.",
    },
    "III": {
        "best":   ["Terracotta", "Olive green", "Warm red", "Mustard", "Deep teal"],
        "avoid":  ["Pastel washed-out tones"],
        "neutrals": ["Warm beige", "Chocolate brown", "Tan"],
        "tip":    "Rich, earthy tones bring out the warmth in your complexion.",
    },
    "IV": {
        "best":   ["Burnt orange", "Deep teal", "Rich purple", "Forest green", "Cobalt blue"],
        "avoid":  ["Light beige that washes you out"],
        "neutrals": ["Dark olive", "Warm brown", "Charcoal"],
        "tip":    "Bold jewel tones contrast beautifully with your rich skin tone.",
    },
    "V": {
        "best":   ["Bright white", "Cobalt blue", "Rich gold", "Hot pink", "Vibrant orange"],
        "avoid":  ["Dark muddy browns that blend into skin"],
        "neutrals": ["Black", "Dark navy", "Deep grey"],
        "tip":    "High contrast colors like bright white and bold jewels look stunning against your deep skin.",
    },
    "VI": {
        "best":   ["Royal purple", "Electric blue", "Bright red", "Emerald green", "Bright white"],
        "avoid":  ["Dark brown that blends into skin"],
        "neutrals": ["Black", "Charcoal", "Deep navy"],
        "tip":    "Bold, vibrant colors create stunning contrast. Bright white is your power neutral.",
    },
}

# ── Beard recommendations ─────────────────────────────────────────────────────
BEARD_BY_SHAPE = {
    "Oval":    "Lucky you — almost any beard style works. Try a full beard, stubble, or a classic short boxed beard.",
    "Round":   "Goatee or chin strap to elongate. Keep sides trimmed short. Avoid full round beards.",
    "Square":  "Short stubble or a rounded full beard to soften angular jaw. Avoid sharp, defined beard lines.",
    "Heart":   "Full beard or chinstrap to add width and weight to the narrow chin.",
    "Diamond": "Full beard to add width at the chin and jaw, balancing prominent cheekbones.",
    "Oblong":  "Short, full beard with volume on the sides to add width. Avoid long goatees that add length.",
}

# ── Men's grooming suggestions ────────────────────────────────────────────────
GROOMING_BY_FEATURES = {
    "high_symmetry":    "Your high facial symmetry is a major asset — keep grooming clean and minimalist to let your features shine.",
    "low_symmetry":     "Strategic grooming can enhance balance — a well-shaped beard can compensate for asymmetry.",
    "sharp_jaw":        "Your defined jaw benefits from clean-shaven or tight stubble to showcase the structure.",
    "soft_jaw":         "A shaped beard or goatee can add definition and structure to your jawline.",
    "prominent_brows":  "Keep brows groomed — a light trim and defined arch adds polish without looking over-done.",
    "wide_set_eyes":    "A subtle center brow groom helps draw eyes inward for a balanced appearance.",
    "close_set_eyes":   "Let brow tails extend naturally to visually widen the eye area.",
    "full_lips":        "Your full lips are a strong feature — keep them moisturized and let them stand out.",
    "thin_lips":        "A clean-shaven upper lip draws attention upward. Light exfoliation adds natural fullness.",
}


def generate_style_recommendations(face, eyes, brows, nose, lips, jaw, skin):
    """Generate gender-specific style and grooming recommendations."""

    face_shape    = face.get("shape", "Oval")
    skin_tone     = skin.get("fitzpatrick", "III")
    eye_shape     = eyes.get("shape", "Almond")
    eye_spacing   = eyes.get("spacing", "Ideal")
    jaw_type      = jaw.get("type", "Defined")
    lip_fullness  = lips.get("fullness", "Medium")
    symmetry      = face.get("symmetryScore", 80)
    brow_shape    = brows.get("shape", "Arched")
    dark_circles  = skin.get("darkCircles", "None")
    skin_evenness = skin.get("evennessScore", 75)

    # ── Photography tips ───────────────────────────────────────────────────────
    angle_map = {
        "Oval":    "Camera slightly above eye level (5–10°) angled down — shows off balanced proportions.",
        "Round":   "Camera 10–15° above eye level, tilt chin slightly down to elongate.",
        "Square":  "Camera at eye level, 3/4 angle to soften the strong jaw.",
        "Heart":   "Camera at or slightly below eye level, straight-on or 3/4 to balance the forehead.",
        "Diamond": "Camera at eye level, slight downward tilt to add width to forehead.",
        "Oblong":  "Camera at eye level, straight-on — avoid shooting from below.",
    }
    photography_tips = {
        "bestAngle":          angle_map.get(face_shape, "Camera at or slightly above eye level."),
        "bestSide":           "Either side (very symmetric)" if symmetry >= 85 else "Try both sides — one will feel more natural. Your stronger side typically photographs better.",
        "lightingStyle":      "Soft diffused natural light from a 45° angle (Rembrandt lighting). Avoid harsh overhead flash.",
        "lensRecommendation": "85–105mm portrait lens to avoid distortion. Avoid wide-angle lenses (below 35mm).",
        "postingTip":         "Natural smile with soft eyes (Duchenne smile). Relaxed jaw, slight chin-forward posture.",
        "backgroundTip":      "Clean neutral or blurred background (bokeh) so features remain the focal point.",
    }

    # ── Skincare routine (by Fitzpatrick + skin concerns) ─────────────────────
    # Morning routine — universal core + concern-specific add-ons
    morning_routine = ["Gentle cleanser", "Vitamin C serum (brightening)", "Moisturiser", "SPF 50+ sunscreen (non-negotiable)"]
    evening_routine = ["Double cleanse (oil + water-based)", "Retinol or Retinoid (start 2×/week)", "Niacinamide toner", "Rich moisturiser or sleeping mask"]
    weekly_routine  = ["Chemical exfoliant (AHA/BHA — 2×/week)", "Hydrating sheet mask", "Facial massage with gua sha or jade roller"]

    if dark_circles in ("Moderate", "Prominent"):
        morning_routine.insert(1, "Caffeine + Vitamin K eye cream (AM)")
        evening_routine.insert(-1, "Retinol eye cream (PM)")

    if skin_evenness < 60:
        morning_routine.insert(2, "Alpha Arbutin or Kojic Acid serum for evenness")

    if skin_tone in ("I", "II"):
        morning_routine.append("Avoid fragranced products — fair skin is more reactive")

    skincare_routine = {
        "morning": morning_routine,
        "evening": evening_routine,
        "weekly":  weekly_routine,
        "proTip":  "Consistency beats intensity — a simple routine done daily outperforms a complex one done occasionally.",
    }

    # ── Grooming tips selection ────────────────────────────────────────────────
    grooming_tips = []
    if symmetry >= 85:
        grooming_tips.append(GROOMING_BY_FEATURES["high_symmetry"])
    else:
        grooming_tips.append(GROOMING_BY_FEATURES["low_symmetry"])
    if jaw_type in ["Sharp", "Defined"]:
        grooming_tips.append(GROOMING_BY_FEATURES["sharp_jaw"])
    else:
        grooming_tips.append(GROOMING_BY_FEATURES["soft_jaw"])
    if eye_spacing == "Wide-set":
        grooming_tips.append(GROOMING_BY_FEATURES["wide_set_eyes"])
    elif eye_spacing == "Close-set":
        grooming_tips.append(GROOMING_BY_FEATURES["close_set_eyes"])
    if lip_fullness in ["Full", "Very full"]:
        grooming_tips.append(GROOMING_BY_FEATURES["full_lips"])
    elif lip_fullness == "Thin":
        grooming_tips.append(GROOMING_BY_FEATURES["thin_lips"])

    # ── Grooming plan (men) ───────────────────────────────────────────────────
    grooming_plan = {
        "daily": [
            "AM: Cleanser + lightweight moisturiser + SPF 30+ (yes, men need it too)",
            "PM: Cleanser + eye cream if dark circles present",
            "Beard: comb/brush, apply beard oil if over 3mm",
            "Brows: quick spoolie brush to keep in shape",
        ],
        "weekly": [
            "Exfoliate under the beard line",
            "Trim beard edges or any strays",
            "Deep-clean pores (clay mask or BHA exfoliant)",
            "Scalp massage with hair oil for 5 minutes",
        ],
        "monthly": [
            "Professional haircut or trim",
            "Beard shaping and fade (barber visit)",
            "Brow threading or waxing for clean lines",
            "Skin check: adjust routine for seasonal changes",
        ],
    }

    # ── Women's recommendations ───────────────────────────────────────────────
    women = {
        "makeup":          MAKEUP_BY_SHAPE.get(face_shape, MAKEUP_BY_SHAPE["Oval"]),
        "eyebrowShape":    EYEBROW_BY_SHAPE.get(face_shape, "Natural arched brows work beautifully."),
        "hairstyles":      HAIRSTYLE_WOMEN.get(face_shape, HAIRSTYLE_WOMEN["Oval"]),
        "hairColors":      HAIR_COLOR_BY_SKIN.get(skin_tone, HAIR_COLOR_BY_SKIN["III"]),
        "glasses":         GLASSES_WOMEN.get(face_shape, "Oval frames are universally flattering."),
        "colorPalette":    COLOR_PALETTE_BY_SKIN.get(skin_tone, COLOR_PALETTE_BY_SKIN["III"]),
        "photographyTips": photography_tips,
        "skincareRoutine": skincare_routine,
        "basedOn": {
            "faceShape": face_shape,
            "skinTone":  f"Fitzpatrick {skin_tone}",
            "eyeShape":  eye_shape,
        },
    }

    # ── Men's recommendations ─────────────────────────────────────────────────
    men = {
        "beardStyle":      BEARD_BY_SHAPE.get(face_shape, "A well-groomed short beard suits your face shape."),
        "hairstyles":      HAIRSTYLE_MEN.get(face_shape, HAIRSTYLE_MEN["Oval"]),
        "glasses":         GLASSES_MEN.get(face_shape, "Wayfarers or oval frames are universally flattering."),
        "groomingTips":    grooming_tips,
        "groomingPlan":    grooming_plan,
        "colorPalette":    COLOR_PALETTE_BY_SKIN.get(skin_tone, COLOR_PALETTE_BY_SKIN["III"]),
        "hairColors":      HAIR_COLOR_BY_SKIN.get(skin_tone, HAIR_COLOR_BY_SKIN["III"]),
        "photographyTips": photography_tips,
        "skincareRoutine": skincare_routine,
        "basedOn": {
            "faceShape": face_shape,
            "skinTone":  f"Fitzpatrick {skin_tone}",
            "jawType":   jaw_type,
            "symmetry":  symmetry,
        },
    }

    return {"women": women, "men": men}
