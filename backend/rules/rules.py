from components.components import Component, Word, Sentence, Paragraph

class Rule:
    def apply(self, Component: Component) -> bool:
        raise NotImplementedError

class WordRule(Rule):
    def apply(self, word: Word) -> bool:
        raise NotImplementedError

class SentenceRule(Rule):
    def apply(self, sentence: Sentence) -> bool:
        raise NotImplementedError

class ParagraphRule(Rule):
    def apply(self, paragraph: Paragraph) -> bool:
        raise NotImplementedError
    
class WindowRule():
    def apply_insert(self, new_word: Word) -> None:
        raise NotImplementedError
    
    def apply_remove(self, old_word: Word) -> None:
        raise NotImplementedError