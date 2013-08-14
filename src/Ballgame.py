#!/usr/bin/env python
# -*- coding: cp1252 -*-
'''
Created on 4 jul 2013

@author: krille
'''
import ConfigParser, pygame, Ball

MAP_TILE_WIDTH, MAP_TILE_HEIGHT = 24, 16
SCREEN_SIZE = (800, 300)

class Game(object):
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.pressed_key = None
        self.mainloop = True
        self.b1 = Ball.Ball(self.screen, (150, 50), 15)
        self.fps = 60
    
    def use_level(self, level):
        #Set level
        self.overlays = pygame.sprite.RenderUpdates()
        
    
    def control(self):
        keys = pygame.key.get_pressed()
        
        def pressed(key): #kollar om knapp är nedtryckt
            return self.pressed_key == key or keys[key]
        
        
        if pressed(pygame.K_DOWN):
            self.b1.dribble('d')
        if pressed(pygame.K_ESCAPE):
            self.mainloop = False
        self.pressed_key = None
        
    def main(self):
        clock = pygame.time.Clock()
        
        background, overlay_dict = level.render()
        overlays = pygame.sprite.RenderUpdates()
        for (x, y), image in overlay_dict.iteritems():
            overlay = pygame.sprite.Sprite(overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
        self.screen.blit(background, (0, SCREEN_SIZE[1]-100))
        
        overlays.draw(self.screen)
        #self.screen.blit(self.background, (0,0))
        self.screen.fill([255,255,255])
        pygame.display.flip()
        m = 0
        #mainloop
        while self.mainloop:
            self.control()
            pygame.display.set_caption("Game of Ball FPS: %.2f" % (clock.get_fps()))
            self.screen.fill((255,255,255))
            #overlays.draw(self.screen)
           # self.screen.blit(background, (0, SCREEN_SIZE[1]-100))
            self.screen.blit(background, (800+m, 0))
            m -= 1
            self.b1.move()
            self.b1.display()
            pygame.display.update()
            clock.tick(self.fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.mainloop = False
                elif event.type == pygame.KEYDOWN:
                    self.pressed_key = event.key
                    

'''
Created on 12 aug 2013

@author: krille
'''

import ConfigParser, pygame

class Level(object):
    
    def __init__(self, filename = "lvl1.map"):
        self.tileset =''
        self.map=[]
        self.items = {}
        self.key = {}
        self.width = 5
        self.load_file(filename)
        
        
    def load_file(self, filename="lvl1.map"):
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)
        for y, line in enumerate(self.map):
            for x, c in enumerate(line):
                if not self.is_wall(x, y) and 'sprite' in self.key[c]:
                    self.items[(x, y)] = self.key[c]

    def get_tile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}
        
    def get_bool(self, x, y, name):
      #  """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_wall(self, x, y):
        """Is there a wall?"""

        return self.get_bool(x, y, 'wall')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')
    

    def render(self):
        wall = self.is_wall
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    # Draw different tiles depending on neighbourhood
                    if not wall(map_x, map_y+1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            tile = 1, 2
                        elif wall(map_x+1, map_y):
                            tile = 0, 2
                        elif wall(map_x-1, map_y):
                            tile = 2, 2
                        else:
                            tile = 3, 2
                    else:
                        if wall(map_x+1, map_y+1) and wall(map_x-1, map_y+1):
                            tile = 1, 1
                        elif wall(map_x+1, map_y+1):
                            tile = 0, 1
                        elif wall(map_x-1, map_y+1):
                            tile = 2, 1
                        else:
                            tile = 3, 1
                    # Add overlays if the wall may be obscuring something
                    if not wall(map_x, map_y-1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            over = 1, 0
                        elif wall(map_x+1, map_y):
                            over = 0, 0
                        elif wall(map_x-1, map_y):
                            over = 2, 0
                        else:
                            over = 3, 0
                        overlays[(map_x, map_y)] = tiles[over[0]][over[1]]
                else:
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 3
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
        return image, overlays

class TileCache(object):
    
    def __init__(self, width=32, height=None):
        self.width = width
        self.height = height or width
        self.cache = {}
        
    def __getitem__(self, filename):
        #Returns a table of tiles
        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width, self.height)
            self.cache[key] = tile_table
            return tile_table
        
    def _load_tile_table(self, filename, width, height):
            #Load image and split into tiles
            
            image = pygame.image.load(filename).convert()
            image_width, image_height = image.get_size()
            tile_table=[]
            
            for tile_x in range(0,image_height/height):
                line =[]
                tile_table.append(line)
                for tile_y in range(0, image_height/height):
                    Rect = (tile_x*width, tile_y*height, width, height)
                    line.append(image.subsurface(Rect))
            return tile_table        
            
if __name__ == "__main__":
    MAP_CACHE = TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)
    level = Level()
    level.load_file('lvl1.map')
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    Game().main()
    