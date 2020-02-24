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
    def __init__(self, z, x, y, image='./assets/NPCs/16x16DungeonCrate.png'):

        super().__init__(z, x, y)

        # This unit's health
        #self.health = 10000
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()

        #movement speed
        self.delta = 100

        #crate position
        self.x = x
        self.y = y

        #crate image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
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

    def move(self, direction):
        amount = self.delta * Updateable.gameDeltaTime * direction
        #pygame.mixer.Channel(3).play(pygame.mixer.Sound('assets/Music/Scrape Effects/scrape-2.wav'))

        try:
            if self.x + amount.x < 0:
                raise OffScreenLeftException            
            elif self.x + amount.x > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            elif self.y + amount.y < 0:
                raise OffScreenTopException
            elif self.y + amount.y > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.x += amount.x
                self.y += amount.y

        except:
            pass

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        #self.collisions = []
    
    def slowUpdate(self):
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
