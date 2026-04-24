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
                         adjectives: list[str] | None = None,
                         description: str = "",
                         pronouns: list[str] | None = None,
                         alternative_names: list[str] | None = None) -> "Character":

        char_names = set(common_name.lower())
        if alternative_names:
            char_names.add(name.lower() for name in alternative_names)
        
        all_names = set(self.characters.keys())
        
        if char_names & all_names:
            raise ValueError(f"Character with name(s) {char_names & all_names} already exists.")

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
        print(f"Try adding recent encounter for name '{name}' at sentence {sentence_index}")    
        char = self.characters.get(name.lower(), None)
        print(f"Found character: {char}")
        if not char:
            return

        for p in char.pronouns:
            self.recent_encounter.setdefault(p, [])
            self.recent_encounter[p].append((sentence_index, char))
    
    def get_recent_encounters(self,
                              pronoun: str,
                              sentence_index: int) -> set["Character"]:

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

        print(f"Returning recent encounters for pronoun '{pronoun}' at sentence {sentence_index}: {result}")
        return result
    
    def is_character(self, name: str) -> bool:
        return name.lower() in self.characters
    
    def get_character(self, name: str) -> "Character":
        return self.characters.get(name.lower(), None)
    
    def to_dict(self) -> dict:
        seen = set()
        characters = []

        for char in self.characters.values():
            if char.common_name not in seen:
                seen.add(char.common_name)
                characters.append(char.to_dict())

        return {
            "characters": characters
        }
    
    @staticmethod
    def from_dict(data: dict) -> "CharacterRegistry":
        registry = CharacterRegistry()

        for char_data in data["characters"]:
            registry.create_character(
                common_name=char_data["common_name"],
                adjectives=char_data["adjectives"],
                description=char_data.get("description", ""),
                pronouns=set(char_data.get("pronouns", [])),
                alternative_names=char_data.get("alternative_names", [])
            )

        return registry
    
    def __repr__(self):
        return f"CharacterRegistry({list(self.characters.keys())})" 
    
class Character(Object):
    def __init__(self, common_name: str, adjectives: list[str], description: str = "", pronouns: set[str] = [], alternative_names: list[str] = []):
        super().__init__(common_name, adjectives, description)
        self.pronouns = pronouns
        self.alternative_names = alternative_names
    
    @property
    def names(self) -> list[str]:
        names = [self.common_name.lower()]
        if self.alternative_names:
            names.extend(name.lower() for name in self.alternative_names)
        return names
    
    def to_dict(self) -> dict:
        return {
            "common_name": self.common_name,
            "adjectives": self.adjectives,
            "description": self.description,
            "pronouns": list(self.pronouns),
            "alternative_names": self.alternative_names,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Character":
        return Character(
            common_name=data["common_name"],
            adjectives=data["adjectives"],
            description=data["description"],
            pronouns=data["pronouns"],
            alternative_names=data["alternative_names"]
        )
    
    def __repr__(self):
        return f"Character({self.common_name})"