

from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
from pygame import Vector3
import pygame
from range_shot import Ranged_Shot
from Enemy import Enemy


class Player(Character, Collidable):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """

    def __init__(self, scene, *args, image='assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_idle_anim_f0.png'):
        
        super().__init__(args)
        # This unit's health
        self.health = 100

        # This unit's max health
        self.maxHealth = 100

        # Damage values
        self.meleeDmg = 50
        self.rangedDmg = 20

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
        self.collide_function = pygame.sprite.collide_rect
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

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

            damage = self.meleeDmg if self.usingMelee else self.rangedDmg
            self.scene.addRanged(self.rect.centerx, self.rect.centery, direction, self, damage, self.usingMelee)
            if self.usingMelee:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(self.soundEffects[3]))
            else:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(self.soundEffects[2]))
            self.last_shot = now

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.index = (self.index + 1) % len(self.idleImages)
        self.handleInput()

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

        other = collision.getOther(self)
        if(abs(direction.x) > abs(direction.y)):
            direction.y = 0
        else:
            direction.x = 0
        self.move(direction.normalize())

        if type(other) is Enemy:
            self.ouch(other.meleeDmg)
        
        if type(other) is Ranged_Shot:
            self.ouch(other.damage)

            
    def ouch(self, damage=10):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.soundEffects[1]))

        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health -= damage
            self.last_hit = now
            self.scene.overlay.healthChange()
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
        print("Player died!")
        self.scene.reset()
        #TODO Reset room.

    def swap_weapons(self):
        self.usingMelee = not self.usingMelee

    def handleInput(self):
        for event in self.scene.engine.gameEvents:
            if event.type == pygame.KEYDOWN:
                # Ideally these would be stored in a constants file but it works for now.

                # Movement
                if event.key == pygame.K_RIGHT:
                    self.direction.x = 1
                    self.setFlip = False
                if event.key == pygame.K_LEFT:
                    self.direction.x = -1
                    self.setFlip = True
                if event.key == pygame.K_UP:
                    self.direction.y = -1
                if event.key == pygame.K_DOWN:
                    self.direction.y = 1
                #TODO see why even when check passes, normalize thinks the vector has length 0.
                #if self.direction.length != 0:
                #    self.direction = self.direction.normalize()

                # Attack
                if event.key == pygame.K_d:
                    self.attackDirection.x = 1
                if event.key == pygame.K_a:
                    self.attackDirection.x = -1
                if event.key == pygame.K_w:
                    self.attackDirection.y = -1
                if event.key == pygame.K_s:
                    self.attackDirection.y = 1

            if event.type == pygame.KEYUP:
                
                # Movement release.
                if event.key == pygame.K_RIGHT:
                    self.direction.x = 0
                if event.key == pygame.K_LEFT:
                    self.direction.x = 0
                if event.key == pygame.K_UP:
                    self.direction.y = 0
                if event.key == pygame.K_DOWN:
                    self.direction.y = 0
                
                # Attack release
                if event.key == pygame.K_d:
                    self.attackDirection.x = 0
                if event.key == pygame.K_a:
                    self.attackDirection.x = 0
                if event.key == pygame.K_w:
                    self.attackDirection.y = 0
                if event.key == pygame.K_s:
                    self.attackDirection.y = 0

                # Weapon Switch
                if event.key == pygame.K_SPACE:
                    self.swap_weapons()

