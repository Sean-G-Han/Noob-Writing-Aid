import os
import sys
import spacy

def get_model_path():
    if hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
        model_path = os.path.join(bundle_dir, "en_core_web_sm", "en_core_web_sm-3.8.0")
        return model_path
    return "en_core_web_sm"

try:
    nlp = spacy.load(get_model_path())
except Exception as e:
    print(f"Detailed Error: {e}")