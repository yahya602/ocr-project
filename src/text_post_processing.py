import re

def fix_bullets(text):

    # common OCR mistakes → bullet fix
    text = re.sub(r'(?m)^\s*[eo]\s+', '• ', text)   # e / o at line start
    text = re.sub(r'(?m)^\s*\.\s+', '• ', text)     # . as bullet
    text = re.sub(r'(?m)^\s*-\s+', '• ', text)      # - as bullet

    return text