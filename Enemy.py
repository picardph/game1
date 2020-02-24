

from league import *
from league.game_objects import Updateable
from collision import Collision, Collidable
from pygame import Vector3
import pygame
from pygame import Vector3
from range_shot import Ranged_Shot


class Enemy(Character, Collidable):
    """
    """

    def __init__(self, scene, *args, image='assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_idle_anim_f0.png'):
        
        super().__init__(args)
        # This unit's health
        self.health = 30

        # This unit's max health
        self.maxHealth = 100

        # Damage values
        self.meleeDmg = 20
        self.rangedDmg = 10

        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()

        # Last time I attacked
        self.last_shot = pygame.time.get_ticks()

        # A unit-less value.  Bigger is faster.
        self.delta = 150

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
        self.soundEffects.append('assets/Music/Movement/footsteps/step_cloth2.ogg')
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

        self.scene = scene

        # Used to tell where this enemy should move.
        self.destinations = []

        # What destination is currently being targeted.
        self.destIndex = 0

        # How accurate the pathfinding has to be. Lower is more accurate.
        self.pfTolerance = 5

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

            pygame.mixer.Channel(4).play(pygame.mixer.Sound(self.soundEffects[0]))

        except:
            pass

    def shoot(self, direction:Vector3):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 400:
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

    def slowUpdate(self):
        self.simplePathFinding()
        self.attackPlayer()

    def onCollision(self, collision, direction):
        other = collision.getOther(self)
        if(abs(direction.x) > abs(direction.y)):
            direction.y = 0
        else:
            direction.x = 0
        self.move(direction.normalize())

        if type(other) is Ranged_Shot:
            if other.source is not self:
                self.ouch(other.damage)

    def ouch(self, damage=10):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.soundEffects[1]))

        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
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
        self.scene.despawnObject(self)

    def swap_weapons(self):
        self.usingMelee = not self.usingMelee

    def simplePathFinding(self):
        """
        This path finding method simply directs the enemy towards each location
        in the destinations list. It does not account for obstacles. When it 
        reaches the end of the list, it returns to the start.

        If the player is within 180 units of the enemy, the enemy will now "chase"
        the player.
        """

        playerPos = Vector3(self.scene.player.rect.centerx, self.scene.player.rect.centery, 0)
        distance = Vector3(self.x, self.y, 0).distance_to(playerPos)
        if distance < 180:
            self.move(self.getDirection(playerPos))
        else:
            distance = Vector3(self.x, self.y, 0).distance_to(self.destinations[self.destIndex])
            if  distance > self.pfTolerance:
                direction = (self.destinations[self.destIndex] - Vector3(self.x, self.y, 0)).normalize()
                self.direction = direction
            else:
                self.direction *= 0
                if self.destIndex < len(self.destinations) -1:
                    self.destIndex += 1
                else:
                    self.destIndex = 0


    def attackPlayer(self):
        playerPos = Vector3(self.scene.player.rect.centerx, self.scene.player.rect.centery, 0)
        distance = Vector3(self.x, self.y, 0).distance_to(playerPos)
        if distance < 300:
            if distance < 60:
                self.usingMelee = True
            else:
                self.usingMelee = False
            self.shoot(self.getDirection(playerPos))
            
    def getDirection(self, target:Vector3):
        """
        Method that returns a vector to the nearest cardinal direction to the target.
        """
        direction = (target - Vector3(self.rect.centerx, self.rect.centery, 0)).normalize()
        if direction.x > 0.25:
            direction.x = 1
        elif direction.x < -0.25:
            direction.x = -1
        else:
            direction.x = 0

        if direction.y > 0.25:
            direction.y = 1
        elif direction.y < -0.25:
            direction.y = -1
        else:
            direction.y = 0
        return direction