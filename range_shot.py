from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
import pygame
from NPC_crate import Crate

class Ranged_Shot(Collidable):
    def __init__(self, z, x, y, scene, direction = "right", melee = False):

        super().__init__(z, x, y)

        # movement speed
        self.delta = 1000

        # crate position
        self.z = 0
        self.x = x
        self.y = y
        self.image = None
        self.melee = melee
        self.maxRange = 0
        self.moved = 0

        if melee:
            self.maxRange = 200
            self.delta = 500
            if direction == "right":
                self.image = pygame.image.load('./assets/right_slash.png').convert_alpha()
            elif direction == "down":
                self.image = pygame.image.load('./assets/down_slash.png').convert_alpha()
            elif direction == "up":
                self.image = pygame.image.load('./assets/up_slash.png').convert_alpha()
            else:
                self.image = pygame.image.load('./assets/left_slash.png').convert_alpha()
        else:
            if direction == "right":
                self.image = pygame.image.load('./assets/right_shot.png').convert_alpha()
            elif direction == "down":
                self.image = pygame.image.load('./assets/down_shot.png').convert_alpha()
            elif direction == "up":
                self.image = pygame.image.load('./assets/up_shot.png').convert_alpha()
            else:
                self.image = pygame.image.load('./assets/left_shot.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Correct for the size of the projectile to make the bullet more centered from the player's position
        if direction == "right" or direction == "left":
            self.rect.y = self.rect.y - (self.rect.height / 2)
            self.y = self.rect.y
        else:
           self.rect.x = self.rect.x - (self.rect.width / 2)
           self.x = self.rect.x

        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowed to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []

        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

        self.direction = direction
        self.scene = scene
        self.beenDeleted = False

    def update(self):
        amount = self.delta * Updateable.gameDeltaTime
        if self.melee:
            self.moved += amount
            if self.moved >= self.maxRange:
                self.scene.despawnObject(self)
                return
        try:
            if self.direction == "right":
                self.x = self.x + amount
                self.rect.x = self.x
                if self.x > self.world_size[0] - Settings.tile_size:
                   raise OffScreenException
            elif self.direction == "left":
                self.x = self.x - amount
                self.rect.x = self.x
                if self.x < 0:
                    raise OffScreenException
            elif self.direction == "down":
               self.y = self.y + amount
               self.rect.y = self.y
               if self.y > self.world_size[1] - Settings.tile_size:
                    raise OffScreenException
            elif self.direction == "up":
                self.y = self.y - amount
                self.rect.y = self.y
                if self.y < 0:
                    raise OffScreenException
        except:
            self.scene.despawnObject(self)
            self.beenDeleted = True
            pass

        self.collisions = []
        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    if type(sprite) is not Crate:
                        Collision(self, sprite)
                    else:
                        self.scene.despawnObject(self)


    def onCollision(self, collision, direction):
        try:
          self.scene.despawnObject(self)
        except:
            pass