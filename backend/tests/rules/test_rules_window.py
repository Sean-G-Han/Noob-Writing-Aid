from rules.window_rules import RepeatedSubjectRule
from components.components import Word, Sentence

def make_sentence(words):
    text = " ".join(word.text for word in words)
    sentence = Sentence(text, words=words)
    for i, w in enumerate(sentence.words):
        w.index = i
    return sentence

def test_repeated_subject_detected():
    rule = RepeatedSubjectRule()

    sentence = make_sentence([
        Word(text="he", pos="PRON", lemma="he", dependency="nsubj"),
        Word(text="eats", pos="VERB"),
        Word(text="he", pos="PRON", lemma="he", dependency="nsubj"),
        Word(text="runs", pos="VERB"),
    ])

    assert rule.apply_insert(sentence.words[0]) == False
    assert rule.apply_insert(sentence.words[2]) == True

    assert sentence.words[2].critics

def test_repeated_subject_removed_correctly():
    rule = RepeatedSubjectRule()

    w1 = Word(text="he", pos="PRON", lemma="he", dependency="nsubj")
    w2 = Word(text="he", pos="PRON", lemma="he", dependency="nsubj")

    w1.index = 0
    w2.index = 1

    rule.apply_insert(w1)
    rule.apply_insert(w2)

    assert "he" in rule.referents

    rule.apply_remove(w1)
    assert "he" in rule.referents
    
    rule.apply_remove(w2)
    assert "he" not in rule.referents