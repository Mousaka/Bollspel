#!/usr/bin/env python
# -*- coding: cp1252 -*-
'''
Created on 4 jul 2013

@author: krille
'''
import pygame, random
import Ball

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
    
    
    
    
