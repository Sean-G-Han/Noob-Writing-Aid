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

def add_character_pattern(nlp, phrase: str, label: str = "CHARACTER"):
    # tokenizer safeguard (optional, but keep if you want)
    nlp.tokenizer.add_special_case(
        phrase,
        [{"ORTH": phrase}]
    )

    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        ruler = nlp.get_pipe("entity_ruler")

    ruler.add_patterns([
        {
            "label": label,
            "pattern": [{"LOWER": t} for t in phrase.split()]
        }
    ])

def get_nlp_model():
    return nlp