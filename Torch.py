import pygame

class Torch(pygame.sprite.Sprite):
    def __init__(self):
        super(Torch, self).__init__()

        self.images = []

        self.images.append('assets/v1.1 dungeon crawler 16x16 pixel pack/props_itens/torch_anim_f0.png')
        self.images.append('assets/v1.1 dungeon crawler 16x16 pixel pack/props_itens/torch_anim_f1.png')
        self.images.append('assets/v1.1 dungeon crawler 16x16 pixel pack/props_itens/torch_anim_f2.png')
        self.images.append('assets/v1.1 dungeon crawler 16x16 pixel pack/props_itens/torch_anim_f3.png')
        self.images.append('assets/v1.1 dungeon crawler 16x16 pixel pack/props_itens/torch_anim_f4.png')
        self.images.append('assets/v1.1 dungeon crawler 16x16 pixel pack/props_itens/torch_anim_f5.png')

        self.index = 0
        self.image = self.images[self.index]


    #updates based on clock tick
    def update(self):

            self.index = (self.index + 1) % len(self.images)
            self.image = pygame.image.load(self.images[self.index]).convert_alpha()

