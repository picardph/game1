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

        self.calcDirections()

        if issubclass(type(source), Collidable):
            source.onCollision(self, self.sourceDirection)
            #print(str(self.source) + "direction: " + str(self.sourceDirection))
        if issubclass(type(target), Collidable):
            target.onCollision(self, self.targetDirection)
            #print(str(self.target) + " direction: " + str(self.targetDirection))

    def calcDirections(self):
        diffX = self.source.rect.left - self.target.rect.left
        diffY = self.source.rect.top - self.target.rect.top

        self.sourceDirection = Vector3(diffX, diffY, 0)
        self.targetDirection = Vector3(-diffX, -diffY, 0)

class Collidable(Drawable):
# Class that provides collision handling to other classes.

    def onCollision(self, collision, direction):
        pass