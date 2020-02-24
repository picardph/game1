

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

    def __init__(self, scene, *args):
        
        super().__init__(scene, args)
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

        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f0.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f1.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f2.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f3.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f4.png')
        self.runImages.append('assets/v1.1 dungeon crawler 16x16 pixel pack/heroes/knight/knight_run_anim_f5.png')

    def onCollision(self, collision, direction):
        other = collision.getOther(self)
        if type(other) is Ranged_Shot:
            if type(other.source) is Enemy:
                self.ouch(other.damage)
            return
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
        super().ouch(damage)
        self.scene.overlay.healthChange()
    
    def heal(self, amount):
        super().heal(amount)
        self.scene.overlay.healthChange()

    def onDeath(self):
        print("Player died!")
        self.scene.reset()
        #TODO Reset room.

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

    def update(self):
        super().update()

        self.handleInput()

        for sprite in self.blocks:
            if sprite is not self:
                self.collider.rect.x = sprite.x
                self.collider.rect.y = sprite.y
                if pygame.sprite.collide_rect(self, self.collider):
                    Collision(self, sprite)
