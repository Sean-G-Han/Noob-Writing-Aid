from util import get_model_path
import spacy

nlp = spacy.load(get_model_path())

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