# pygame imports
import pygame

# thespian imports
from thespian.actors import Actor, ActorExitRequest

from crumbs import StartCrumb, CrumbSpriteActor
from settings import SPRITE_SIZE, SURFACE_Y_SIZE


class ClickData(object):
    def __init__(self, click_pos, sprite_data, message, drawer):
        self.xpos, self.ypos = click_pos
        self.spriteData = sprite_data
        self.message = message
        self.drawer = drawer


class ClickNotifier(Actor):
    
    def receiveMessage(self, message, sender):
        if isinstance(message, ClickData):
            if message.ypos < SURFACE_Y_SIZE:
                self._send_to_clicked_sprite(message)
            
    def _send_to_clicked_sprite(self, message):
        removed_sprite = False
        for spriteAddr in message.spriteData:
            if self._is_in_range(message.xpos, message.spriteData[spriteAddr][1]) \
               and self._is_in_range(message.ypos, message.spriteData[spriteAddr][2]):
                self.send(spriteAddr, message.message)
                removed_sprite = True
        if not removed_sprite:
            crumb = self.createActor(CrumbSpriteActor)
            crumb_starter = StartCrumb(message.xpos - 80, message.ypos - 80,
                                      message.spriteData, message.drawer)
            self.send(crumb, crumb_starter)
            
    def _is_in_range(self, clickPos, spritePos):
        return spritePos < clickPos < spritePos + SPRITE_SIZE
