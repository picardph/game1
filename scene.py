import pygame
import league
import json
import enum
import NPC_crate
from overlay import Overlay
import range_shot
from player import Player


TILE_WIDTH = league.settings.Settings.tile_size
TILE_HEIGHT = league.settings.Settings.tile_size


class TileType(enum.Enum):
    empty = pygame.Color(255, 255, 255)                 # Empty
    wall = pygame.Color(0, 0, 0)                        # Black
    crate = pygame.Color(185, 122, 87)                  # Brown
    start = pygame.Color(0, 255, 0)                     # Green
    end = pygame.Color(255, 0, 0)                       # Red
    open_end = pygame.Color(200, 0, 0)                  # Light Red
    pressure_plate = pygame.Color(163, 73, 164)         # Purple


class Scene(league.game_objects.Drawable):
    def __init__(self, engine, folder):
        super().__init__()
        self.tw = league.settings.Settings.tile_size
        self.th = league.settings.Settings.tile_size
        file = open(folder + "/data.json", "r")
        data = json.loads(file.read())
        file.close()
        pygame.mixer.music.load('assets/Music/D1ST0RT.wav')
        pygame.mixer.music.play(-1)



        self.engine = engine
        self.__width = data['width']
        self.__height = data['height']
        self.__background = [[TileType.empty for y in range(0, data['height'])] for x in range(0, data['width'])]
        self.__crates = []
        self.__pressure_plates = []
        self.__start_x = 0
        self.__start_y = 0
        self.__end_x = 0
        self.__end_y = 0
        self.__end_open = False
        self.__tile_images = {
            TileType.wall: pygame.image.load('assets/tiles/wall.png').convert(),
            TileType.end: pygame.image.load('assets/tiles/closed_door.png').convert(),
            TileType.open_end: pygame.image.load('assets/tiles/open_door.png').convert(),
            TileType.pressure_plate: pygame.image.load('assets/tiles/pressure_plate.png').convert()
        }
        self.engine = engine
        self.impassable = pygame.sprite.Group()

        world_size = (self.get_width() * league.Settings.tile_size, self.get_height() * league.Settings.tile_size)

        player = Player(self, 0, 0, 0)
        player.world_size = world_size
        player.rect = player.image.get_rect()
        player._layer = 1

        engine.objects.append(player)
        engine.drawables.add(player)

        #Add overlay to scene
        self.overlay = Overlay(player)

        engine.objects.append(self.overlay)
        engine.drawables.add(self.overlay)

        # Fill out the scene's data with information by reading pixels from
        # an image.
        surface = pygame.image.load(folder + "/background.png").convert()
        for x in range(0, surface.get_width()):
            for y in range(0, surface.get_height()):
                color = surface.get_at((x, y))

                # Depending on the color of the pixel, different things will be spawned.
                if color == TileType.wall.value:
                    self.__background[x][y] = TileType.wall
                    # Add this wall to our collisions system.
                    # We will just use a blank dumy sprite because the scene handles
                    # rendering the walls and what not.
                    spr = pygame.sprite.Sprite()
                    spr.x = x * TILE_WIDTH
                    spr.y = y * TILE_HEIGHT
                    spr.rect = pygame.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                    self.impassable.add(spr)
                elif color == TileType.crate.value:
                    crate = NPC_crate.Crate(0, x * TILE_WIDTH, y * TILE_HEIGHT)
                    crate.world_size = world_size
                    crate.rect = crate.image.get_rect()
                    crate._layer = 1
                    self.__crates.append(crate)

                    engine.objects.append(crate)
                    engine.drawables.add(crate)

                    # testCrate.blocks.add(scene.impassable)
                elif color == TileType.start.value:
                    self.__start_x = x * TILE_WIDTH
                    self.__start_y = y * TILE_HEIGHT
                    player.x = x
                    player.y = y
                elif color == TileType.end.value:
                    self.__end_x = x * TILE_WIDTH
                    self.__end_y = y * TILE_HEIGHT
                    self.__background[x][y] = TileType.end
                elif color == TileType.pressure_plate.value:
                    self.__background[x][y] = TileType.pressure_plate
                    self.__pressure_plates.append((x * TILE_WIDTH, y * TILE_HEIGHT))

        # Pre-render that data to a surface to save performance.
        self.image = self.render_background()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())

        # Only add the impassable blocks at the end so nothing else can be added.
        for c in self.__crates:
            for im in self.impassable:
                if c is not im:
                    c.blocks.add(im)
        player.blocks.add(self.impassable, self.__crates)
        for c in self.__crates:
            c.blocks.add(self.__crates)

        # Move the player to the starting position.
        player.x = self.get_starting_x()
        player.y = self.get_starting_y()

        engine.key_events[pygame.K_a] = player.shoot_left
        engine.key_events[pygame.K_d] = player.shoot_right
        engine.key_events[pygame.K_w] = player.shoot_up
        engine.key_events[pygame.K_s] = player.shoot_down

    def render_background(self):
        background = pygame.Surface((self.__width * TILE_WIDTH, self.__height * TILE_HEIGHT))
        for x in range(0, self.__width):
            for y in range(0, self.__height):
                tile = self.__background[x][y]
                if tile is not TileType.empty:
                    image = self.__tile_images[tile]
                    background.blit(image, (x * TILE_WIDTH, y * TILE_HEIGHT))
        return background

    def is_puzzle_finished(self):
        # Check every pressure plate and check that a crate is on it.
        states = [False for p in self.__pressure_plates]
        idx = 0
        for plate in self.__pressure_plates:
            for crate in self.__crates:
                plate_vec = pygame.Vector2(plate)
                crate_vec = pygame.Vector2((crate.x, crate.y))
                dist = plate_vec.distance_to(crate_vec)
                if dist < 16:
                    states[idx] = True
            idx += 1
        for s in states:
            if not s:
                return False
        return True

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_starting_x(self):
        return self.__start_x

    def get_starting_y(self):
        return self.__start_y

    def addRanged(self, x, y, direction = "right"):
        bullet = range_shot.Ranged_Shot(0, x, y, self, direction)
        bullet._layer = 1
        bullet.blocks.add(self.impassable, self.__crates)
        self.engine.objects.append(bullet)
        self.engine.drawables.add(bullet)

    def removeBullet(self, bullet):
        self.engine.objects.remove(bullet)
        self.engine.drawables.remove(bullet)