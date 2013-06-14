
# Copyright (C) Johan Ceuppens 2010
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

class Bullet(Gameobject):
    ""
    def __init__(self,xx,yy,direction):
	Gameobject.__init__(self, xx, yy)
        self.w = 32
        self.h = 32
        self.hitpoints = 2
        
        self.yy = yy
    
        self.image = pygame.image.load('./pics/bullet-1.bmp').convert()
        self.image.set_colorkey((0,0,255))
        
	self.direction = direction 

        self.crawling = 1
        self.up = 0

    def draw(self, screen, room):
            screen.blit(self.image, (self.x-40+room.relativex,self.y+room.relativey))
	    
    def update(self,room,player):
	if self.direction == "left":
		self.x -= 5
	elif self.direction == "right":
		self.x += 5

    def collide(self, room, player):
        # FIX BUG
        #print 'gameobject x=%d y=%d player x=%d y=%d' % (self.x,self.y,player.x-room.relativex,player.y-room.relativey)
	if (player.x-room.relativex > self.x-self.w  and 
	player.x-room.relativex < self.x+self.w+self.w and 
	player.y-room.relativey > self.y-self.h and 
	player.y-room.relativey < self.y + self.h +self.h):
	    print "collision with Deeler!"
	    return 1 
	else:
	    return 0 ## for game self.talker

    def fight(self,room,player,keydown = -1):
        1