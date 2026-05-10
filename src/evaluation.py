import difflib
import re

def clean(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def char_accuracy(pred, actual):
    pred = clean(pred)
    actual = clean(actual)
    return difflib.SequenceMatcher(None, pred, actual).ratio() * 100