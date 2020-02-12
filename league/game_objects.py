import abc
import pygame
from .settings import Settings

class GameObject(abc.ABC):
    """Any object that makes up our game world."""
    pass

class Drawable(pygame.sprite.Sprite):
    """Creates a drawable.  For us, a drawable is a pygame Sprite object."""
    def __init__(self, layer=0, x=0, y=0):
        super().__init__()
        self._layer = layer
        self.image = None
        self.rect = pygame.Rect(0, 0, Settings.tile_size, Settings.tile_size)
        self.x = x
        self.y = y


class Updateable(abc.ABC):
    """An interface that ensures an object has an update(gameDeltaTime) method."""
    #TODO Add gameDeltaTime as a static class variable.
    gameDeltaTime=None
    @abc.abstractmethod
    def update():
        pass

class UGameObject(GameObject, Updateable):
    """A game object that is updateable but not drawn."""
    pass

class DGameObject(GameObject, Drawable):
    """A game object that is drawable, but not updateable.  A static object."""
    pass

class DUGameObject(UGameObject, Drawable):
    """A game object that is updateable and drawable."""
    pass
