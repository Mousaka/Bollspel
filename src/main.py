#!/usr/bin/env python
# -*- coding: cp1252 -*-
'''
Created on 4 jul 2013

@author: krille
'''
import pygame, random
import Ball


MAP_TILE_WIDTH, MAP_TILE_HEIGHT = 24, 16

def load_tile_table(filename, width, height):
    pygame.display.set_mode((1,1), pygame.NOFRAME)
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table

def main():
    
    MAP_TILE_WIDTH = 24
    MAP_TILE_HEIGHT = 16
    MAP_CACHE = {
    'ground.png': load_tile_table('ground.png', MAP_TILE_WIDTH,
                                      MAP_TILE_HEIGHT),
    }
    pygame.init()
    K_DOWN = False
    K_UP = False
    K_LEFT = False
    K_RIGHT = False
    
    table = load_tile_table("img/ground2.png", 24, 16)
    screen = pygame.display.set_mode([700,300])
    screen.fill([255,255,255])
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile, (x*32, y*24))
    mainloop, x, y, color, fontsize, delta, fps =  True, 25 , 0, (32,32,32), 35, 1, 60 
    Clock = pygame.time.Clock()
    b1 = Ball.Ball(screen, (150, 50), 15)
    pygame.display.flip()
    while mainloop:
        tickFPS = Clock.tick(fps)
        x = 100
        y = 100
        pygame.display.set_caption("Game of Ball FPS: %.2f" % (Clock.get_fps()))
        fontsize = 50
        myFont = pygame.font.SysFont("None", fontsize)
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        screen.fill((255,255,255))
        b1.move()
        b1.display()
       # screen.blit(myFont.render("Bounce that shit!", 0, (color)), (10,10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    K_DOWN = True
                if event.key == pygame.K_RIGHT:
                    K_RIGHT = True
                if event.key == pygame.K_LEFT:
                    K_LEFT = True
                elif event.key == pygame.K_ESCAPE:
                    mainloop = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    K_DOWN = False
                if event.key == pygame.K_LEFT:
                    K_LEFT = False
                if event.key == pygame.K_RIGHT:
                    K_RIGHT = False
                
        if K_DOWN:
            b1.dribble('d')
        if K_LEFT:
            b1.dribble('l')
        if K_RIGHT:
            b1.dribble('r')
                    
        pygame.display.update()
     
    pygame.quit() # Be IDLE friendly!

if __name__ == '__main__':
    main()
    
    
    
    

import ConfigParser, pygame

class Level(object):
    def load_file(self, filename="img/level.map", MAP_TILE_WIDTH, MAP_TILE_HEIGHT):
        self.map = []
        self.key = {}
        self.MAP_TILE_WIDTH = MAP_TILE_WIDTH
        self.MAP_TILE_HEIGHT = MAP_TILE_HEIGHT
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