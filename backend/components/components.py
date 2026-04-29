from typing import Generator
from spacy.tokens import Token, Span, Doc
from components.critic import Critic
from context.character import CharacterRegistry

class Component:
    def __init__(self, text: str):
        self.text = text.strip()
        self.critics: list[Critic] = []

    def add_critic(self, critic: Critic):
        self.critics.append(critic)

class Word(Component):
    def __init__(self,
                 text: str,
                 start: int = -1,
                 end: int = -1,
                 pos: str = "",
                 lemma: str = "",
                 dependency: str = "",
                 morph=None,
                 head_index: int = -1,
                 index: int = -1,
                 ent_type: str = ""):
        super().__init__(text)
        self.start = start
        self.end = end
        self.pos = pos
        self.lemma = lemma
        self.dependency = dependency
        self.morph = morph
        self.head_index = head_index
        self.index = index
        self.ent_type = ent_type
        self.char_ref: set[str] = set()

    @classmethod
    def from_token(cls, token: Token) -> "Word":
        return cls(
            text=token.text,
            start=token.idx,
            end=token.idx + len(token),
            pos=token.pos_,
            lemma=token.lemma_,
            dependency=token.dep_,
            morph=token.morph,
            head_index=token.head.i,
            index=token.i,
            ent_type=token.ent_type_
        )

    def get_tense(self):
        morph = self.morph
        if "Tense=Pres" in morph:
            return "present"
        if "Tense=Past" in morph:
            return "past"
        if "Tense=Fut" in morph:
            return "future"
        if "VerbForm=Inf" in morph:
            return "infinitive"
        return "unknown"

    def is_singular(self):
        return "Number=Sing" in self.morph

    def is_plural(self):
        return "Number=Plur" in self.morph

    def __str__(self):
        if self.critics:
            max_severity = max(c.severity.value for c in self.critics)
            return f"[(Severity: {max_severity})({', '.join(str(c) for c in self.critics)}){self.text}]"
        return self.text

class Sentence(Component):
    def __init__(self, text: str, start: int = -1, end: int = -1, words: list[Word] | None = None):
        super().__init__(text)
        self.start = start
        self.end = end
        self.words = words or []

    @classmethod
    def from_span(cls, span: Span) -> "Sentence":
        return cls(
            text=span.text,
            start=span.start_char,
            end=span.end_char,
            words=[Word.from_token(token) for token in span]
        )

    def __str__(self):
        parts = []
        for word in self.words:
            text = str(word)
            if word.pos == "PUNCT":
                if parts:
                    parts[-1] += text
                else:
                    parts.append(text)
            else:
                parts.append(text)
        sentence_str = " ".join(parts)
        if self.critics:
            max_severity = max(c.severity.value for c in self.critics)
            sentence_str = f"[(Severity: {max_severity})({', '.join(str(c) for c in self.critics)}) {sentence_str}]"
        return sentence_str

class Paragraph(Component):
    def __init__(self, text: str, start: int = -1, end: int = -1, sentences: list[Sentence] | None = None):
        super().__init__(text)
        self.start = start
        self.end = end
        self.sentences = sentences or []

    @classmethod
    def from_span(cls, span: Span) -> "Paragraph":
        return cls(
            text=span.text,
            start=span[0].idx if len(span) > 0 else -1,
            end=span[-1].idx + len(span[-1]) if len(span) > 0 else -1,
            sentences=[Sentence.from_span(sent) for sent in span.sents]
        )

    def __str__(self):
        string = " ".join(str(sentence) for sentence in self.sentences)
        if self.critics:
            max_severity = max(c.severity.value for c in self.critics)
            return f"[(Severity: {max_severity})({', '.join(str(c) for c in self.critics)}){string}]"
        return string

class Document:
    def __init__(self, text: str, nlp_model, char_registry: CharacterRegistry | None = None):
        self.doc: Doc = nlp_model(text)
        self.char_registry: CharacterRegistry = char_registry
        if char_registry:
            self._merge_character_spans()
        self.paragraphs: list[Paragraph] = []
        self._split_paragraphs()
        if char_registry:
            self._preprocess_characters()

    def _split_paragraphs(self):
        start = 0

        for i, token in enumerate(self.doc):
            if "\n" in token.text_with_ws:
                span = self.doc[start:i+1]
                self.paragraphs.append(Paragraph.from_span(span))
                start = i + 1

        if start < len(self.doc):
            self.paragraphs.append(Paragraph.from_span(self.doc[start:]))

    def _merge_character_spans(self):
        if not self.char_registry:
            return

        spans_to_merge = []

        for name in self.char_registry.get_names():
            spans = self._find_all_spans(name)
            spans_to_merge.extend(spans)

        with self.doc.retokenize() as retokenizer:
            for span in spans_to_merge:
                if span is not None and len(span) > 1:
                    retokenizer.merge(span)

    def _find_all_spans(self, phrase: str):
        phrase_tokens = phrase.lower().split()
        spans = []

        for i in range(len(self.doc) - len(phrase_tokens) + 1):
            window = self.doc[i:i + len(phrase_tokens)]

            if [t.text.lower() for t in window] == phrase_tokens:
                spans.append(window)

        return spans
    
    def _preprocess_characters(self):
        if not self.char_registry:
            return
        
        sentence_idx = -1

        for item_type, component in self.iter_words_with_context():

            if item_type == "SENT":
                sentence_idx += 1
                continue

            if item_type != "WORD":
                continue

            word: Word = component
            if self.char_registry._is_character(word.text):
                self.char_registry._encounter_character(word.text, sentence_idx)
                character = self.char_registry.get_character(word.text)
                word.char_ref.add(character.common_name)
            elif word.pos == "PRON":
                characters = self.char_registry.get_recent_characters_for_pronoun(word.text)
                for char in characters:
                    word.char_ref.add(char.common_name)
                         

    def iter_words_with_context(self) -> Generator[tuple[str, Component], None, None]:
        for paragraph in self.paragraphs:
            yield ("PARA", paragraph)

            for sentence in paragraph.sentences:
                yield ("SENT", sentence)

                for word in sentence.words:
                    yield ("WORD", word)
    
    def __str__(self):
        return "\n\n".join(str(paragraph) for paragraph in self.paragraphs)