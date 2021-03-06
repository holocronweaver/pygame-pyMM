
# Copyright (C) Johan Ceuppens 2010-2013
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pygame
from pygame.locals import *
from gameobject import *
from stateimagelibrary import *
import random
from time import *
from math import *
from rng import *

class HeatMansFlamerow1(Gameobject):
    ""
    def __init__(self,xx,yy,direction):
	Gameobject.__init__(self, xx, yy)
        self.w = 20 
        self.h = 80 
        self.hitpoints = 2000003

	self.startx = xx
	self.starty = yy
        
        self.yy = yy
    
        self.image = pygame.image.load('./pics/heatman-flamerow-1.bmp').convert()
        self.image.set_colorkey((0,0,255))
        
	self.direction = direction 

        self.crawling = 1
        self.up = 0

    def draw(self, screen, room):
            screen.blit(self.image, (self.x-40, self.starty + room.relativey)) # NOTE starty
	    
    def update(self,room,player):
	if self.direction == "left":
		self.x -= 10 
		if self.x < self.startx - 600:
			return 1
	elif self.direction == "right":
		self.x += 10
		if self.x > self.startx + 600:
			return 1
	return 0
	
    def collide(self, room, player):
        # FIX BUG
        #print 'gameobject x=%d y=%d player x=%d y=%d' % (self.x,self.y,player.x-room.relativex,player.y-room.relativey)
	if (player.x-room.relativex > self.x-self.w  and 
	player.x-room.relativex < self.x+self.w+self.w and 
	player.y-room.relativey > self.y-self.h and 
	player.y-room.relativey < self.y + self.h +self.h):
	    print "player collision with Flame!"
	    return 1 
	else:
	    return 0 ## for game self.talker

    def collide(self, room, o):
	if (o.x-room.relativex > self.x-self.w  and 
	o.x-room.relativex < self.x+self.w+self.w and 
	o.y-room.relativey > self.y-self.h and 
	o.y-room.relativey < self.y + self.h +self.h):
	    print "go collision with Bullet!"
	    return 1 
	else:
	    return 0 ## for game self.talker


    def fight(self,room,player,keydown = -1):
        1
