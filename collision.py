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

        self.isTrigger = False
        
        #Is either object a trigger?
        if issubclass(type(source), Collidable):
            self.isTrigger = source.isTrigger
        if issubclass(type(target), Collidable):
            self.isTrigger = target.isTrigger or self.isTrigger

        self.calcDirections()

        if issubclass(type(source), Collidable):
            if self.isTrigger:
                source.onTrigger(self,self.sourceDirection)
            else:
                source.onCollision(self, self.sourceDirection)
            
        if issubclass(type(target), Collidable):
            if self.isTrigger:
                target.onTrigger(self, self.targetDirection)
            else:
                target.onCollision(self, self.targetDirection)
            
    def calcDirections(self):
        diffX = self.source.rect.left - self.target.rect.left
        diffY = self.source.rect.top - self.target.rect.top

        self.sourceDirection = Vector3(diffX, diffY, 0)
        self.targetDirection = Vector3(-diffX, -diffY, 0)

class Collidable(Drawable):
# Class that provides collision handling to other classes.
    def __init__(self, *args, trigger=False):
        super().__init__(args)
        self.isTrigger = trigger

    def onCollision(self, collision, direction):
        pass
    
    def onTrigger(self, collision, direction):
        pass