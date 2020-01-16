from .game_objects import DUGameObject

class Character(DUGameObject):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(z)

class Player(Character):
    def __init__(self):
        super().__init__()
    def update(self):
        pass

class NPC(Character):
    pass
