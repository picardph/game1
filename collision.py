from pygame import *
from league.constants import Direction
from league.game_objects import Drawable

class Collision():
    # This is a class to give more detailed information about a collision.

    def __init__(self, source, target):
        #The object causing the collision
        self.source = source

        #The object collided with.
        self.target = target

        # These must be called in this order currently.
        self.sourceDirection = self.calcSourceDirection()
        self.targetDirection = self.calcTargetDirection(self.sourceDirection)

        if issubclass(type(source), Collidable):
            source.onCollision(self, self.sourceDirection)
        if issubclass(type(target), Collidable):
            target.onCollision(self, self.targetDirection)

    def calcSourceDirection(self):
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

    def calcTargetDirection(self, direction):
        if direction == Direction.EAST:
            return Direction.WEST
        elif direction == Direction.WEST:
            return Direction.EAST
        elif direction == Direction.NORTH:
            return Direction.SOUTH
        else:
            return Direction.NORTH

class Collidable(Drawable):
# Class that provides collision handling to other classes.

    def onCollision(self, collision, direction):
        pass