import abc
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from .settings import *

class Engine:
    """Engine is the definition of our game engine.  We want it to
    be as game agnostic as possible, and will try to emulate code
    from the book as much as possible.  If there are deviations they
    will be noted here.

    Fields:
    title - The name of the game.
    running - Whether or not the engine is currently in the main game loop.
    clock - The real world clock for elapsed time.
    events - A dictionary of events and handling functions.
    objects - A list of updateable game objects.
    drawable - A list of drawable game objects.
    screen - The window we are drawing upon.
    realDeltaTime - How much clock time has passed since our last check.
    gameDeltaTime - How much game time has passed since our last check.
    """

    def __init__(self, title):
        self.title = title
        self.running = False
        self.clock = None 
        self.events = {}
        self.objects = []
        self.drawables = []
        self.screen = None
        self.realDeltaTime = 0

    def init_pygame(self):
        """This function sets up the state of the pygame system,
        including passing any specific settings to it."""
        # Startup the pygame system
        pygame.init()
        # Create our window
        self.screen = pygame.display.set_mode((Settings.width, Settings.height))
        # Set the title that will display at the top of the window.
        pygame.display.set_caption(self.title)
        # Create the clock
        self.clock = pygame.time.Clock()
        # Startup the joystick system
        pygame.joystick.init()
        # For each joystick we find, initialize the stick
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
        # Set the repeat delay for key presses
        pygame.key.set_repeat(Settings.key_repeat)

    def run(self):
        """The main game loop.  As close to our book code as possible."""
        self.running = True
        while self.running:
            # The time since the last check
            self.realDeltaTime = pygame.time.get_ticks() - self.realDeltaTime 
            self.gameDeltaTime = self.realDeltaTime * Settings.gameTimeFactor

            # Wipe screen
            self.screen.fill(Settings.fill_color)
            
            # Process inputs
            self.handle_inputs()

            # Update game world
            # Each object must have an update(time) method
            for o in self.objects:
                o.update(self.gameDeltaTime)

            # Generate outputs
            for d in self.drawables:
                d.draw(self.screen)

            font = self.font = pygame.font.Font(None,30)
            fps = font.render("FPS: " + str(int(self.clock.get_fps())), True, Settings.overlay_color)
            #print(self.clock.get_fps())
            self.screen.blit(fps, (10, 10))
            pygame.display.flip()
            #pygame.display.update()

            # Frame limiting code
            self.clock.tick(Settings.fps)
    
    def stop(self):
        self.running = False

    def handle_inputs(self):
        for event in pygame.event.get():
            #print(event)
            if event.type in self.events.keys():
                self.events[event.type]()
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_events.keys():
                    #print(event.key)
                    self.key_events[event.key]() 


class GameObject(abc.ABC):
    """Any object that makes up our game world."""
    pass

class Drawable(pygame.sprite.Sprite):
    """Creates a drawable.  For us, a drawable is a pygame Sprite object."""
    def __init__(self, layer=0):
        super().__init__()
        self.layer = layer

class Updateable(abc.ABC):
    """An interface that ensures an object has an update(gameDeltaTime) method."""
    @abc.abstractmethod
    def update(gameDeltaTime):
        pass

class UGameObject(GameObject, Updateable):
    """A game object that is updateable but not drawn."""
    pass

class DGameObject(GameObject, Drawable):
    """A game object that is drawable, but not updateable.  A static object."""
    pass

class DUGameObject(UGameObject, Drawable):
    """A game object that is updateable and drawable."""
    pass
