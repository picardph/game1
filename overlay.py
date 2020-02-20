import league
import pygame

class Overlay(league.DUGameObject):
    def __init__(self, player):
        super().__init__(self)
        self._layer = 1000
        self.player = player

        self.hpBarWidth = 62
        self.hpColor = (200, 0, 0, 255)
        self.hpRect = pygame.Rect(18, 1, self.hpBarWidth, 14)
        
        self.image = pygame.Surface([80, 16])
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
        self.image.fill((0,100,200, 0))
        pygame.draw.rect(self.image, self.hpColor, self.hpRect)
        self.image.blit(self.uiHealthFrame, (0, 0))

    def healthChange(self):
        # Method that updates health bar
        # This is to prevent unnecessary calculations each frame.

        self.hpRect.width = round(62 * (self.player.health / self.player.maxHealth))