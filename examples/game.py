#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player

"""This file is garbage. It was a hastily coded mockup
to demonstrate how to use the engine.  We will be creating
a Game class that organizes this code better (and is
reusable).
"""

# Function to call when colliding with zombie
def ouch():
    print("Ouch!  Look out, you #$!@%!@")

def main():
    e = league.Engine("Sigrid's Quest")
    e.init_pygame()

    sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    t = league.Tilemap('./assets/world.lvl', sprites, layer = 1)
    b = league.Tilemap('./assets/background.lvl', sprites, layer = 0)
    world_size = (t.wide*league.Settings.tile_size, t.high *league.Settings.tile_size)
    e.drawables.add(t.passable.sprites())
    e.drawables.add(b.passable.sprites()) 
    text = "0100     4 lives"
    font = pygame.font.SysFont("comicsansms", 72)
    score = font.render(text, True, (0, 0, 0))
    e.overlay = text
    p = Player(2, 400, 300)
    p.blocks.add(t.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()
    q = Player(10, 100, 100)
    q.image = p.image
    e.objects.append(p)
    e.objects.append(q)
    e.drawables.add(p)
    e.drawables.add(q)
    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    #c = league.DumbCamera(800, 600, p, e.drawables, world_size)
    
    e.objects.append(c)

    e.collisions[p] = (q, ouch) 
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down
    e.events[pygame.USEREVENT + 1] = q.move_right
    e.events[pygame.QUIT] = e.stop
    e.run()

if __name__=='__main__':
    main()
