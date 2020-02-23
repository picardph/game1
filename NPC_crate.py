# Class for interactable crates in the game
# Ideally when the player collides with a crate
# it will move 1 tile in the direction of the player's movement.

#from league import *
from league.constants import Direction
from league import Settings
from league import Character
from league.game_objects import Drawable
from league.game_objects import Updateable
import pygame
from collision import Collision, Collidable


class Crate(Character, Collidable):
    def __init__(self, *args):
        super().__init__(args)
        self.idleImages.append('./assets/NPCs/16x16DungeonCrate.png')
        self.maxHealth = 1000000
        self.health = 1000000

    def update(self):
        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    Collision(self, sprite)

    def onCollision(self, collision, direction):
        if(abs(direction.x) > abs(direction.y)):
            direction.y = 0
        else:
            direction.x = 0
        self.move(direction.normalize())
