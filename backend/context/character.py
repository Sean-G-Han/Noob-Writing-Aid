from context.object import Object
from nlp import add_character_pattern, get_nlp_model


class CharacterRegistry:

    MALE_PRONOUNS = {"he", "him", "his"}
    FEMALE_PRONOUNS = {"she", "her", "hers"}
    NEUTRAL_PRONOUNS = {"it", "its"}
    ALL_PRONOUNS = MALE_PRONOUNS | FEMALE_PRONOUNS | NEUTRAL_PRONOUNS

    def __init__(self):
        self.characters: dict[str, Character] = {}
        self.pronoun_map: dict[str, set[Character]] = {}
        self.recent_encounter: dict[str, list[tuple[int, Character]]] = {}

    def create_character(self,
                         common_name: str,
                         adjectives: set[str] | None = None,
                         description: str = "",
                         pronouns: set[str] | None = None,
                         alternative_names: set[str] | None = None) -> "Character":

        char_names = {common_name.lower()}
        if alternative_names:
            char_names |= {name.lower() for name in alternative_names}

        existing_names = set(self.characters.keys())

        if char_names & existing_names:
            raise ValueError(
                f"Character with name(s) {char_names & existing_names} already exists."
            )

        char = Character(
            common_name=common_name,
            adjectives=adjectives,
            description=description,
            pronouns=pronouns,
            alternative_names=alternative_names
        )

        self._register(char)
        return char

    def _register(self, character: "Character"):
        for name in character.names:
            self.characters[name] = character
            add_character_pattern(get_nlp_model(), name)

        for p in character.pronouns:
            if p not in self.pronoun_map:
                self.pronoun_map[p] = set()
            self.pronoun_map[p].add(character)
    
    def add_recent_encounter(self, name: str, sentence_index: int):
        char = self.characters.get(name.lower())
        if not char:
            return

        for p in char.pronouns:
            self.recent_encounter.setdefault(p, [])
            self.recent_encounter[p].append((sentence_index, char))

    def get_recent_encounters(self,
                              pronoun: str,
                              sentence_index: int) -> set["Character"]:
                            # Sentence index might be used later IDK
        stack = self.recent_encounter.get(pronoun.lower(), [])

        if not stack:
            return set()

        result = set()
        target_sentence = None

        for s, char in reversed(stack):
            if target_sentence is None:
                target_sentence = s

            if s != target_sentence:
                break

            result.add(char)

        return result

    def is_character(self, name: str) -> bool:
        return name.lower() in self.characters

    def get_character(self, name: str) -> "Character":
        return self.characters.get(name.lower())

    def to_dict(self) -> dict:
        seen = set()
        characters = []

        for char in self.characters.values():
            if char.common_name not in seen:
                seen.add(char.common_name)
                characters.append(char.to_dict())

        return {"characters": characters}

    @staticmethod
    def from_dict(data: dict) -> "CharacterRegistry":
        registry = CharacterRegistry()

        for char_data in data["characters"]:
            registry.create_character(
                common_name=char_data["common_name"],
                adjectives=set(char_data.get("adjectives", [])),
                description=char_data.get("description", ""),
                pronouns=set(char_data.get("pronouns", [])),
                alternative_names=set(char_data.get("alternative_names", []))
            )

        return registry

    def __repr__(self):
        return f"CharacterRegistry({list(self.characters.keys())})"


class Character(Object):
    def __init__(self,
                 common_name: str,
                 adjectives: set[str] | None = None,
                 description: str = "",
                 pronouns: set[str] | None = None,
                 alternative_names: set[str] | None = None):
        super().__init__(
            common_name,
            set(adjectives or []),
            description
        )

        self.pronouns: set[str] = {p.lower() for p in (pronouns or [])}
        self.alternative_names: set[str] = {
            n.lower() for n in (alternative_names or [])
        }

    @property
    def names(self) -> set[str]:
        return {self.common_name.lower()} | self.alternative_names

    def to_dict(self) -> dict:
        return {
            "common_name": self.common_name,
            "adjectives": list(self.adjectives),
            "description": self.description,
            "pronouns": list(self.pronouns),
            "alternative_names": list(self.alternative_names),
        }

    @staticmethod
    def from_dict(data: dict) -> "Character":
        return Character(
            common_name=data["common_name"],
            adjectives=set(data.get("adjectives", [])),
            description=data.get("description", ""),
            pronouns=set(data.get("pronouns", [])),
            alternative_names=set(data.get("alternative_names", []))
        )

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False

        return (
            self.common_name == other.common_name and
            self.description == other.description and
            self.adjectives == other.adjectives and
            self.pronouns == other.pronouns and
            self.alternative_names == other.alternative_names
        )
    
    def __hash__(self):
        return hash((
            self.common_name,
            self.description,
            frozenset(self.adjectives), #YH Note Sets are not hashable as it is still mutable
            frozenset(self.pronouns),
            frozenset(self.alternative_names),
        ))

    def __repr__(self):
        return f"Character({self.common_name})"