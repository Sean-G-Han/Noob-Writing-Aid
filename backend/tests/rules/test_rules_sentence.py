from rules.sentence_rules import *
from components.components import Word, Sentence

def make_sentence(words):
    text = " ".join(word.text for word in words)
    sentence = Sentence(text, words=words)
    for i, w in enumerate(sentence.words):
        w.index = i
    return sentence

def test_repeated_word_detected():
    rule = RepeatedWordRule()

    sentence = make_sentence([
        Word(text="this", pos="DET"),
        Word(text="is", pos="VERB"),
        Word(text="is", pos="VERB"),
    ])

    result = rule.apply(sentence)

    assert result == True
    assert any(w.critics for w in sentence.words)

def test_repeated_word_not_detected():
    rule = RepeatedWordRule()

    sentence = make_sentence([
        Word(text="this", pos="DET"),
        Word(text="is", pos="VERB"),
        Word(text="good", pos="ADJ"),
    ])

    result = rule.apply(sentence)

    assert result == False

def test_repeated_word_short_sentence():
    rule = RepeatedWordRule()

    sentence = make_sentence([
        Word(text="Hello", pos="INTJ"),
    ])

    result = rule.apply(sentence)
    assert result == False

def test_repeated_word_seperated_by_punctuation():
    rule = RepeatedWordRule()

    sentence = make_sentence([
        Word(text="Hello", pos="INTJ"),
        Word(text=",", pos="PUNCT"),
        Word(text="Hello", pos="INTJ"),
    ])

    result = rule.apply(sentence)

    assert result == True

def test_to_be_adjective_detected():
    rule = ToBeAdjectiveRule()

    sentence = make_sentence([
        Word(text="it", pos="PRON", lemma="it"),
        Word(text="is", pos="AUX", lemma="be"),
        Word(text="bad", pos="ADJ"),
    ])

    result = rule.apply(sentence)

    assert result == True
    assert sentence.words[2].critics

def test_to_be_adjective_not_detected():
    rule = ToBeAdjectiveRule()

    sentence = make_sentence([
        Word(text="he", pos="PRON"),
        Word(text="runs", pos="VERB"),
    ])

    result = rule.apply(sentence)

    assert result == False

def test_present_sva_detects_error():
    rule = PresentSVARule()

    sentence = make_sentence([
        Word(text="the", pos="DET", lemma="the"),
        Word(text="dogs", pos="NOUN", morph="Number=Plur"),
        Word(text="runs", pos="VERB", morph="VerbForm=Fin|Tense=Pres|Number=Sing")
    ])

    sentence.words[1].dependency = "nsubj"
    sentence.words[1].head_index = 2

    result = rule.apply(sentence)

    assert result == True

def test_present_sva_no_error():
    rule = PresentSVARule()

    sentence = make_sentence([
        Word(text="the", pos="DET", lemma="the"),
        Word(text="dog", pos="NOUN", morph="Number=Sing"),
        Word(text="runs", pos="VERB", morph="VerbForm=Fin|Tense=Pres|Number=Sing")
    ])

    sentence.words[0].dependency = "nsubj"
    sentence.words[0].head_index = 1

    result = rule.apply(sentence)

    assert result == False

def test_past_to_be_sva_detected():
    rule = PastToBeSVARule()

    sentence = make_sentence([
        Word(text="happy", pos="ADJ"),
        Word(text="he", pos="PRON", morph="Number=Sing"),
        Word(text="were", pos="AUX", lemma="be", morph="Tense=Past"),
    ])

    sentence.words[1].dependency = "nsubj"
    sentence.words[1].head_index = 2

    sentence.words[2].dependency = "root"

    result = rule.apply(sentence)

    assert result == True

def test_perfect_tense_sva_detected():
    rule = PerfectTenseSVARule()
    sentence = make_sentence([
        Word(text="the", pos="DET", lemma="the"),
        Word(text="cat", pos="NOUN", morph="Number=Sing"),
        Word(text="have", pos="AUX", lemma="have", morph="VerbForm=Fin|Tense=Pres|Number=Plur"),
        Word(text="eaten", pos="VERB", morph="VerbForm=Part"),
    ])

    sentence.words[1].dependency = "nsubj"
    sentence.words[1].head_index = 3

    sentence.words[2].dependency = "aux"
    sentence.words[2].head_index = 3

    sentence.words[3].dependency = "root"

    result = rule.apply(sentence)
    assert result == True
    assert sentence.words[2].critics

    sentence = make_sentence([
        Word(text="the", pos="DET", lemma="the"),
        Word(text="cats", pos="NOUN", morph="Number=Plur"),
        Word(text="has", pos="AUX", lemma="have", morph="VerbForm=Fin|Tense=Pres|Number=Sing"),
        Word(text="eaten", pos="VERB", morph="VerbForm=Part"),
    ])

    sentence.words[1].dependency = "nsubj"
    sentence.words[1].head_index = 3

    sentence.words[2].dependency = "aux"
    sentence.words[2].head_index = 3

    sentence.words[3].dependency = "root"

    result = rule.apply(sentence)
    assert result == True

def test_inconsistent_tense_detected():
    rule = InconsistentTenseRule()

    sentence = make_sentence([
        Word(text="he", pos="PRON", morph=""),
        Word(text="goes", pos="VERB", morph="VerbForm=Fin Tense=Pres"),
        Word(text="went", pos="VERB", morph="VerbForm=Fin Tense=Past"),
    ])

    result = rule.apply(sentence)

    assert result == True
    assert sentence.critics

def test_determiner_rule_wrong_a():
    rule = DeterminerRule()

    sentence = make_sentence([
        Word(text="a", pos="DET", lemma="a"),
        Word(text="apple", pos="NOUN"),
    ])

    result = rule.apply(sentence)

    assert result == True
    assert sentence.words[0].critics

def test_determiner_rule_wrong_an():
    rule = DeterminerRule()

    sentence = make_sentence([
        Word(text="an", pos="DET", lemma="an"),
        Word(text="dog", pos="NOUN"),
    ])

    result = rule.apply(sentence)

    assert result == True

def test_double_negative_detected():
    rule = DoubleNegativeRule()

    sentence = make_sentence([
        Word(text="I", pos="PRON"),
        Word(text="do", pos="AUX"),
        Word(text="n't", dependency="neg"),
        Word(text="not", pos="ADV", dependency="neg"),
    ])

    result = rule.apply(sentence)

    assert result == True
    assert sentence.words[1].critics or sentence.words[2].critics

def test_double_negative_not_detected():
    rule = DoubleNegativeRule()

    sentence = make_sentence([
        Word(text="I", pos="PRON"),
        Word(text="don't", pos="AUX"),
    ])

    result = rule.apply(sentence)

    assert result == False

def test_sentence_fragment_detected():
    rule = SentenceFragmentRule()

    sentence = make_sentence([
        Word(text="No", pos="PART"),
        Word(text="way", pos="NOUN"),
        Word(text="here", pos="ADV"),
    ])

    result = rule.apply(sentence)

    assert result == True
    assert sentence.critics

def test_sentence_fragment_not_detected():
    rule = SentenceFragmentRule()

    sentence = make_sentence([
        Word(text="He", pos="PRON"),
        Word(text="runs", pos="VERB"),
    ])

    result = rule.apply(sentence)

    assert result == False

def test_word_echo_detected():
    rule = WordEchoRule()

    sentence = make_sentence([
        Word(text="dog", pos="NOUN", lemma="dog"),
        Word(text="dog", pos="NOUN", lemma="dog"),
    ])

    result = rule.apply(sentence)

    assert result == True
    assert sentence.words[1].critics

def test_word_echo_not_detected():
    rule = WordEchoRule()

    sentence = make_sentence([
        Word(text="dog", pos="NOUN", lemma="dog"),
        Word(text="cat", pos="NOUN", lemma="cat"),
    ])

    result = rule.apply(sentence)

    assert result == False

def test_word_echo_ignore_common_words():
    rule = WordEchoRule()

    sentence = make_sentence([
        Word(text="the", pos="DET", lemma="the"),
        Word(text="dog", pos="NOUN", lemma="dog"),
        Word(text="and", pos="CCONJ", lemma="and"),
        Word(text="the", pos="DET", lemma="the"),
        Word(text="cat", pos="NOUN", lemma="cat"),
    ])

    result = rule.apply(sentence)

    assert result == False