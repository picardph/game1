class Settings:
    """Settings exists to store default values used by the engine.
    These values will be class (static) variables, and are not final
    (Python doesn't support finals) so they are still changeable at runtime
    (though you should do so with great care!).

    Attributes:
    fps - Determines how many frames per second the engine attempts to render.
    key_repeat - How quickly (in milliseconds) to wait before allowing a key to repeat.
    width - The width of the screen in pixels.
    height - The height of the screen in pixels.
    tile_size - The default tile_size for sprites
    gameTimeFactor - Controls how real time relates to game time.
    """
    fps = 30
    key_repeat = 50
    width = 800
    height = 640
    tile_size = 32
    gameTimeFactor = 1

from enum import IntEnum
class State(IntEnum):
    """State enumerates character states for readability.  Common states
    are predefined, add your own as needed."""
    IDLE = 0
    MOVE = 1
    ATTACK = 2
    PROJECT = 3
    
from enum import IntEnum
class Direction(IntEnum):
    """Direction enumerates character directions for readability.  Cardinal
    directions are predefined, add your own as needed."""
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
