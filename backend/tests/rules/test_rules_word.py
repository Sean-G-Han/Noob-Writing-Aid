from rules.word_rules import *

from components.components import Word
from components.critic import Critic

def test_adverb_rule_detects_adverb():
    rule = AdverbRule()
    word = Word(text="quickly", pos="ADV")

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1
    assert word.critics[0].type == Critic.Type.STYLE

def test_adverb_rule_no_issue():
    rule = AdverbRule()
    word = Word(text="dog", pos="NOUN")

    result = rule.apply(word)

    assert result == False
    assert len(word.critics) == 0

def test_weak_verb_rule_detects_weak_verb():
    rule = WeakVerbRule()
    word = Word(text="make", pos="VERB", lemma="make")

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1

def test_weak_verb_rule_strong_verb():
    rule = WeakVerbRule()
    word = Word(text="run", pos="VERB", lemma="run")

    result = rule.apply(word)

    assert result == False
    assert len(word.critics) == 0

def test_weak_adverb_detected():
    rule = WeakAdverbRule()
    word = Word(text="really", pos="ADV", lemma="really")

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1
    assert word.critics[0].severity == Critic.Severity.MEDIUM

def test_weak_adverb_not_detected():
    rule = WeakAdverbRule()
    word = Word(text="quickly", pos="ADV", lemma="quickly")

    result = rule.apply(word)

    assert result == False

def test_weak_filler_detected():
    rule = WeakFillerRule()
    word = Word(text="thing", lemma="thing")

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1

def test_weak_filler_not_detected():
    rule = WeakFillerRule()
    word = Word(text="innovation", lemma="innovation")

    result = rule.apply(word)

    assert result == False

def test_passive_voice_detected():
    rule = PassiveVoiceRule()
    word = Word(text="was", dependency="auxpass")

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1

def test_passive_voice_not_detected():
    rule = PassiveVoiceRule()
    word = Word(text="was", dependency="aux")

    result = rule.apply(word)

    assert result == False

def test_spelling_rule_detects_error():
    rule = SpellingRule()
    word = Word(text="speling", pos="NOUN")

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1
    assert word.critics[0].type == Critic.Type.SPELLING

def test_spelling_rule_ignores_proper_word():
    rule = SpellingRule()
    word = Word(text="correct", pos="NOUN")

    result = rule.apply(word)

    assert result == False

def test_spelling_rule_ignores_punctuation_and_numbers():
    rule = SpellingRule()
    word = Word(text="123", pos="NUM")

    result = rule.apply(word)

    assert result == False

def test_spelling_rule_ignores_contractions():
    rule = SpellingRule()
    word = Word(text="don't", pos="VERB")

    result = rule.apply(word)

    assert result == False

def test_spelling_rule_ignores_apostrophes():
    rule = SpellingRule()
    word1 = Word(text="n’t", pos="VERB")
    word2 = Word(text="n't", pos="VERB")

    result1 = rule.apply(word1)
    result2 = rule.apply(word2)

    assert result1 == False
    assert result2 == False

def test_ambiguous_pronoun_not_pronoun():
    rule = AmbiguousPronounRule()
    word = Word(text="table", pos="NOUN")

    result = rule.apply(word)

    assert result == False
    assert len(word.critics) == 0

def test_ambiguous_pronoun_no_reference():
    rule = AmbiguousPronounRule()
    word = Word(text="he", pos="PRON")
    word.char_ref = set()

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1

def test_ambiguous_pronoun_multiple_references():
    rule = AmbiguousPronounRule()
    word = Word(text="he", pos="PRON")
    word.char_ref = {"John", "Mike"}

    result = rule.apply(word)

    assert result == True
    assert len(word.critics) == 1

def test_ambiguous_pronoun_clear_reference():
    rule = AmbiguousPronounRule()
    word = Word(text="he", pos="PRON")
    word.char_ref = {"John"}

    result = rule.apply(word)

    assert result == False
    assert len(word.critics) == 0