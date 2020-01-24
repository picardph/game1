#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player

def all_done(self):
    print("Peace out ya'll.")
    pygame.quit()
    sys.exit()

league.Settings.width = 768
league.Settings.height = 768

e = league.Engine("Really sucky PvZ")
e.init_pygame()

e.events[pygame.QUIT] = all_done

sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
t = league.Tilemap('./assets/defense.lvl', sprites, layer = 0)

scs = []
scs_b = []
sc = sprites.sprites[155]
sc_b = sprites.sprites[163]
for i in range(6):
    scs.append(league.Drawable())
    scs_b.append(league.Drawable())
    scs[i].image = sc.image
    scs_b[i].image = sc_b.image
    scs[i].rect = scs[i].image.get_rect()
    scs_b[i].rect = scs_b[i].image.get_rect()
    scs[i].rect.x = 64
    scs_b[i].rect.x = 64
    scs[i].rect.y = (128 * i) + 64
    scs_b[i].rect.y = (128 * i) + 96
    scs[i]._layer = 1
    scs_b[i]._layer = 1
    e.drawables.add(scs[i])
    e.drawables.add(scs_b[i])

z = Player(3)
z.rect.x = 500
z.rect.y = 500
e.drawables.add(z)

move_zombie = pygame.USEREVENT + 1
pygame.time.set_timer(move_zombie, 1000)
e.events[move_zombie] = z.move_left

e.drawables.add(t.passable.sprites())
e.run()
