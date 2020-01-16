# L.E.A.G.U.E.

Laker Educationally Accessible Game Understanding Engine is an engine built on top of PyGame to teach basic game development aspects.

Code for this engine is written to mirror pseudocode in *Game Programming Algorithms and Techniques* by Madhav.

Note that this was designed with education in mind.  Therefore optimization is not of the essence.  We will not (for instance) use concepts like DirtySprites or updating only parts of the screen, relying instead upon a more traditional (easier to understand albeit less optimal) approach.  This may mean renaming certain pygame concepts to keep closer to the textbook code.

There are some problems with pygame on macOS.  Be sure you use version 2.0.0dev6:

pip install pygame==2.0.0.dev6

**Be sure you are using Python 3.**

# Classes

**Engine** - the core game engine.  No game logic should go here, merely the game loop.

**Graphics** - a utility class for graphics functions.

**Settings** - a static class used to hold default values needed by the Engine class.

# Use
