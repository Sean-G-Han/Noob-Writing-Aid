from components.components import Component, Word, Sentence, Paragraph

class Rule:
    def apply(self, Component: Component) -> None:
        pass

class WordRule(Rule):
    def apply(self, word: Word) -> None:
        raise NotImplementedError

class SentenceRule(Rule):
    def apply(self, sentence: Sentence) -> None:
        raise NotImplementedError

class ParagraphRule(Rule):
    def apply(self, paragraph: Paragraph) -> None:
        raise NotImplementedError
    
class WindowRule():
    def apply_insert(self, new_word: Word) -> None:
        raise NotImplementedError
    
    def apply_remove(self, old_word: Word) -> None:
        raise NotImplementedError