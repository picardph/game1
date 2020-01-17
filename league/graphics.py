from .settings import *
from .engine import *
from .game_objects import *

import csv
import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Tilemap:
    """An object that represents an MxN list of tiles.  Give x, y
    returns various pieces of information about that tile, such as
    the image to draw, etc.

    Fields:
    path - A path to the file that holds the tilemap data.  Structure described below.
    spritesheet - The spritesheet from which to get the images for the tiles.
    tile_size - The number of pixels wide and high (we are forcing squares) per tile.
    wide - The number of tiles wide the map holds.
    high - The number of tiles vertically the map holds.
    world - The MxN list of tile numbers.
    sprites - The sprites for drawing the world.

    File structure:
    A tilemap file begins with the width (an integer) of the map (in tiles, not pixels), a newline,
    the height (an integer; again in tiles, not pixels), followed by a comma-separated list of lists
    of integers that represent the sprite number from the spritesheet.  For instance,

    5
    7
    1, 1, 1, 1, 2, 1, 1
    1, 1, 1, 1, 2, 1, 1
    1, 1, 1, 2, 1, 2, 1
    1, 1, 1, 2, 1, 2, 2
    2, 2, 2, 2, 1, 2, 2
    """
    def __init__(self, path, spritesheet, tile_size = Settings.tile_size, layer = 0):
        self.path = path
        self.spritesheet = spritesheet
        self.tile_size = tile_size
        self.layer = layer
        self.world = []
        self.group = pygame.sprite.Group()
        self.__parse()

    def __parse(self):
        """This function begins the process of (attempting) to
        parse a level file.  The structure of the file is described above.
        """
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            contents = list(reader)
        # How many tiles wide is our world?
        self.wide = contents[0]
        # And how tall?
        self.high = contents[1]
        # Sprite numbers for all tiles are in the
        # multidimensional list "world".
        self.world = contents[2:]
        a = 0
        for i in self.world:
            b = 0
            for j in i:
                x = b * self.spritesheet.tile_size
                y = a * self.spritesheet.tile_size
                base_sprite = self.spritesheet.sprites[int(j)]
                sprite = Drawable(self.layer)
                sprite.image = base_sprite.image
                # Set rectangle coords (using top-left coords here)
                rect = sprite.image.get_rect() 
                rect.x = x
                rect.y = y
                sprite.rect = rect
                self.group.add(sprite)
                b = b + 1
            a = a + 1

class Spritesheet:
    """An object that represents a spritesheet and provides
    methods to access individual sprites from it.

    There are better ways to create spritesheets.  This code does
    not allow for packed sprites for instance.  Instead, it forces
    sprites to be in nice, tiled squares.

    Fields:
    path - The path to the spritesheet file.
    tile_size - The number of pixels wide and high the sprites are.  We are forcing square tiles for this engine.
    per_row - The number of sprites per row on the spritesheet.
    width - Number of pixels wide of the spritesheet image.
    height - Number of pixels high of the spritesheet image.
    sprites - A single-dimensional list of the sprites from the sheet.
    """
    def __init__(self, path, tile_size, per_row):
        self.path = path
        self.sheet = pygame.image.load(self.path).convert_alpha()
        self.tile_size = tile_size
        self.per_row = per_row
        self.width, self.height = self.sheet.get_size()
        self.sprites = self.__split_up()

    def __split_up(self):
        # This function splits the sheet up into equal-sized chunks,
        # and returns a list of the chunks.
        sprites = []
        for i in range((self.width * self.height) // (Settings.tile_size * Settings.tile_size)):
                image = self.__get_image_num(i)
                sprites.append(image)
        return sprites

    def __get_image_num(self, num):
        # This function copies an MxM image from x, y
        # to a new Sprite and returns it.
        y = self.tile_size * (num  // self.per_row)
        x = self.tile_size * (num  % self.per_row)
        sprite = Drawable()
        sprite.image = pygame.Surface((self.tile_size, self.tile_size)).convert_alpha()
        sprite.image.blit(self.sheet, (0, 0), (x, y, x + self.tile_size, y + self.tile_size))
        return sprite
