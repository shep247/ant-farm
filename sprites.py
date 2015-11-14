import pygame
from pygame.locals import *
from thespian.actors import Actor, ActorExitRequest, WakeupMessage
from random import randint
from datetime import timedelta
from settings import (MAX_X, MIN_X, MAX_Y, MIN_Y)


class StartSprite(object):
    def __init__(self, drawer, boundaries):
        self.drawer = drawer
        self.boundaries = boundaries


class SpriteAction(object):
    def __init__(self, img, xpos, ypos):
        self.img = img
        self.xpos = xpos
        self.ypos = ypos


class AddSprite(SpriteAction):
    pass


class MoveSprite(SpriteAction):
    pass


class RemoveSprite(SpriteAction):
    pass


class MoveSpriteTo(SpriteAction):
    def __init__(self, xpos, ypos, destSpriteAddr):
        super(MoveSpriteTo, self).__init__(None, xpos, ypos)
        self.destSprite = destSpriteAddr


class AntSpriteActor(Actor):
    def __init__(self):
        self.img         = ''
        self.xpos        = 10
        self.ypos        = 10
        self.increment   = 2
        self.clockwise   = True
        self.boundaries  = []
        self.destination = (None, None, None)  # (xpos, ypos, spriteAddr)
        self.oldDestination = (None, None, None)
        self.going_home = False
        self.posVert = 1 if randint(0,1) == 1 else -1
        self.directionCount = 60
        self.drawer = None
        
    def receiveMessage(self, message, sender):
        if isinstance(message, StartSprite):
            self.drawer = message.drawer
            self.boundaries = message.boundaries
            self.send(message.drawer, AddSprite(self.img, self.xpos, self.ypos))
            self.wakeupAfter(timedelta(milliseconds=20))
        elif isinstance(message, MoveSpriteTo):
            self.destination = (message.xpos, message.ypos, message.destSprite)

        elif isinstance(message, WakeupMessage):
            self._do_move()
            self.send(self.drawer, MoveSprite(self.img, self.xpos, self.ypos))
            self.wakeupAfter(timedelta(milliseconds=30))
        elif isinstance(message, ActorExitRequest):
            self._remove_from_drawer()
            
    def _do_move(self):
        if self.destination[0]:
            # move to the destination
            xsteps, ysteps = self._get_xy_steps()
            self.xpos = self._get_new_pos(self.xpos, self.destination[0], xsteps)
            self.ypos = self._get_new_pos(self.ypos, self.destination[1], ysteps)
            if self.xpos == self.destination[0] and \
               self.ypos == self.destination[1]:
                self._reset_destination()
        else:
            # move randomly
            self._move_sprite()
                
    def _remove_from_drawer(self):
        self.send(self.drawer, RemoveSprite(self.img, self.xpos, self.ypos))

    @static
    def _get_new_pos(self, pos, dest_pos, maxnum_of_steps):
        if pos != dest_pos:
            difference = pos - dest_pos
            direction = 1 if difference < 0 else -1
            increment = direction * min(maxnum_of_steps, abs(difference))
            return increment + pos
        return pos

    def _get_xy_steps(self):
        xdifference = abs(self.xpos - self.destination[0])
        ydifference = abs(self.ypos - self.destination[1])
        total_diff = xdifference + ydifference
        xsteps = int((xdifference / total_diff) * self.increment)
        ysteps = self.increment - xsteps
        return xsteps, ysteps
    
    def _reset_slope(self):
        self.posVert = 1 if randint(0,1) == 1 else -1
        self.posHoriz = 1 if randint(0,1) == 1 else -1
    
    def _move_sprite(self):
        self.xpos = max(min(self.posHoriz*self.increment + self.xpos, MAX_X), MIN_X)
        self.ypos = max(min(self.posVert*self.increment + self.ypos, MAX_Y), MIN_Y)
        self._reverse_direction()
        
    def _reset_destination(self):
        if self.going_home:
            self.destination = self.oldDestination
            self.going_home = False
        else:
            # self.send(self.destination[2], ActorExitRequest())
            self.going_home = True
            self.oldDestination = self.destination
            self.destination = (self.home_x_pos, self.home_y_pos, self.myAddress)
        
    def _reverse_direction(self):
        if self.directionCount == 0: 
            self.directionCount = randint(8,20)
            self._reset_slope()
        else:
            self.directionCount -= 1


class RedAntSpriteActor(AntSpriteActor):
    def __init__(self):
        super(RedAntSpriteActor, self).__init__()
        self.img = 'redAnt.png'
        self.home_x_pos = MIN_X + 65
        self.home_y_pos = MAX_Y/2 + 40 
        self.xpos = self.home_x_pos
        self.ypos = self.home_y_pos
        self.posHoriz = 1


class BlackAntSpriteActor(AntSpriteActor):
    def __init__(self):
        super(BlackAntSpriteActor, self).__init__()
        self.img = 'blackAnt.png'
        self.home_x_pos = MAX_X - 65
        self.home_y_pos = MAX_Y/2 + 40
        self.xpos = self.home_x_pos
        self.ypos = self.home_y_pos
        self.posHoriz = -1
