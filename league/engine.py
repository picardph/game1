from settings import Settings
from graphics import SpriteSheet

class Engine:
    """Engine is the definition of our game engine.  We want it to
    be as game agnostic as possible, and will try to emulate code
    from the book as much as possible.  If there are deviations they
    will be noted here.

    Fields:
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
        self.running = False
        self.clock = pygame.time.Clock()
        self.events = {}
        self.objects = []
        self.drawables = []
        self.screen = self.get_window(title, Settings.width, Settings.height)
        self.init_pygame()
        self.realDeltaTime = 0

    def init_pygame(self):
        """This function sets up the state of the pygame system,
        including passing any specific settings to it."""
        # Startup the pygame system
        pygame.init()
        # Startup the joystick system
        pygame.joystick.init()
        # For each joystick we find, initialize the stick
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
        # Set the repeat delay for key presses
        pygame.key.set_repeat(Settings.repeat)

    def get_window(self, title, width, height):
        """This function creates a new window and returns a reference to it."""
        # Set the title that will display at the top of the window.
        pygame.display.set_caption(title)
        # Create a window of the given dimensions and return it.
        screen = pygame.display.set_mode(width, height)
        return screen

    def run(self):
        """The main game loop.  As close to our book code as possible."""
        while self.running:
            # The time since the last check
            self.realDeltaTime = pygame.time.get_ticks() - self.realDeltaTime 
            self.gameDeltaTime = self.realDeltaTime * Settings.gameTimeFactor

            # Process inputs
            self.handleInputs()

            # Update game world
            # Each object must have an update(time) method
            for o in self.objects:
                o.update(self.gameDeltaTime)

            # Generate outputs
            for d in self.drawables:
                d.draw()

            # Frame limiting code
            self.clock.tick(Settings.fps)
