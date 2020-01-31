import pygame
import league
import os
import json
import enum
import NPC_crate


TILE_WIDTH = 32
TILE_HEIGHT = 32


class TileType(enum.Enum):
    empty = (255, 255, 255)                 # Empty
    wall = (0, 0, 0)                        # Black
    crate = (185, 122, 87)                  # Brown


background_tiles = [
    TileType.empty,
    TileType.wall
]


class Scene:
    def __init__(self, folder):
        data = json.loads(folder + "/data.json")

        self.__background = [[TileType.empty for y in range(0, data['height'])] for x in range(0, data['width'])]
        self.__crates = []

        surface = pygame.image.load(folder + "/background.png")
        for x in range(0, surface.get_width()):
            for y in range(0, surface.get_height()):
                color = surface.get_at(x, y)

                # Depending on the color of the pixel, different things will be spawned.
                if color in background_tiles:
                    self.__background[x][y] = color
                elif color == TileType.crate:
                    self.__crates.append(NPC_crate.Crate(x * TILE_WIDTH, y * TILE_HEIGHT))

    def update(self, delta):
        pass

    def render(self, delta):
        pass

    def is_puzzle_finished(self, delta):
        return False
