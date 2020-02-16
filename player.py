from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
import pygame
from range_shot import Ranged_Shot


class Player(Character, Collidable):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, scene, z=0, x=0, y=0, image='assets/norris.png'):
        super().__init__(z, x, y)
        # This unit's health
        self.health = 100
        # Last time I was hit

        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 500
        # Where the player is positioned
        self.x = x
        self.y = y
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
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
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0,0,0))

        self.scene = scene

    def move_left(self):
        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
        except:
            pass

    def move_right(self):
        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
        except:
            pass

    def move_up(self):
        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
        except:
            pass

    def move_down(self):
        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
        except:
            pass

    def shoot_left(self):
        self.scene.addRanged(self.rect.x - self.rect.width, self.rect.centery, direction = "left")
        pass

    def shoot_right(self):
        self.scene.addRanged(self.rect.x, self.rect.centery)
        pass

    def shoot_up(self):
        self.scene.addRanged(self.rect.centerx, self.y - (self.rect.height), direction = "up")
        pass

    def shoot_down(self):
        self.scene.addRanged(self.rect.centerx, self.rect.y, direction = "down")
        pass

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    Collision(self, sprite)

    def onCollision(self, collision, direction):
       #Quick and dirty movement code to test collision.
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.move_right()
            elif direction.x < 0:
                self.move_left()
        else:
            if direction.y > 0:
                self.move_down()
            elif direction.y < 0:
                self.move_up() 
            else:
                print("Unknown Direction.")


    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now
