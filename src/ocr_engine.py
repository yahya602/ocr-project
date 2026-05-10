import pytesseract
import os

# 🔥 SAFE PATH HANDLING (NO MORE CRASH)
TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
]

def set_tesseract_path():
    for path in TESSERACT_PATHS:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return True
    return False

# auto set on import
if not set_tesseract_path():
    print("ERROR: Tesseract not found. Install it or fix path.")

def extract_text(img):
    try:
        return pytesseract.image_to_string(img)
    except Exception as e:
        print("OCR Error:", e)
        return ""