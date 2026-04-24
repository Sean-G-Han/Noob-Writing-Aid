from rules.rules import WindowRule
from components.components import Word
from components.critic import Critic

class RepeatedSubjectRule(WindowRule):
    def __init__(self):
        self.referents: dict[str, int] = {}

    def apply_insert(self, word: Word):

        self._on_word(word)

        if word.dependency == "nsubj":
            lemma = word.lemma.lower()
            self.referents[lemma] = self.referents.get(lemma, 0) + 1

    def apply_remove(self, word: Word):
        if word.dependency == "nsubj":
            lemma = word.lemma.lower()
            self.referents[lemma] -= 1
            if self.referents[lemma] == 0:
                del self.referents[lemma]

    def _on_word(self, word: Word):
        if word.dependency == "nsubj":
            lemma = word.lemma.lower()
            if lemma in self.referents:
                word.add_critic(Critic(
                    f"Repeated subject '{word.text}' in close proximity",
                    Critic.Severity.LOW,
                    Critic.Type.STYLE
                ))