

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

    def __init__(self, *args):
        
        super().__init__(args)

        
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

        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f0.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f1.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f2.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f3.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f4.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/enemies/goblin/goblin_run_anim_f5.png')

        # Used to tell where this enemy should move.
        self.destinations = []

        # What destination is currently being targeted.
        self.destIndex = 0

        # How accurate the pathfinding has to be. Lower is more accurate.
        self.pfTolerance = 5

    def update(self):
        super.update()

        self.simplePathFinding()
        self.attackPlayer()

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

        if type(other) is Ranged_Shot:
            if other.source is not self:
                self.ouch(other.damage)

    def onDeath(self):
        self.scene.despawnObject(self)

    def simplePathFinding(self):
        """
        This path finding method simply directs the enemy towards each location
        in the destinations list. It does not account for obstacles. When it 
        reaches the end of the list, it returns to the start.
        """
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