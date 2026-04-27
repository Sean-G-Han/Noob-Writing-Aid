from context.object import Object

class PronounEncounter:
    def __init__(self):
        self.sentence_index: int | None = None
        self.characters: list["Character"] = []

    def add(self, sentence_index: int, character: "Character"):
        if self.sentence_index != sentence_index:
            self.sentence_index = sentence_index
            self.characters.clear()

        self.characters.append(character)

    def get_characters(self) -> list["Character"]:
        return self.characters

    def is_ambiguous(self) -> bool:
        return len(self.characters) > 1

class CharacterRegistry:
    def __init__(self):
        self.name_to_characters_map: dict[str, "Character"] = {}
        self.pronoun_to_characters_map: dict[str, set["Character"]] = {}
        self.recent_encounter: dict[str, PronounEncounter] = {}
    
    def register(self, character: "Character"):
        for name in character.names:
            self.name_to_characters_map[name.lower()] = character

        for pronoun in character.pronouns:
            self.pronoun_to_characters_map.setdefault(pronoun, set()).add(character)

    def get_names(self) -> list[str]:
        return list(self.name_to_characters_map.keys())
    
    def _is_character(self, text: str) -> bool:
        return text.lower() in self.name_to_characters_map
    
    def get_character(self, name: str) -> "Character":
        return self.name_to_characters_map.get(name.lower())
    
    def get_recent_characters_for_pronoun(self, pronoun: str) -> list["Character"]:
        encounter = self.recent_encounter.get(pronoun.lower())
        return encounter.get_characters() if encounter else []
    
    def _encounter_character(self, name: str, sentence_index: int) -> None:
        character = self.name_to_characters_map.get(name.lower())
        if not character:
            return

        for pronoun in character.pronouns:
            encounter = self.recent_encounter.setdefault(pronoun, PronounEncounter())
            encounter.add(sentence_index, character)

    def _is_ambiguous_pronoun(self, pronoun: str) -> bool:
        encounter = self.recent_encounter.get(pronoun.lower())
        return encounter.is_ambiguous() if encounter else False

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