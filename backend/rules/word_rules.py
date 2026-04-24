from rules.rules import WordRule
from components.components import Word
from components.critic import Critic
from spellchecker import SpellChecker

class AdverbRule(WordRule):
    def apply(self, word: Word):
        if word.pos == "ADV":
            critic = Critic(f"Adverb", Critic.Severity.LOW, Critic.Type.STYLE)
            word.add_critic(critic)
    
class WeakVerbRule(WordRule):
    WEAK_VERBS = {
        "be", "have", "do", "get", "make", "go", "take",
        "come", "see", "seem", "appear", "become",
        "remain", "stay", "look", "feel", "sound", "smell", "taste",
        "say", "tell", "ask", "think", "know", "want", "need",
        "like", "love", "hate", "prefer", "wish", "hope",
    }

    def apply(self, word: Word):
        if word.pos == "VERB" and word.lemma.lower() in self.WEAK_VERBS:
            critic = Critic(f"Weak verb", Critic.Severity.LOW, Critic.Type.STYLE)
            word.add_critic(critic)

class WeakAdverbRule(WordRule):
    WEAK_ADVERBS = {
        "very", "really", "quite", "just",
        "maybe", "probably", "actually",
        "fairly", "somewhat", "extremely",
        "literally", "absolutely", "totally", "completely"
    }

    def apply(self, word: Word):
        if word.pos == "ADV" and word.lemma.lower() in self.WEAK_ADVERBS:
            critic = Critic(f"Weak adverb", Critic.Severity.MEDIUM, Critic.Type.STYLE)
            word.add_critic(critic)


class WeakFillerRule(WordRule):
    WEAK_FILLERS = {
        "thing", "stuff", "nice", "good", "bad", "lot", "bit",
        "kind", "sort", "way", "part", "aspect", "point",
        "something", "anything", "everything", "nothing",
    }

    def apply(self, word: Word):
        if word.lemma.lower() in self.WEAK_FILLERS:
            critic = Critic(f"Weak filler", Critic.Severity.LOW, Critic.Type.STYLE)
            word.add_critic(critic)

class PassiveVoiceRule(WordRule):
    def apply(self, word: Word):
        if word.dependency == "auxpass":
            critic = Critic(f"Passive voice", Critic.Severity.LOW, Critic.Type.STYLE)
            word.add_critic(critic)

class SpellingRule(WordRule):
    def __init__(self):
        self.spell = SpellChecker() 

    def apply(self, word: Word):
        clean = word.text.strip('.,!?;:').lower()
        if clean == "’s" or clean == "n’t" or clean == "'s" or clean == "n't":
            return
        if clean and word.pos not in {"PUNCT", "NUM", "PROPN",  "SYM"} and clean not in self.spell:
            word.add_critic(Critic(
                f"Did you mispell '{word.text}'", 
                Critic.Severity.HIGH,
                Critic.Type.SPELLING
            ))

class AmbiguousPronounRule(WordRule):
    def apply(self, word: Word):
        if word.pos != "PRON":
            return
        if not word.char_ref or len(word.char_ref) == 0:
            word.add_critic(Critic(
                f"Ambiguous pronoun '{word.text}' with no clear reference",
                Critic.Severity.HIGH,
                Critic.Type.CLARITY
            ))
        elif len(word.char_ref) > 1:
            word.add_critic(Critic(
                f"Ambiguous pronoun '{word.text}' with multiple possible references: {', '.join(word.char_ref)}",
                Critic.Severity.MEDIUM,
                Critic.Type.CLARITY
            ))