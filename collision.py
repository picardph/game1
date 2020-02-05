from pygame import *
from league.constants import Direction

class Collision():
    # This is a class to give more detailed information about a collision.

    def __init__(self, source, target):
        #The object causing the collision
        self.source = source

        #The object collided with.
        self.target = target

        self.direction = self.direction()


    def direction(self):
        diffX = self.source.rect.left - self.target.rect.left
        diffY = self.source.rect.top - self.target.rect.top

        if abs(diffX) > abs(diffY):
            if diffX > 0:
                direction = Direction.EAST
            else:
                direction = Direction.WEST
        else:
            if diffY > 0:
                direction = Direction.SOUTH
            else:
                direction = Direction.NORTH
        return direction

