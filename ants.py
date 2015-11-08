#pygame imports
import pygame
from pygame.locals import *

#thespian imports
from thespian.actors import Actor, ActorSystem, ActorExitRequest, WakeupMessage

#std imports
from datetime import timedelta
from collections import namedtuple

#my classes imports
from sprites import AddSprite, MoveSprite, RemoveSprite,\
    StartSprite, RedAntSpriteActor, BlackAntSpriteActor
from crumbs import AddCrumbSprite, UpdateSpriteLocations
from notifiers import ClickNotifier, ClickData
from settings import (SURFACE_X_SIZE, SURFACE_Y_SIZE, FPS, 
                      BLACK, WHITE, GREEN, BLUE, MAX_X, MAX_Y, MIN_X)

class DrawerActor(Actor):
    
    def __init__(self):
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.displaysurf = pygame.display.set_mode((SURFACE_X_SIZE,SURFACE_Y_SIZE), 0, 32)
        pygame.display.set_caption('OMG Ants')
        self._createTextObj(text = "ANTS!")
        self.itemsToDraw = {} #senderAddr:(img, xpos, ypos)
        self.crumbs = {} #senderAddr:(img, xpos, ypos)
        self.ant_hills = {}
        
    def receiveMessage(self, message, sender):
        if isinstance(message, MoveSprite):
            # update the location of a single sprite
            currentLoc = self.itemsToDraw[sender]
            self.itemsToDraw[sender] = (currentLoc[0], message.xpos, message.ypos)
#             self.spriteDestinations[sender] = (img,message)
        elif isinstance(message, WakeupMessage):
            # the normal loop method.  redraw the board, and handle any events
            # the user may have input.
            self._drawBoard()
            self._updateCrumbs()
            self._handleEvents()
            self.fpsClock.tick(FPS)
            self.wakeupAfter(timedelta(milliseconds=30))
        elif isinstance(message, RemoveSprite):
            # remove a sprite from the list, and tell the sprite notifier that 
            # the sprite has been removed
            del self.itemsToDraw[sender]
        elif isinstance(message, AddSprite):
            # add a sprite the items to draw list, then tell the sprite notifier
            # about the new sprite
            img = pygame.image.load(message.img)
            if isinstance(message, AddCrumbSprite):
                self.crumbs[sender] = (img, message.xpos, message.ypos)
            else:
                self.itemsToDraw[sender] = (img, message.xpos, message.ypos)
        elif str(message) == "start":
            self._startSimulation(sender)
            
    def _startSimulation(self, sender):
        self.origSender = sender
        self.wakeupAfter(timedelta(milliseconds=10))
        self.clickNotifier = self.createActor(ClickNotifier)
        self.ant_hills['blackHill'] = (pygame.image.load('Ant_Hill_Black.png'), MAX_X-75, MAX_Y/2)
        self.ant_hills['redHill'] = (pygame.image.load('Ant_Hill_Red.png'), MIN_X, MAX_Y/2)
        
    def _drawBoard(self):
        self.displaysurf.fill(WHITE)
        self.displaysurf.blit(self.textSurfaceObj, self.textRectObj)
        for _ in self.itemsToDraw.values():
            self.displaysurf.blit(_[0], (_[1], _[2]))
        
        for _ in self.ant_hills.values():
            self.displaysurf.blit(_[0], (_[1], _[2]))
            
        for _ in self.crumbs.values():
            self.displaysurf.blit(_[0], (_[1], _[2]))
        
        pygame.display.update()    
        
    def _updateCrumbs(self):
        for crumb in self.crumbs:
            self.send(crumb, UpdateSpriteLocations(self.itemsToDraw))
        
    def _handleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONUP:
                self.send(self.clickNotifier, ClickData(event.pos, self.itemsToDraw, ActorExitRequest(), self.myAddress))
            elif event.type == KEYDOWN:
#               self.send(self.keyNotifier, KeyData(event.key, self.itemsToDraw, self.boundaries, self.myAddress))
                antType = {pygame.K_b: BlackAntSpriteActor,
                           pygame.K_r: RedAntSpriteActor}.get(event.key, None)
                if antType:
                    sprite = self.createActor(antType)
                    self.send(sprite, StartSprite(self.myAddress, []))
            elif event.type == QUIT:
                print("   QUIT")
                pygame.quit()
                self.send(self.origSender, "STOP")
                self.send(self.myAddress, ActorExitRequest())
                #self.send(self.spriteNotifier, ActorExitRequest())  
    
    def _drawDestination(self, destination):
        self.displaysurf.blit(destination[0], (destination[1].xpos, destination[1].ypos))
            
    def _drawBoundary(self, boundary):
        left, top     = boundary[0]
        right, bottom = boundary[1]
        boundaryRect = pygame.Rect(left, top, abs(right-left), abs(bottom-top))
        pygame.draw.rect(self.displaysurf, BLACK, boundaryRect)
    
    def _createTextObj(self, centerLoc=(SURFACE_X_SIZE/2, SURFACE_Y_SIZE/2), text=''):
        fontObj = pygame.font.Font('freesansbold.ttf', 32)
        self.textSurfaceObj = fontObj.render(text, True, GREEN, BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (centerLoc[0], centerLoc[1])

asys = ActorSystem('multiprocQueueBase')
# asys = ActorSystem()
drawerActor = asys.createActor(DrawerActor)

asys.ask(drawerActor, 'start')
print("COMPLETE")
asys.shutdown()


