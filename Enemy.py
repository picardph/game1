

from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
from pygame import Vector3
import pygame
from range_shot import Ranged_Shot


class Enemy(Character, Collidable):
    """
    """

    def __init__(self, scene, *args, image='assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f0.png'):
        
        super().__init__(args)
        # This unit's health
        self.health = 100

        # This unit's max health
        self.maxHealth = 100

        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()

        # Last time I attacked
        self.last_shot = pygame.time.get_ticks()

        # A unit-less value.  Bigger is faster.
        self.delta = 200

        # The direction the player is facing. Should be a unit vector.
        self.direction = Vector3(0, 0, 0)

        self.attackDirection = Vector3(0, 0, 0)


        # flag to tell us if we need to flip image or not
        self.setFlip = False

        # flag to tell us if player is moving
        self.isMoving = False
        self.isAttacking = False
        self.usingMelee = False
        self.idleImages = []

        self.soundEffects = []
        self.soundEffects.append('assets/Music/Movement/footsteps/step_metal (3).ogg')
        self.soundEffects.append('assets/Combat/Socapex - hurt.wav')
        self.soundEffects.append('assets/Combat/105016__julien-matthey__jm-fx-fireball-01.wav')
        self.soundEffects.append('assets/Combat/heavy_sword.wav')

        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f0.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f1.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f2.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f3.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f4.png')
        self.idleImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f5.png')

        self.runImages = []

        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f0.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f1.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f2.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f3.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f4.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f5.png')

        self.index = 0
        self.image = self.idleImages[self.index]
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

        # How big the world is, so we can check for boundaries
        self.world_size = (Settings.width, Settings.height)
        
        # What sprites am I not allowed to cross?
        self.blocks = pygame.sprite.Group()

        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_rect
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()
        
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0, 0, 0))

        self.scene = scene

    def move(self, direction):
        amount = self.delta * Updateable.gameDeltaTime * direction
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

            pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.soundEffects[0]))

        except:
            pass

    def shoot(self, direction:Vector3):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 250:
            self.scene.addRanged(self.rect.centerx, self.rect.centery, direction, melee =self.usingMelee)
            if self.usingMelee:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(self.soundEffects[3]))
            else:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(self.soundEffects[2]))
            self.last_shot = now

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.index = (self.index + 1) % len(self.idleImages)

        #If player's direction is not 0, 0, 0, player is moving.
        if self.direction != Vector3(0,0,0):
            self.isMoving = True
            self.move(self.direction)
        else:
            self.isMoving = False

        # If the player's attackDirection is not 0, 0, 0, player is attacking.
        if self.attackDirection != Vector3(0,0,0):
            self.isAttacking = True
            self.shoot(self.attackDirection)
        else:
            self.isAttacking = False

        #Load animations based on movement state.
        if self.isMoving == False:
            self.image = pygame.image.load(self.idleImages[self.index]).convert_alpha()
        else:
            self.image = pygame.image.load(self.runImages[self.index]).convert_alpha()

        if self.setFlip == True:
            self.image = pygame.transform.flip(self.image, True, False)

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

        if collision.getOther(self):
            self.ouch()


    def ouch(self):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.soundEffects[1]))

        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now
            self.scene.overlay.healthChange()
            if self.health <= 0:
                self.onDeath
                
    def heal(self, amount):
        if amount <= 0:
            pass
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        self.scene.overlay.healthChange()

    def onDeath(self):
        #TODO handle enemy death.
        pass

    def swap_weapons(self):
        self.usingMelee = not self.usingMelee