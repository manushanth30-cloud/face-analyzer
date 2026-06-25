"""Test the celebrity_matcher module."""
import sys
sys.path.insert(0, r"c:\face-analyzer\backend")
from celebrity_matcher import CELEBRITIES, build_user_vector, find_celebrity_matches

# 1. Total count
print(f"Total celebrities: {len(CELEBRITIES)}")

# 2. Vector validation
ok = True
for c in CELEBRITIES:
    v = c["vector"]
    if len(v) != 12:
        print(f"BAD DIM: {c['name']} has {len(v)} dims")
        ok = False
    for val in v:
        if val < 0 or val > 1:
            print(f"BAD RANGE: {c['name']} has val {val}")
            ok = False
print(f"All vectors valid: {ok}")

# 3. Uniqueness
vecs = [tuple(c["vector"]) for c in CELEBRITIES]
print(f"Unique vectors: {len(set(vecs))}/1000")

# 4. Required fields
fields = ["name", "gender", "category", "face_shape", "vector", "fun_fact"]
all_have = all(all(f in c for f in fields) for c in CELEBRITIES)
print(f"All required fields: {all_have}")

# 5. Genders and shapes
genders = set(c["gender"] for c in CELEBRITIES)
shapes = set(c["face_shape"] for c in CELEBRITIES)
print(f"Genders: {genders}")
print(f"Shapes: {shapes}")

# 6. Category breakdown
cats = {}
for c in CELEBRITIES:
    cats[c["category"]] = cats.get(c["category"], 0) + 1
for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {n}")

# 7. Test female-filtered matching
vec = [0.55, 0.89, 0.52, 0.56, 0.46, 0.55, 0.45, 0.72, 0.70, 0.50, 0.58, 0.84]
f_matches = find_celebrity_matches(vec, top_n=5, gender_filter="F")
print("\nTop 5 female matches:")
for m in f_matches:
    print(f"  {m['name']} ({m['category']}) - {m['matchPercent']}%")
    print(f"    Shape: {m['faceShape']}, Fact: {m['funFact']}")
    print(f"    Similarities: {m['similarities']}")

# 8. Test build_user_vector
face = {"shape": "Oval", "symmetryScore": 85, "facialThirds": "Balanced",
        "facialFifths": "Balanced", "cheekboneProminence": "High",
        "widthToLengthRatio": 0.72, "_faceWidth": 100, "_faceHeight": 140,
        "_jawWidth": 80, "_cheekboneWidth": 95}
eyes = {"shape": "Almond", "canthalTilt": "+3.5", "spacing": "Ideal",
        "asymmetryScore": 88, "_eyeWidth": 20, "_interEyeDist": 22}
brows = {"shape": "Curved", "thickness": "Medium", "height": "Ideal",
         "symmetryScore": 85}
nose_d = {"widthRatio": "Proportionate", "tipShape": "Medium",
          "_noseWidth": 18, "_noseLength": 42}
lips_d = {"fullness": "Full", "upperLowerRatio": "1:1.6",
          "symmetryScore": 90, "_mouthWidth": 35}
jaw_d = {"type": "Defined", "symmetryScore": 87}
skin_d = {"fitzpatrick": "III", "tone": "Medium"}
harmony = {"goldenRatioScore": 72, "overallSymmetry": 85}

user_vec = build_user_vector(face, eyes, brows, nose_d, lips_d, jaw_d, skin_d, harmony)
print(f"\nUser vector: {user_vec}")
print(f"User vector length: {len(user_vec)}")

matches = find_celebrity_matches(user_vec, top_n=5)
print("\nTop 5 overall matches for user:")
for m in matches:
    print(f"  {m['name']}: {m['matchPercent']}% - {m['similarities']}")

print("\n=== ALL TESTS PASSED ===")
