import pygame
import league
from player import Player


if __name__ == "__main__":
    e = league.Engine('Free Palestine')
    e.init_pygame()

    # Initialize the player
    sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    t = league.Tilemap('./assets/world.lvl', sprites, layer=1)
    b = league.Tilemap('./assets/background.lvl', sprites, layer=0)
    world_size = (t.wide * league.Settings.tile_size, t.high * league.Settings.tile_size)
    e.drawables.add(t.passable.sprites())

    you = Player(0, 0, 0)
    you.world_size = world_size
    you.rect = you.image.get_rect()
    you.blocks.add(t.impassable)

    print(you.image)


    e.objects.append(you)
    e.drawables.add(you)

    e.events[pygame.QUIT] = e.stop
    e.run()
