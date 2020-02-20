from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
from pygame import Vector3
import pygame
from range_shot import Ranged_Shot


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

        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()

        # A unit-less value.  Bigger is faster.
        self.delta = 100

        # The direction the player is facing. Should be a unit vector.
        self.direction = Vector3(0, 0, 0)

        #flag to tell us if we need to flip image or not
        self.setFlip = False

        #flag to tell us if player is moving
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
        self.collide_function = pygame.sprite.collide_rect
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()
        
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0,0,0))

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
        except:
            pass

    def shoot_left(self):
        pass

    def shoot_right(self):
        self.scene.addRanged(self.x, self.y)
        pass

    def shoot_up(self):
        pass

    def shoot_down(self):
        pass

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

        #Load animations based on movement state.
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
        if(abs(direction.x) > abs(direction.y)):
            direction.y = 0
        else:
            direction.x = 0
        self.move(direction.normalize())

        #For testing health.
        #TODO Check for object type

        self.ouch()


    def ouch(self):
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
        #TODO handle player death.
        pass

    def handleInput(self):
        for event in self.scene.engine.gameEvents:
            if event.type == pygame.KEYDOWN:
                # Ideally these would be stored in a constants file but it works for now.
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

            if event.type == pygame.KEYUP:
                # Ideally these would be stored in a constants file but it works for now.
                if event.key == pygame.K_RIGHT:
                    self.direction.x = 0
                if event.key == pygame.K_LEFT:
                    self.direction.x = 0
                if event.key == pygame.K_UP:
                    self.direction.y = 0
                if event.key == pygame.K_DOWN:
                    self.direction.y = 0
               #TODO see why even when check passes, normalize thinks the vector has length 0.
               # if self.direction.length != 0:
                #    self.direction = self.direction.normalize()



