from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
import pygame
from pygame import Vector3
from NPC_crate import Crate

class Ranged_Shot(Collidable):
    def __init__(self, z, x, y, scene, direction:Vector3, melee = False):

        super().__init__(z, x, y)

        # crate position
        self.z = 0
        self.x = x
        self.y = y
        self.image = None
        self.melee = melee
        self.maxRange = 0
        self.moved = 0
        self.direction = direction
        self.delta = self.direction * 750
        self.offset = 16

        if melee:
            self.maxRange = 50
            self.delta *= 0.25
        
        self.imageSelect()

        self.rect = self.image.get_rect()
        self.calcOffset()
        
        self.rect.x = x
        self.rect.y = y

        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowed to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle

        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

        self.scene = scene
        self.beenDeleted = False

    def update(self):
        amount = self.delta * Updateable.gameDeltaTime
        if self.melee:
            self.moved += amount.magnitude()
            if self.moved >= self.maxRange:
                self.scene.despawnObject(self)
                return
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
            self.scene.despawnObject(self)
            self.beenDeleted = True
            return

        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    if type(sprite) is not Crate:
                        Collision(self, sprite)
                    else:
                        self.scene.despawnObject(self)
        self.rect.x = self.x
        self.rect.y = self.y

    def calcOffset(self):
        # Method to set initial offset of projectile.
        if self.direction.x != 0:
            self.y -= self.rect.height / 2
        if self.direction.y != 0:
            self.x -= self.rect.width / 2
        self.x += self.offset * self.direction.x
        self.y += self.offset * self.direction.y


    def onCollision(self, collision, direction):
        try:
          self.scene.despawnObject(self)
        except:
            pass

    def imageSelect(self):
        if self.melee:
            self.image = pygame.image.load('./assets/right_slash.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 64))
        else:
            self.image = pygame.image.load('./assets/right_shot.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (32,16))

        self.image = pygame.transform.rotate(self.image, Vector3(1,0,0).angle_to(self.direction))
        if self.direction.y == 1:
            self.image = pygame.transform.flip(self.image, False, True)