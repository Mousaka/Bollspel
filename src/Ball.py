#!/usr/bin/env python
# -*- coding: cp1252 -*-
'''
Created on 6 jul 2013

@author: krille
'''
import pygame
import math

class Ball:

    '''
    classdocs
    '''


    def __init__(self, screen, (x, y), size):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0,0,255)
        self.thickness = 0
        self.screen=screen
        self.speed = 6
        self.angle = math.pi/7
        
    def updatePos(self, x,y):
        self.x = x
        self.y = y
        
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.bounce()
        
    def bounce(self):
        if self.x< self.size:
            self.x = self.size #Flyttar bollen till början av avgränsningen ifall den hunnit åka utanför
            self.angle = - self.angle
        elif self.x> (self.screen.get_width()-self.size):
            self.x = (self.screen.get_width()-self.size)
            self.angle = - self.angle
        if self.y< self.size:
            self.y = self.size
            self.angle = math.pi- self.angle
        elif self.y> (self.screen.get_height()-self.size):
            self.y = (self.screen.get_height()-self.size)
            self.angle = math.pi- self.angle
        
    def display(self):
        pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
        