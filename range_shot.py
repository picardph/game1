from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
import pygame

class Ranged_Shot(Collidable):
    def __init__(self, z, x, y, image='./assets/right_shot.png', direction = "right"):

        super().__init__(z, x, y)

        # movement speed
        self.delta = 1000

        # crate position
        self.z = 0
        self.x = x
        self.y = y

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    def update(self):
        amount = self.delta * Updateable.gameDeltaTime
        if self.direction == "right":
            self.rect.x = self.rect.x + amount
        #self.collisions = []
        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    Collision(self, sprite)


    def onCollision(self, collision, direction):
      self.rect.x = -1
      self.rect.y = -1