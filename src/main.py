#!/usr/bin/env python
# -*- coding: cp1252 -*-
'''
Created on 4 jul 2013

@author: krille
'''
import pygame, random
import Ball

def main():
    

    pygame.init()
     
    screen = pygame.display.set_mode([700,300])
    screen.fill([255,255,255])
    print type(screen)
    mainloop, x, y, color, fontsize, delta, fps =  True, 25 , 0, (32,32,32), 35, 1, 60 
    Clock = pygame.time.Clock()
    b1 = Ball.Ball(screen, (150, 50), 15)
    while mainloop:
        tickFPS = Clock.tick(fps)
        x = 100
        y = 100
        pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (Clock.get_fps()))
        fontsize = 50
        myFont = pygame.font.SysFont("None", fontsize)
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        screen.fill((255,255,255))
        b1.move()
        b1.display()
        screen.blit(myFont.render("I love pygame!", 0, (color)), (10,10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # Be IDLE friendly!
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # Be IDLE friendly!
        pygame.display.update()
     
    pygame.quit() # Be IDLE friendly!

if __name__ == '__main__':
    main()