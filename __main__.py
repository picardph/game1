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
<<<<<<< HEAD
    you = Player(0, scene.get_starting_x(), scene.get_starting_y())
    testCrate = Crate(0, 200, 100)
    scene.impassable.add(testCrate)
    scene.impassable.add(you)

    
    you.world_size = world_size
    you.rect = you.image.get_rect()
    you.blocks.add(scene.impassable)
    you._layer = 1

    testCrate.world_size = world_size
    testCrate.rect = testCrate.image.get_rect()
    testCrate.blocks.add(scene.impassable)
    testCrate._layer = 1
    

    e.objects.append(you)
    e.drawables.add(you)
    e.drawables.add(scene)

    #test crate
    e.objects.append(testCrate)
    e.drawables.add(testCrate)

    e.key_events[pygame.K_a] = you.move_left
    e.key_events[pygame.K_d] = you.move_right
    e.key_events[pygame.K_w] = you.move_up
    e.key_events[pygame.K_s] = you.move_down

    e.key_events[pygame.K_LEFT] = you.move_left
    e.key_events[pygame.K_RIGHT] = you.move_right
    e.key_events[pygame.K_UP] = you.move_up
    e.key_events[pygame.K_DOWN] = you.move_down

=======
    e.drawables.add(scene)

>>>>>>> master
    e.events[pygame.QUIT] = e.stop
    e.run()
