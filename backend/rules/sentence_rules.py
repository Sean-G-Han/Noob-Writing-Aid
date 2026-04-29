from rules.rules import SentenceRule
from components.components import Word, Sentence
from components.critic import Critic

class RepeatedWordRule(SentenceRule):
    def apply(self, sentence: Sentence) -> bool:
        issue_found = False
        if len(sentence.words) < 2:
            return False
        
        prev_word: Word = None

        for word in sentence.words:
            if word.pos in {"PUNCT", "SPACE"}:
                continue
            if prev_word != None and word.text.lower() == prev_word.text.lower():
                issue_found = True
                word.add_critic(Critic(f"Repeated word", Critic.Severity.LOW, Critic.Type.STYLE))
            else:
                prev_word = word
        return issue_found

class ToBeAdjectiveRule(SentenceRule):
    def apply(self, sentence: Sentence) -> bool:
        be_verbs = {"be", "is", "am", "are", "was", "were", "been", "being"}
        issue_found = False
        for i, word in enumerate(sentence.words):
            if word.lemma.lower() not in be_verbs:
                continue

            for neighbor in sentence.words[i+1 : i+3]:
                if neighbor.pos == "ADJ":
                    issue_found = True
                    neighbor.add_critic(Critic(
                        "This is a passive description. Can you use an active verb instead?", 
                        Critic.Severity.LOW,
                        Critic.Type.STYLE
                    ))
        return issue_found


def get_subject(sentence: Sentence, word: Word) -> Word:
    return next((w for w in sentence.words if w.dependency == "nsubj" and w.head_index == word.index), None)

class PresentSVARule(SentenceRule):
    def apply(self, sentence: Sentence) -> bool:
        issue_found = False
        for word in sentence.words:
            if (word.pos not in {"VERB", "AUX"} or "VerbForm=Fin" not in str(word.morph) or "Tense=Pres" not in str(word.morph)):
                continue
                
            subject = get_subject(sentence, word)
            if not subject:
                continue

            if subject.is_singular() != word.is_singular():
                issue_found = True
                msg = f"'{subject.text}' requires the {'singular' if subject.is_singular() else 'plural'} form of '{word.text}'"
                critic = Critic(msg, Critic.Severity.HIGH, Critic.Type.GRAMMAR)
                word.add_critic(critic)
        return issue_found

class PastToBeSVARule(SentenceRule):
    def apply(self, sentence: Sentence)-> bool:
        issue_found = False
        for word in sentence.words:
            if word.lemma.lower() != "be" or "Tense=Past" not in str(word.morph):
                continue

            subject = get_subject(sentence, word)
            if not subject: 
                continue

            if subject.is_singular() != word.is_singular():
                issue_found = True
                msg = f"In the past tense, '{subject.text}' should use '{'was' if subject.is_singular() else 'were'}'"
                critic = Critic(msg, Critic.Severity.HIGH, Critic.Type.GRAMMAR)
                word.add_critic(critic)
        return issue_found

class PerfectTenseSVARule(SentenceRule):
    def apply(self, sentence: Sentence)-> bool:
        issue_found = False
        for word in sentence.words:
            if word.lemma.lower() != "have" or word.dependency != "aux":
                continue

            subject = get_subject(sentence, word)
            if not subject: 
                continue

            if subject.is_singular() and word.text.lower() == "have":
                issue_found = True
                critic = Critic("Use 'has' for singular subjects", Critic.Severity.HIGH, Critic.Type.GRAMMAR)
                subject.add_critic(critic)
                word.add_critic(critic)

            elif subject.is_plural() and word.text.lower() == "has":
                issue_found = True
                critic = Critic("Use 'have' for plural subjects", Critic.Severity.HIGH, Critic.Type.GRAMMAR)
                subject.add_critic(critic)
                word.add_critic(critic)
        return issue_found

class InconsistentTenseRule(SentenceRule):
    def apply(self, sentence: Sentence)-> bool:
        issue_found = False
        finite_verbs = [
            w for w in sentence.words 
            if w.pos == "VERB" 
            and "VerbForm=Fin" in str(w.morph)
        ]

        found_tenses = {v.get_tense() for v in finite_verbs}

        if len(found_tenses) > 1:
            tense_list = ", ".join(found_tenses)
            issue_found = True
            sentence.add_critic(Critic(
                f"Inconsistent tenses: {tense_list}",
                Critic.Severity.COMMENT,
                Critic.Type.GRAMMAR
            ))

            for verb in finite_verbs:
                verb.add_critic(Critic(
                    f"Verb '{verb.text}' is {verb.get_tense()} in a sentence with tenses: {tense_list}",
                    Critic.Severity.LOW,
                    Critic.Type.GRAMMAR
                ))
        return issue_found

class DeterminerRule(SentenceRule):
    def apply(self, sentence: Sentence) -> bool:
        issue_found = False
        vowels = {'a', 'e', 'i', 'o', 'u'}
        for i in range(len(sentence.words) - 1):
            curr = sentence.words[i]
            nxt = sentence.words[i+1]
            if curr.lemma.lower() == "a" and nxt.text[0].lower() in vowels:
                issue_found = True
                curr.add_critic(Critic(
                    "Wrong use of 'a'",
                    Critic.Severity.MEDIUM,
                    Critic.Type.GRAMMAR
                ))
            elif curr.lemma.lower() == "an" and nxt.text[0].lower() not in vowels:
                issue_found = True
                curr.add_critic(Critic(
                    "Wrong use of 'an'",
                    Critic.Severity.MEDIUM,
                    Critic.Type.GRAMMAR
                ))
        return issue_found

class DoubleNegativeRule(SentenceRule):
    def apply(self, sentence: Sentence)-> bool:
        issue_found = False
        negation_words = {"n’t", "n't"}
        negs = [word for word in sentence.words if word.text.lower() in negation_words or word.dependency == "neg"]
        
        if len(negs) < 2:
            return
        
        for neg in negs:
            issue_found = True
            neg.add_critic(Critic(
                "Double negative detected. Consider rephrasing", 
                Critic.Severity.MEDIUM,
                Critic.Type.CLARITY
            ))
        return issue_found

class SentenceFragmentRule(SentenceRule):
    def apply(self, sentence: Sentence)-> bool:
        issue_found = False
        if len(sentence.words) < 3:
            return

        has_verb = any(word.pos in {"VERB", "AUX"} for word in sentence.words)
        
        if not has_verb:
            issue_found = True
            sentence.add_critic(Critic(
                "Sentence fragment. Seems to be missing a verb",
                Critic.Severity.HIGH,
                Critic.Type.GRAMMAR
            ))
        return issue_found

class WordEchoRule(SentenceRule):
    def apply(self, sentence: Sentence)-> bool:
        issue_found = False
        seen_words = {}
        ignore_list = {"the", "and", "is", "has", "that", "with"}
        
        for word in sentence.words:
            issue_found = False
            low_word = word.lemma.lower()
            if word.pos in {"NOUN", "VERB", "ADJ"} and low_word not in ignore_list:
                if low_word in seen_words:
                    word.add_critic(Critic(
                            f"Multiple instance of '{word.text}' in same sentence", 
                            Critic.Severity.LOW,
                            Critic.Type.STYLE
                        )
                    )
        return issue_found