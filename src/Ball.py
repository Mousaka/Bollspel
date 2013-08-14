#!/usr/bin/env python
# -*- coding: cp1252 -*-
'''
Created on 6 jul 2013

@author: krille
'''
import pygame
import math
gravity = (math.pi, 0.3)
elasticity = 0.9
drag = 0.999
drib = 0.05 #Hur h�rt man dribblar ner bollen
bottom_boarder_height = 28
directions = {'d': math.pi, 'u': 0, 'r': math.pi/2, 'l': (3*math.pi)/2}

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
    
    def dribble(self, d):
        (self.angle,self.speed) = self.addVectors((self.angle,self.speed), (directions[d], 0.1+ drib*self.speed))
    def keyDown(self):
        (self.angle,self.speed) = self.addVectors((self.angle,self.speed), (math.pi, drib))
 
    def getDownVec(self):
        print - math.cos(self.angle) * self.speed
        return - math.cos(self.angle) * self.speed
        
        
    #Adderar tv� vectorer.
    def addVectors(self, (angle1, length1), (angle2, length2)):
        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
        
        length = math.hypot(x, y) #L�ngden p� nya vectorn

        #Vinkeln p� nya vectorn
        angle = (0.5 * math.pi) - math.atan2(y, x) #atan2 �r arctan som hanterar "y/0".
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
            self.x = self.size #Flyttar bollen till b�rjan av avgr�nsningen ifall den hunnit �ka utanf�r
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
        elif self.y> (self.screen.get_height()-self.size-bottom_boarder_height):   #G�r s� bollen studsar p� "marken"., b�r �ndras s� den studsar n�r den nuddar n�got ist
            self.y = (self.screen.get_height()-self.size-bottom_boarder_height)
            if self.getDownVec() > 5:
                self.speed *= elasticity
            else:
                print "recovering"
             #   self.addVectors((self.angle, self.speed))
            self.angle = math.pi- self.angle
            
        
    def display(self):
        pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
        