import os
import cv2
from src.preprocessing import full_pipeline
from src.ocr_engine import extract_text
from src.evaluation import char_accuracy

def process_with_accuracy(image_folder, gt_folder):
    results = []

    for file in os.listdir(image_folder):

        if not (file.endswith(".png") or file.endswith(".jpg")):
            continue

        img_path = os.path.join(image_folder, file)
        name = os.path.splitext(file)[0]
        gt_path = os.path.join(gt_folder, name + ".txt")

        img = cv2.imread(img_path)

        if img is None:
            continue

        # preprocessing
        processed = full_pipeline(img)

        # OCR
        pred_text = extract_text(processed)

        # ground truth
        try:
            with open(gt_path, "r", encoding="utf-8") as f:
                actual_text = f.read()
        except:
            actual_text = ""

        # accuracy
        acc = char_accuracy(pred_text, actual_text)

        # 🔥 SAVE ALL DATA
        results.append((file, pred_text, acc))

    return results