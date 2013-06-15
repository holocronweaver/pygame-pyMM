#!/usr/local/bin/python
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

from maproom1 import *
from meter import *
from playermegaman import *
from bullet import *

class Game:
    "Main function"
    def __init__(self):
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((640, 480))
        font = pygame.font.SysFont("Times", 14)
        gameover = 0

        askplayers = 0 # NOTE: 2 Player flag
        
        blankimage = pygame.image.load('./pics/blank.bmp').convert()
        ## There are several title screens in the ./pics/ directory
        titleimage = pygame.image.load('./pics/megaman-titlescreen-640x480.bmp').convert()
        self.x = 0
        self.y = 0
        
        self.room = Maproom1(0,0)
        heartmeter = Meter()
        player = PlayerMegaMan(heartmeter)
        pygame.key.set_repeat(10,100)
        self.keydown = 0
        self.inventoryitem = None
        self.inventorymasterkey = None
        self.inventorykey1 = None
        self.inventorykey2 = None
        self.inventoryrubysword = None
        
        self.talker = None
        gameflag = 0
        while gameover == 0:
            pygame.display.update()
            screen.blit(titleimage, (0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    gameover = 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gameover = 1

            
        gameover = 0
        while gameover == 0:
            player.h = 72 ############FIXME NOTE: for ducking
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_z:
                        1###if self.keydown == 2 or player.duck:
                        #    player.fightlow(self.room)
                        #else:
                        #    player.fightmedium(self.room)
                        break
                    # FIXME KLUDGE
            	    self.keydown = 1
                    # player 1 key controls
                    
                    if event.key == K_DOWN:
                        player.duck = 1
                        self.keydown = 2
                        #FIXME keydown = 2
                        #self.room.moveup()    


			### kludge
                    elif event.key == K_LEFT:
			player.prevdirection = player.direction
			player.direction = "left"
                        player.duck = 0
                        self.room.moveright()   
                    elif event.key == K_RIGHT:
                        player.duck = 0
                        self.room.moveleft()    
			player.prevdirection = player.direction
			player.direction = "right"
                    elif event.key == K_x:
                        if player.jumpcounter == 0:
                            player.jump(self.room)  
                    elif event.key == K_c:
                        if player.prevdirection == "left":
				self.room.bullets.append(Bullet(player.x-player.w/2,player.y+20,"left")) 
                        elif player.prevdirection == "right":
				self.room.bullets.append(Bullet(player.x+player.w/2,player.y+20,"right")) 
    
                else:
                    player.direction = "none"
 
            if self.room.collide(player) == 1 or player.hitpoints <= 0: # NOTE: return 1 after player heartmeter runs out (player.hit)
        	endingimage = pygame.image.load('./pics/endingscreen.bmp').convert()
        	while gameover == 0:
	            	pygame.display.update()
        	    	screen.blit(endingimage, (0,0))
            		for event in pygame.event.get():
                		if event.type == QUIT:
                    			return
                		elif event.type == KEYDOWN:
                    			gameover = 1
					return
                		if event.type == pygame.MOUSEBUTTONDOWN:
                    			gameover = 1
					return
				    
            if self.room.collide(player) == 3 or self.room.collide(player) == 2:###Dungeon wall
                f = self.room.fall(player)
                if not f == 2:
                    self.room.movedown()#FIXME
            f = self.room.fall(player)
            if f == 2:
                gameflag = 0
            elif f == 0:
                1#gameflag = 1
            if self.room.collidewithropes(player) == 2:
                
                while gameflag == 0:

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            return
                        elif event.type == KEYDOWN:
            	    
                            # player 1 key controls
                            ##player.draw(screen)
                            ##if event.key == K_z:
                             ##   player.fight(self.room)  
                            if event.key == K_UP:
                                if self.room.collidewithropes(player) == 2:
                                    self.room.movedown()   
                            elif event.key == K_DOWN:
##                              if at the end of the rope, have to jump off  
                                if self.room.collidewithropes(player) == 2:
                                    self.room.moveup()
                            elif event.key == K_RIGHT:
                                self.room.moveleft()
                                gameflag = 1    
                            elif event.key == K_LEFT:
                                self.room.moveright()
                                gameflag = 1
                            elif event.key == K_x:
                                gameflag = 1
                            elif event.key == K_z:
                                gameflag = 1


                    self.room.draw(screen,player)
                    player.update(self.room)
                    player.drawclimbing(screen)
                    self.taskbar.draw()
                    heartmeter.draw(screen) 
                    pygame.display.update()
                    screen.blit(blankimage, (0,0))

            if self.room.collide(player) == 2: # NOTE: return 1 after player heartmeter runs out (player.hit)
                   o = player.hit()
		   if o == 0:
			player.hitpoints = -100###extra
               	   else:
			self.undomovecollide(player)
 
            self.room.draw(screen,player)
            player.update(self.room)
            if self.keydown == 1:
                self.keydown = 0
                player.draw(screen)
            elif self.keydown == 2:
                self.keydown = 2
                player.drawduck(screen)
                player.h = 32
            elif player.direction == "none":
                player.drawstatic(screen)
            
	    sleep(0.05)

	    ### Set player hitpoints in life bar
	    heartmeter.index = player.hitpoints

            for b in self.room.bullets:
		if b.update(self.room, player) == 1:
			self.room.bullets.remove(b)
		else:
			b.draw(screen,self.room)

		for go in self.room.gameobjects:
			if b.collide(self.room,go) == 1:
				self.room.gameobjects.remove(go)
				self.room.bullets.remove(b)

            for o in self.room.gameobjects:
                if o:
                    o.fight(self.room,player,self.keydown)
                    if o.hitpoints <= 0:
                        self.room.removeobject(o)

            if self.talker != None:
                self.talker.talk(screen,font)

            heartmeter.draw(screen)
            
            pygame.display.update()
            screen.blit(blankimage, (0,0))
            roomnumber = self.room.exit(self)
            self.chooseroom(roomnumber,font)

    def undomovecollide(self, player):
            if self.room.collide(player) == 2: # NOTE: return 1 after player heartmeter runs out (player.hit)
		if player.direction == "left":
			self.room.moveleft() 
			self.room.moveleft() 
			self.room.moveleft() 
           	elif player.direction == "right": 
			self.room.moveright() 
			self.room.moveright() 
			self.room.moveright() 
		else:###FIXME move down and up
			self.room.moveup()
			self.room.moveup()
			self.room.moveup()

		if self.room.collide(player) == 2:
			self.undomovecollide(player) 

    def sethitf(self, hitf):
        for i in self.room.gameobjects:
            i.hitf = hitf

    def setxy(self,xx,yy):
        self.x = xx
        self.y = yy

    def chooseroom(self, roomnumber,font):
        if (roomnumber == 0):
            return
        # NOTE: 1_X  woods around haunted castle
        elif (roomnumber == 1):
            self.talker = None
            self.room = Maproom1(self.x,self.y)
        # set sword parameters
        if self.inventoryrubysword:
            self.sethitf(self.room.gameobjects.hit2)
            
if __name__ == "__main__":
    foo = Game()



