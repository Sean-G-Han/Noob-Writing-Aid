from components.components import Word, Document
from collections import deque
from rules.word_rules import *
from rules.sentence_rules import *
from rules.paragraph_rules import *
from rules.window_rules import *
from util import get_nlp_model

WORD_RULES: list[WordRule] = [
    AdverbRule(),
    WeakVerbRule(),
    WeakAdverbRule(),
    WeakFillerRule(),
    PassiveVoiceRule(),
    SpellingRule(),
    AmbiguousPronounRule(),
]

SENTENCE_RULES: list[SentenceRule] = [
    RepeatedWordRule(),
    ToBeAdjectiveRule(),
    PerfectTenseSVARule(),
    PastToBeSVARule(),
    PresentSVARule(),
    InconsistentTenseRule(),
    DeterminerRule(),
    DoubleNegativeRule(),
    SentenceFragmentRule(),
    WordEchoRule(),
]

PARAGRAPH_RULES: list[ParagraphRule] = [
    SentenceStartRepetitionRule(),
    MonotonousLengthRule(),
]

WINDOW_RULES: list[WindowRule] = [
    RepeatedSubjectRule(),
]

class SlidingWindow:
    def __init__(
        self,
        maxlen: int,
    ):
        self.buffer: deque[Word] = deque(maxlen=maxlen)

    def push(self, word: Word):
        self.buffer.append(word)
        if len(self.buffer) > self.buffer.maxlen:
            return self.buffer.popleft()

class Grader:
    def __init__(self):
        self.window = SlidingWindow(maxlen=50)
    
    def grade_text(self, doc: Document) -> str:
        print("Loading model...")
        
        print("Applying rules...")
        for item_type, component in doc.iter_words_with_context():
            if item_type == "WORD":
                for rule in WORD_RULES:
                    rule.apply(component)
            
                for rule in WINDOW_RULES:
                    rule.apply_insert(component)
                    removed_word = self.window.push(component)
                    if removed_word:
                        rule.apply_remove(removed_word)

            elif item_type == "SENT":
                for rule in SENTENCE_RULES:
                    rule.apply(component)

            elif item_type == "PARA":
                for rule in PARAGRAPH_RULES:
                    rule.apply(component)

        return str(doc)

if __name__ == "__main__":
    sample_text = "She is huge. Alice likes Dory. She says that she is her best friend. But Sam thinks that Miss Wonderful is annoying. He doesn't like her."
    doc = Document(sample_text, get_nlp_model())
    grader = Grader()
    print(grader.grade_text(doc))
