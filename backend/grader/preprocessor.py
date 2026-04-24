from components.components import Document, Word
from context.character import CharacterRegistry


class Preprocessor:
    def __init__(self, char_registry: CharacterRegistry):
        self.char_registry = char_registry

    def preprocess(self, doc: "Document") -> None:
        items = list(doc.iter_words_with_context())

        self._forward_pass(items)
        # TODO: Implement backward pass
        #self._backward_pass(items)

    def _forward_pass(self, items):
        sentence_index = 0

        for item_type, component in items:

            if item_type == "SENT":
                sentence_index += 1
                continue

            if item_type != "WORD":
                continue

            w: Word = component
            if self.char_registry.is_character(w.text):
                self.char_registry.add_recent_encounter(w.text, sentence_index)
            elif w.pos == "PRON":
                characters = self.char_registry.get_recent_encounters(w.text, sentence_index)
                w.char_ref = set(char.common_name for char in characters)