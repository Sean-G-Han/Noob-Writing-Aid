import json

class Object:
    def __init__(self, common_name: str, adjectives: list[str], description: str):
        self.common_name = common_name
        self.adjectives = adjectives
        self.description = description
        #self.chapter_frame = chapter_frame