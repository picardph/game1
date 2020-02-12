# Class for interactable crates in the game
# Ideally when the player collides with a crate
# it will move 1 tile in the direction of the player's movement.

#from league import *
from league.constants import Direction
from league import Settings
from league import Character
from league.game_objects import Drawable
import pygame
from collision import Collision, Collidable

class Crate(Character, Collidable):
    def __init__(self, z, x, y, image='./assets/NPCs/large_box.png'):

        super().__init__(z, x, y)

        # This unit's health
        #self.health = 10000
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        self.time = 0
        #movement speed
        self.delta = 100

        #crate position
        self.x = x
        self.y = y

        #crate image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

        # How big the world is, so we can check for boundaries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowed to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []

        # For collision detection, we need to compare our sprite
        # with collideable sprites.  However, we have to remap
        # the collideable sprites coordinates since they change.
        # For performance reasons I created this sprite so we
        # don't have to create more memory each iteration of
        # collision detection.
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

    def move_left(self):
        self.collisions = []
        amount = self.delta * self.time
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.x = self.x + amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def move_right(self):
        self.collisions = []
        amount = self.delta * self.time
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.x = self.x - amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def move_up(self):
        self.collisions = []
        amount = self.delta * self.time
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def move_down(self):
        amount = self.delta * self.time
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def update(self, time):
#THis is probably terrible but I;m not sure how else to go about it.
        self.time = time

        self.rect.x = self.x
        self.rect.y = self.y
        #self.collisions = []
        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    Collision(self, sprite)
        

    def onCollision(self, collision, direction):
        #Quick and dirty movement code to test collision.
        if direction is Direction.EAST:
            self.move_right()
        elif direction is Direction.WEST:
            self.move_left()
        elif direction is Direction.SOUTH:
            self.move_down()
        else:
            self.move_up()
