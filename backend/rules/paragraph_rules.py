from rules.rules import ParagraphRule
from components.components import Sentence, Paragraph
from components.critic import Critic

class SentenceStartRepetitionRule(ParagraphRule):
    def apply(self, paragraph: Paragraph)-> bool:
        if len(paragraph.sentences) < 2:
            return False
        issue_found = False
        groups: dict[str, list[Sentence]] = {}

        for sentence in paragraph.sentences:
            if not sentence.words:
                continue

            first_word = sentence.words[0]

            key = first_word.text.lower()

            if key not in groups:
                groups[key] = []
            groups[key].append(sentence)

        for sentences in groups.values():
            if len(sentences) > 1:
                issue_found = True
                critic = Critic(
                    "Repeated start to sentence",
                    Critic.Severity.MEDIUM,
                    Critic.Type.STYLE
                )
                for sentence in sentences:
                    sentence.words[0].add_critic(critic)
        return issue_found

class MonotonousLengthRule(ParagraphRule):
    def apply(self, paragraph: Paragraph) -> bool:
        if len(paragraph.sentences) < 3:
            return False
        issue_found = False
        lengths = [len(s.words) for s in paragraph.sentences]
        for i in range(len(lengths) - 2):
            if abs(lengths[i] - lengths[i+1]) <= 3 and abs(lengths[i+1] - lengths[i+2]) <= 3:
                issue_found = True
                paragraph.sentences[i+2].add_critic(Critic(
                        "Sentence lengths are too similar. Vary them to improve flow", 
                        Critic.Severity.LOW,
                        Critic.Type.STYLE
                    )
                )
        return issue_found