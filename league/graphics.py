
class SpriteSheet:
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
        # to a new image and returns it.
        y = self.tile_size * (num // self.per_row)
        x = self.tile_size * (num % self.per_row)
        image = pygame.Surface((self.tile_size, self.tile_size))
        image.blit(self.sheet, (0, 0), (x, y, x + self.tile_size, y + self.tile_size))
        return image

