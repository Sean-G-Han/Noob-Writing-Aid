from rules. paragraph_rules import SentenceStartRepetitionRule, MonotonousLengthRule
from components.components import Word, Sentence, Paragraph

def make_sentence(words):
    text = " ".join(word.text for word in words)
    sentence = Sentence(text, words=words)
    for i, w in enumerate(sentence.words):
        w.index = i
    return sentence

def make_test_paragraph():
    sentence1 = make_sentence([
        Word(text="The", pos="DET"),
        Word(text="cat", pos="NOUN"),
        Word(text="sat", pos="VERB"),
    ])

    sentence2 = make_sentence([
        Word(text="The", pos="DET"),
        Word(text="dog", pos="NOUN"),
        Word(text="ran", pos="VERB"),
    ])

    sentence3 = make_sentence([
        Word(text="The", pos="DET"),
        Word(text="bird", pos="NOUN"),
        Word(text="flew", pos="VERB"),
    ])

    text = ". ".join(s.text for s in [sentence1, sentence2, sentence3])
    return Paragraph(text=text, sentences=[sentence1, sentence2, sentence3])

def test_sentence_start_repetition_rule():
    paragraph = make_test_paragraph()
    rule = SentenceStartRepetitionRule()

    result = rule.apply(paragraph)

    assert result == True

    for sentence in paragraph.sentences:
        assert sentence.words[0].critics

def test_monotonous_length_rule():
    paragraph = make_test_paragraph()
    rule = MonotonousLengthRule()

    result = rule.apply(paragraph)

    assert result == True