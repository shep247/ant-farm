#pygame imports
import pygame
from pygame.locals import *

#thespian imports
from thespian.actors import Actor, ActorExitRequest

# from sprites import RemoveDestinationSprite
from crumbs import StartCrumb, CrumbSpriteActor
from settings import SPRITE_SIZE, SURFACE_Y_SIZE
            
class ClickData(object):
    def __init__(self, clickPos, spriteData, message, drawer):
        self.xpos, self.ypos = clickPos
        self.spriteData = spriteData
        self.message = message
        self.drawer = drawer


class ClickNotifier(Actor):
    
    def receiveMessage(self, message, sender):
        if isinstance(message, ClickData):
            if message.ypos < SURFACE_Y_SIZE:
                self._sendToClickedSprite(message)
            
    def _sendToClickedSprite(self, message):
        removedSprite = False
        for spriteAddr in message.spriteData:
            if self._isInRange(message.xpos, message.spriteData[spriteAddr][1]) \
               and self._isInRange(message.ypos, message.spriteData[spriteAddr][2]):
                self.send(spriteAddr, message.message)
                removedSprite = True
        if not removedSprite:
            crumb = self.createActor(CrumbSpriteActor)
            crumbStarter = StartCrumb(message.xpos - 80, message.ypos - 80,
                                      message.spriteData, message.drawer)
            self.send(crumb, crumbStarter)
            
    def _isInRange(self, clickPos, spritePos):
        return spritePos < clickPos < spritePos + SPRITE_SIZE
