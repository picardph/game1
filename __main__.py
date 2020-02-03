import pygame
import league
from player import Player
from NPC_crate import *


if __name__ == "__main__":
    e = league.Engine('Knave Escape')
    e.init_pygame()

    # Initialize the player
    sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    t = league.Tilemap('./assets/world.lvl', sprites, layer=1)
    b = league.Tilemap('./assets/background.lvl', sprites, layer=0)
    world_size = (t.wide * league.Settings.tile_size, t.high * league.Settings.tile_size)

    t.layer = 0

    e.drawables.add(t.passable.sprites())


    you = Player(0, 0, 0)
    you.world_size = world_size
    you.rect = you.image.get_rect()
    you.blocks.add(t.impassable)
    you._layer = 1

    print(you.image)


    crate1 = Crate(0,100,0)
    crate1.world_size = world_size
    crate1.rect = crate1.image.get_rect()
    crate1.blocks.add(t.impassable)
    crate1._layer = 1
    print(crate1.image)



    e.objects.append(you)
    e.drawables.add(you)

    e.objects.append(crate1)
    e.drawables.add(crate1)

    e.key_events[pygame.K_a] = you.move_left
    e.key_events[pygame.K_d] = you.move_right
    e.key_events[pygame.K_w] = you.move_up
    e.key_events[pygame.K_s] = you.move_down

    e.key_events[pygame.K_LEFT] = you.move_left
    e.key_events[pygame.K_RIGHT] = you.move_right
    e.key_events[pygame.K_UP] = you.move_up
    e.key_events[pygame.K_DOWN] = you.move_down

    e.events[pygame.QUIT] = e.stop
    e.run()
