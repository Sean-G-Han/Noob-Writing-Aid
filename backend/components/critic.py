from enum import Enum

class Critic:
    class Severity(Enum):
        COMMENT = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
    
    class Level(Enum):
        WORD = 1
        SENTENCE = 2
        PARAGRAPH = 3
    
    class Type(Enum):
        GRAMMAR = 1
        STYLE = 2
        CLARITY = 3
        SPELLING = 4
        OTHER = 5

    def __init__(self, message: str, 
                 severity: "Critic.Severity" = Severity.MEDIUM,
                 type: "Critic.Type" = Type.OTHER,):
        self.message = message
        self.severity = severity
        self.type = type
    
    def __str__(self):
        return f"{self.type.name}: {self.message}"
