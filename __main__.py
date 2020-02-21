import pygame
import league
from player import Player
from NPC_crate import *
import scene as sc


if __name__ == "__main__":
    e = league.Engine('Knave Escape')
    e.init_pygame()

    sc.scene = sc.Scene(e, sc.scene_list[sc.scene_index])
    sc.scene.layer = 0
    e.drawables.add(sc.scene)

    e.events[pygame.QUIT] = e.stop
    e.key_events[pygame.K_r] = sc.reset_room
    e.run(sc.update_callback)
