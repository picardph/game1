from .game_objects import DUGameObject
from .game_objects import Drawable
from .game_objects import Updateable
from league import Settings
import pygame
from pygame import Vector3

class OffScreenException(Exception):
    pass

class OffScreenLeftException(OffScreenException):
    pass

class OffScreenRightException(OffScreenException):
    pass

class OffScreenTopException(OffScreenException):
    pass

class OffScreenBottomException(OffScreenException):
    pass

class Character(DUGameObject):
    """Represents an updateable, drawable sprite object that
    can respond to collisions and events.  For collision events
    add the sprite and the function to call when the sprite
    and this object collide.
    """
    def __init__(self, scene, z=0, x=0, y=0, image='./assets/NPCs/16x16DungeonCrate.png', health = 100, meleeDmg = 50, rangedDmg = 20, speed = 200, atkDelay=250, hurtDelay=1000):
        super().__init__(z, x, y)
        
        # This unit's health
        self.health = 100

        # This unit's max health
        self.maxHealth = 100

        # Damage values
        self.meleeDmg = 50
        self.rangedDmg = 20

        # Minimum number of ticks between attacks.
        self.atkDelay = atkDelay

        # Minimum number of ticks between being damaged.
        self.hurtDelay = hurtDelay

        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()

        # Last time I attacked
        self.last_shot = pygame.time.get_ticks()

        # A unit-less value.  Bigger is faster.
        self.speed = speed

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
        self.runImages = []
        self.soundEffects = []

        self.index = 0
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

        # How big the world is, so we can check for boundaries
        self.world_size = (Settings.width, Settings.height)
        

        #TODO Move to Collidable
        # What sprites am I not allowed to cross?
        self.blocks = pygame.sprite.Group()

        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_rect
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

        self.scene = scene
        
    def move(self, direction):

        amount = self.speed * Updateable.gameDeltaTime * direction
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

            damage = self.meleeDmg if self.usingMelee else self.rangedDmg
            self.scene.addRanged(self.rect.centerx, self.rect.centery, direction, self, damage, self.usingMelee)
            if self.usingMelee:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(self.soundEffects[3]))
            else:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(self.soundEffects[2]))
            self.last_shot = now

    def ouch(self, damage=10):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.soundEffects[1]))

        now = pygame.time.get_ticks()
        if now - self.last_hit > self.hurtDelay:
            self.health -= damage
            self.last_hit = now
            if self.health <= 0:
                self.onDeath()
    
    def heal(self, amount):
        if amount <= 0:
            pass
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        self.scene.overlay.healthChange()

    def onDeath(self):
        pass

    def swap_weapons(self):
        self.usingMelee = not self.usingMelee

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
