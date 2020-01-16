from .game_objects import DUGameObject
import pygame

class OffScreenException(Exception):
    pass

class OffScreenLeftException(OffScreenException):
    pass

class OffScreenRightException(OffScreenException):
    pass

class OffScreenTopException(OffScreenException):
    pass

class OffScreenBottomException(OffScreenException):
    pass

class Character(DUGameObject):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(z)
        self.rect.x = x
        self.rect.y = y
        self.events = {}

    def update(self, time):
        for group in self.groups():
            collisions = pygame.sprite.spritecollide(self, group)
            for sprite in collisions:
                if sprite in self.events.keys():
                    self.events[sprite]()

class Player(Character):
    def __init__(self, x, y, z=0):
        super().__init__(x, y, z)

class NPC(Character):
    pass
