

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

    def __init__(self, scene, *args,
                 image='assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f0.png'):

        super().__init__(args)
        # This unit's health
        self.health = 100
        # Last time I was hit

        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 100

        # flag to tell us if we need to flip image or not
        self.setFlip = False

        # flag to tell us if player is moving
        self.isMoving = False

        self.idleImages = []

        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f0.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f1.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f2.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f3.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f4.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f5.png')

        self.runImages = []

        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f0.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f1.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f2.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f3.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f4.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f5.png')

        self.index = 0
        self.image = self.idleImages[self.index]
        self.image = pygame.image.load(image).convert_alpha()
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
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0, 0, 0))

        self.scene = scene

    def move_left(self):
        self.setFlip = True
        self.isMoving = True
        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
                self.isMoving = False

        except:
            pass

    def move_right(self):
        self.setFlip = False
        self.isMoving = True

        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
                self.isMoving = False

        except:
            pass

    def move_up(self):
        self.isMoving = True

        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
                self.isMoving = False

        except:
            pass

    def move_down(self):
        self.isMoving = True
        amount = self.delta * Updateable.gameDeltaTime
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                self.isMoving = False
        except:
            pass

    def shoot_left(self):
        self.scene.addRanged(self.rect.x - self.rect.width, self.rect.centery, direction="left")
        pass

    def shoot_right(self):
        self.scene.addRanged(self.rect.x, self.rect.centery)
        pass

    def shoot_up(self):
        self.scene.addRanged(self.rect.centerx, self.y - (self.rect.height), direction="up")
        pass

    def shoot_down(self):
        self.scene.addRanged(self.rect.centerx, self.rect.y, direction="down")
        pass

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.index = (self.index + 1) % len(self.idleImages)
        if self.isMoving == False:
            self.image = pygame.image.load(self.idleImages[self.index]).convert_alpha()
        elif self.isMoving == True:
            self.image = pygame.image.load(self.runImages[self.index]).convert_alpha()
            self.isMoving = False

        self.image = pygame.transform.scale(self.image, (32, 32))
        if self.setFlip == True:
            self.image = pygame.transform.flip(self.image, True, False)

        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    Collision(self, sprite)

    def onCollision(self, collision, direction):
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