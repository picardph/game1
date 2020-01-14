from settings import Settings
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Tilemap:
    """An object that represents an MxN list of tiles.  Give x, y
    returns various pieces of information about that tile, such as
    the image to draw, etc.

    Fields:
    spritesheet - The spritesheet from which to get the images for the tiles.
    tile_size - The number of pixels wide and high (we are forcing squares) per tile.
    wide - The number of tiles wide the map holds.
    high - The number of tiles vertically the map holds.
    world - The MxN list of tile numbers.
    sprites - The sprites for drawing the world.
    """
    def __init__(self, path, spritesheet, wide, high, tile_size = Settings.tile_size):
        self.path = path
        self.spritesheet = spritesheet
        self.wide = wide
        self.high = high
        self.tile_size = tile_size
        self.world = []
        self.sprites = []
        self.__parse()

    def __parse(self):
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            contents = list(reader)
        self.wide = contents[0]
        self.high = contents[1]
        self.world = contents[2:]
        a = 0
        for i in self.world:
            b = 0
            for j in i:
                x = b * self.spritesheet.tile_size
                y = a * self.spritesheet.tile_size
                sprite.image = self.spritesheet.sprites[a * self.spritesheet.per_row + b]
                # Set rectangle coords
                rect = sprite.image.get_rect()
                rect.x = x
                rect.y = y
                self.sprites.append(sprite)

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
        count = 0
        for i in range(height // self.tile_size):
            for j in range(width // self.tile.size):
                image = self.__get_image_num(count)
                sprites.append(image)
                count = count + 1
        return sprites

    def __get_image_num(self, num):
        # This function copies an MxM image from x, y
        # to a new Sprite and returns it.
        y = self.tile_size * (num // self.per_row)
        x = self.tile_size * (num % self.per_row)
        sprite = Sprite()
        sprite.image = pygame.Surface((self.tile_size, self.tile_size))
        sprite.image.blit(self.sheet, (0, 0), (x, y, x + self.tile_size, y + self.tile_size))
        return sprite

