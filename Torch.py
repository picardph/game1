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

        self.animation_time = 0.2
        self.current_time = 0

    #updates based on clock tick
    def update(self, dt):

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

