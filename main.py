import os
import cv2
from src.preprocessing import full_pipeline
from src.ocr_engine import extract_text

folder = "data/raw"

for file in os.listdir(folder):

    if not file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    path = os.path.join(folder, file)
    img = cv2.imread(path)

    if img is None:
        continue

    # original OCR
    text1 = extract_text(img)

    # advanced OCR
    processed = full_pipeline(img)
    text2 = extract_text(processed)

    # choose better one
    final_text = text1 if len(text1.strip()) > len(text2.strip()) else text2

    print("\n======", file, "======")
    print(final_text)