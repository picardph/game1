import pygame
import league
from player import Player
from NPC_crate import *
from scene import Scene


if __name__ == "__main__":
    e = league.Engine('Knave Escape')
    e.init_pygame()

    scene = Scene(e, "assets/rooms/level1")
    scene.layer = 0
    e.drawables.add(scene)

    e.events[pygame.QUIT] = e.stop
    e.run()
