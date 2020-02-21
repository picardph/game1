import pygame
import league
from player import Player
from NPC_crate import *
from scene import Scene

global scene, scene_index, scene_list

scene_index = 0
scene = None
scene_list = ['assets/rooms/level1', 'assets/rooms/level2', 'assets/rooms/beat']


def update_callback():
    global scene_index, scene, scene_list
    if scene.is_puzzle_finished():
        scene_index += 1
        e.drawables.empty()
        e.objects.clear()
        e.collisions.clear()
        e.events.clear()

        scene = Scene(e, scene_list[scene_index])
        scene.layer = 0
        e.drawables.add(scene)
        e.events[pygame.QUIT] = e.stop


if __name__ == "__main__":
    e = league.Engine('Knave Escape')
    e.init_pygame()

    scene = Scene(e, scene_list[scene_index])
    scene.layer = 0
    e.drawables.add(scene)

    e.events[pygame.QUIT] = e.stop
    e.run(update_callback)
