#!/usr/bin/env python
# -*- coding: cp1252 -*-
'''
Created on 6 jul 2013

@author: krille
'''
import pygame
import math
gravity = (math.pi, 0.05)
elasticity = 0.95
drag = 0.999
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
        self.speed = 0
        self.angle = math.pi/2
        
    def updatePos(self, x,y):
        self.x = x
        self.y = y
    
    def keyDown(self):
        (self.angle,self.speed) = self.addVectors((self.angle,self.speed), (math.pi, 1))
 
    #Adderar två vectorer.
    def addVectors(self, (angle1, length1), (angle2, length2)):
        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
        
        length = math.hypot(x, y) #Längden på nya vectorn

        #Vinkeln på nya vectorn
        angle = (0.5 * math.pi) - math.atan2(y, x) #atan2 är arctan som hanterar "y/0".
        #print str(angle1)+", "+str(length1)+ " + "+ str(angle2)+", "+str(length2)+" = "+str(angle)+", "+str(length)
        return (angle, length)
        
    def move(self):
        (self.angle, self.speed) = self.addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        
        self.speed *= drag
        
        self.bounce()
        
    def bounce(self):
        if self.x< self.size:
            self.x = self.size #Flyttar bollen till början av avgränsningen ifall den hunnit åka utanför
            self.angle = - self.angle
            self.speed *= elasticity
        elif self.x> (self.screen.get_width()-self.size):
            self.x = (self.screen.get_width()-self.size)
            self.angle = - self.angle
            self.speed *= elasticity
        if self.y< self.size:
            self.y = self.size
            self.angle = math.pi- self.angle
            self.speed *= elasticity
        elif self.y> (self.screen.get_height()-self.size):
            self.y = (self.screen.get_height()-self.size)
            self.angle = math.pi- self.angle
            self.speed *= elasticity
        
    def display(self):
        pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
        