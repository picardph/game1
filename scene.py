import pygame
import league
import json
import enum
import NPC_crate
from overlay import Overlay
import range_shot
from player import Player
from Enemy import Enemy
from pygame import Vector3


TILE_WIDTH = league.settings.Settings.tile_size
TILE_HEIGHT = league.settings.Settings.tile_size

global e
e = None

global scene, scene_index, scene_list

scene_index = 0
scene = None
scene_list = ['assets/rooms/level3', 'assets/rooms/level4', 'assets/rooms/level1', 'assets/rooms/level2', 'assets/rooms/level5',
              'assets/rooms/level6', 'assets/rooms/beat']

def update_callback():
    global scene_index, scene, scene_list
    if scene.is_puzzle_finished():

        scene_index += 1
        e.drawables.empty()
        e.objects.clear()
        e.collisions.clear()
        e.events.clear()

        scene = Scene(e, scene_list[scene_index])
        scene.layer = 0
        e.drawables.add(scene)
        e.events[pygame.QUIT] = e.stop

def reset_room():
    global scene_index, scene, scene_list
    e.drawables.empty()
    e.objects.clear()
    e.collisions.clear()
    e.events.clear()

    scene = Scene(e, scene_list[scene_index])
    scene.layer = 0
    e.drawables.add(scene)
    e.events[pygame.QUIT] = e.stop


class TileType(enum.Enum):
    empty = pygame.Color(255, 255, 255)                 # Empty
    wall = pygame.Color(0, 0, 0)                        # Black
    crate = pygame.Color(185, 122, 87)                  # Brown
    start = pygame.Color(0, 255, 0)                     # Green
    end = pygame.Color(255, 0, 0)                       # Red
    open_end = pygame.Color(200, 0, 0)                  # Light Red
    pressure_plate = pygame.Color(163, 73, 164)         # Purple
    goblin = pygame.Color(181, 230, 29)                 # Lime


class Scene(league.game_objects.Drawable):
    def __init__(self, engine, folder):
        super().__init__()
        self.tw = league.settings.Settings.tile_size
        self.th = league.settings.Settings.tile_size
        file = open(folder + "/data.json", "r")
        data = json.loads(file.read())
        file.close()
        pygame.mixer.music.load('assets/Music/B0N3_J4NGL3.wav')
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        self.scene_not_done = True

        self.numEnemies = 0
        global e
        e = engine

        global scene
        scene = self

        self.__engine = engine
        self.__width = data['width']
        self.__height = data['height']
        self.__background = [[TileType.empty for y in range(0, data['height'])] for x in range(0, data['width'])]
        self.__crates = []
        self.__enemies = []
        self.__pressure_plates = []
        self.__pressure_plate_sounds = []
        self.__start_x = 0
        self.__start_y = 0
        self.__end_x = -20
        self.__end_y = -20
        self.__end_open = False
        self.__tile_images = {
            TileType.wall: pygame.image.load('assets/tiles/wall.png').convert(),
            TileType.end: pygame.image.load('assets/tiles/closed_door.png').convert(),
            TileType.open_end: pygame.image.load('assets/tiles/open_door.png').convert(),
            TileType.pressure_plate: pygame.image.load('assets/tiles/pressure_plate.png').convert()
        }

        self.__floor = pygame.image.load('assets/tiles/floor_1.png').convert()

        self.engine = engine
        self.impassable = pygame.sprite.Group()

        world_size = (self.get_width() * league.Settings.tile_size, self.get_height() * league.Settings.tile_size)

        player = Player(self, 0, 0, 0)
        player.world_size = world_size
        player.rect = player.image.get_rect()
        player._layer = 1

        self.player = player

        engine.objects.append(player)
        engine.drawables.add(player)

        #Add overlay to scene
        self.overlay = Overlay(player)
        if scene_index == 0:
            self.overlay.tutorial = True

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
                    self.__pressure_plate_sounds.append(False)
                elif color == TileType.goblin.value:
                    g = Enemy(scene, 0, x * TILE_WIDTH, y * TILE_HEIGHT)
                    g.world_size = world_size
                    g.rect = g.image.get_rect()
                    g._layer = 1
                    g.x = x * TILE_WIDTH
                    g.y = y * TILE_HEIGHT

                    # Destinations added for testing. Would likely be better to handle this somewhere else or make pre built patterns.
                    g.destinations.append(Vector3(g.x, g.y, 0))
                    g.destinations.append(Vector3(g.x + 256, g.y, 0))
                    g.destinations.append(Vector3(g.x + 256, g.y - 128, 0))
                    g.destinations.append(Vector3(g.x - 128, g.y, 0))

                    engine.objects.append(g)
                    engine.drawables.add(g)
                    self.__enemies.append(g)
                    self.impassable.add(g)


        # Pre-render that data to a surface to save performance.
        self.image = self.render_background()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())

        # Only add the impassable blocks at the end so nothing else can be added.
        for c in self.__crates:
            for im in self.impassable:
                if c is not im:
                    c.blocks.add(im)
        for g in self.__enemies:
            g.blocks.add(self.impassable, self.__crates)
            self.numEnemies += 1
        player.blocks.add(self.impassable, self.__crates, self.__enemies)
        for c in self.__crates:
            c.blocks.add(self.__crates, self.__enemies)

        # Move the player to the starting position.
        player.x = self.get_starting_x()
        player.y = self.get_starting_y()


    def render_background(self):
        background = pygame.Surface((self.__width * TILE_WIDTH, self.__height * TILE_HEIGHT))
        for x in range(0, self.__width):
            for y in range(0, self.__height):
                tile = self.__background[x][y]
                # Always draw the floor tile no matter what.
                background.blit(self.__floor, (x * TILE_WIDTH, y * TILE_HEIGHT))
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
                    if not self.__pressure_plate_sounds[idx]:
                        # INSERT SOUND HERE!!!
                        pygame.mixer.Channel(3).play(pygame.mixer.Sound('assets/Music/Scrape Effects/scrape-4.wav'))
                        pass
                    self.__pressure_plate_sounds[idx] = True
                    states[idx] = True
            idx += 1
        for s in states:
            if not s:
                return False

        if self.numEnemies > 0:
            return False
        if self.scene_not_done:
            pygame.mixer.Channel(3).play(pygame.mixer.Sound('assets/Music/Victory/gmae.wav'))
            self.scene_not_done = False
        # Check that the player is by the door.
        dist = pygame.Vector2((self.__end_x, self.__end_y)).distance_to(pygame.Vector2((self.player.x, self.player.y)))
        if self.__background[self.__end_x // TILE_WIDTH][self.__end_y // TILE_HEIGHT] != TileType.open_end:
            self.__background[self.__end_x // TILE_WIDTH][self.__end_y // TILE_HEIGHT] = TileType.open_end
            self.image = self.render_background()
        if dist > 40:
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

    def addRanged(self, x, y, direction, source, damage = 10, melee=False):
        bullet = range_shot.Ranged_Shot(0, x, y, self, direction, source, damage, melee)
        bullet._layer = 1
        bullet.blocks.add(self.impassable, self.__crates, self.player)
        self.engine.objects.append(bullet)
        self.engine.drawables.add(bullet)

    def despawnObject(self, toDelete):
        try:
            self.engine.objects.remove(toDelete)
            self.engine.drawables.remove(toDelete)
            if type(toDelete) is Enemy:
                self.__enemies.remove(toDelete)
                self.numEnemies -= 1
            if type(toDelete) is NPC_crate:
                self.__crates.remove(toDelete)

            for o in e.objects:
                o.blocks.remove(toDelete)
            try:
                self.impassable.remove(toDelete)
            except:
                pass
        except:
            pass

    def reset(self):
        reset_room()