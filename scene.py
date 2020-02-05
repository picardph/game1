import pygame
import league
import json
import enum
import NPC_crate


TILE_WIDTH = league.settings.Settings.tile_size
TILE_HEIGHT = league.settings.Settings.tile_size


class TileType(enum.Enum):
    empty = pygame.Color(255, 255, 255)                 # Empty
    wall = pygame.Color(0, 0, 0)                        # Black
    crate = pygame.Color(185, 122, 87)                  # Brown
    start = pygame.Color(0, 255, 0)                     # Green
    end = pygame.Color(255, 0, 0)                       # Red
    open_end = pygame.Color(200, 0, 0)                  # Light Red


class Scene(league.game_objects.Drawable):
    def __init__(self, engine, folder):
        super().__init__()
        file = open(folder + "/data.json", "r")
        data = json.loads(file.read())
        file.close()

        self.__engine = engine
        self.__width = data['width']
        self.__height = data['height']
        self.__background = [[TileType.empty for y in range(0, data['height'])] for x in range(0, data['width'])]
        self.__crates = []
        self.__start_x = 0
        self.__start_y = 0
        self.__end_x = 0
        self.__end_y = 0
        self.__end_open = False
        self.__tile_images = {
            TileType.wall: pygame.image.load('assets/tiles/wall.png').convert(),
            TileType.end: pygame.image.load('assets/tiles/closed_door.png').convert(),
            TileType.open_end: pygame.image.load('assets/tiles/open_door.png').convert()
        }

        # Fill out the scene's data with information by reading pixels from
        # an image.
        surface = pygame.image.load(folder + "/background.png").convert()
        for x in range(0, surface.get_width()):
            for y in range(0, surface.get_height()):
                color = surface.get_at((x, y))

                # Depending on the color of the pixel, different things will be spawned.
                if color == TileType.wall.value:
                    self.__background[x][y] = TileType.wall
                elif color == TileType.crate.value:
                    self.__crates.append(NPC_crate.Crate(0, x * TILE_WIDTH, y * TILE_HEIGHT))
                elif color == TileType.start.value:
                    self.__start_x = x * TILE_WIDTH
                    self.__start_y = y * TILE_HEIGHT
                elif color == TileType.end.value:
                    self.__end_x = x * TILE_WIDTH
                    self.__end_y = y * TILE_HEIGHT
                    self.__background[x][y] = TileType.end

        # Pre-render that data to a surface to save performance.
        self.image = self.render_background()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())

        self.impassable = pygame.sprite.Group()

    def render_background(self):
        background = pygame.Surface((self.__width * TILE_WIDTH, self.__height * TILE_HEIGHT))
        for x in range(0, self.__width):
            for y in range(0, self.__height):
                tile = self.__background[x][y]
                if tile is not TileType.empty:
                    image = self.__tile_images[tile]
                    background.blit(image, (x * TILE_WIDTH, y * TILE_HEIGHT))
        return background

    def is_puzzle_finished(self, delta):
        return False

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_starting_x(self):
        return self.__start_x

    def get_starting_y(self):
        return self.__start_y
