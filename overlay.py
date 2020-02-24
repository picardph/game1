import league
import pygame

class Overlay(league.DUGameObject):
    def __init__(self, player):
        super().__init__(self)
        self._layer = 1000
        self.player = player

        self.hpBarWidth = 124
        self.hpColor = (200, 0, 0, 255)
        self.bgColor = (0, 0, 0, 125)
        self.hpRect = pygame.Rect(36, 2, self.hpBarWidth, 28)
        self.bgRect = pygame.Rect(36, 2, self.hpBarWidth, 28)
        
        self.image = pygame.Surface([160, 32], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.image.fill((100,100,100, 0))

        self.uiHealthFrame = pygame.image.load('assets/v1.1 dungeon crawler 16x16 pixel pack/ui (new)/health_ui.png') 

        pygame.draw.rect(self.image, self.hpColor, self.hpRect)
        self.image.blit(self.uiHealthFrame, (0, 0))
        self.x = 0
        self.y = 0
        self.rect.x = 0
        self.rect.y = 0
        self.static = True

    def update(self):
        pass

    def slowUpdate(self):
        self.image.fill((0,100,200, 0))
        pygame.draw.rect(self.image, self.bgColor, self.bgRect)
        pygame.draw.rect(self.image, self.hpColor, self.hpRect)
        self.image.blit(self.uiHealthFrame, (0, 0))

    def healthChange(self):
        # Method that updates health bar
        # This is to prevent unnecessary calculations each frame.

        self.hpRect.width = round(self.hpBarWidth * (self.player.health / self.player.maxHealth))