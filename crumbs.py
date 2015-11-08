from thespian.actors import Actor, WakeupMessage
from datetime import timedelta
from sprites import AddSprite, MoveSpriteTo

class AddCrumbSprite(AddSprite): pass

class UpdateSpriteLocations(object):
    def __init__(self, allSprites):
        self.sprites = allSprites

class StartCrumb(object):
    def __init__(self, xpos, ypos, allsprites, drawer):
        self.xpos = xpos
        self.ypos = ypos
        self.sprites = allsprites
        self.drawer = drawer

class CrumbSpriteActor(Actor):
    def __init__(self):
        self.img = 'crumb.png'
        self.xpos = 10
        self.ypos = 10
        self.sprites = {} #senderAddr:(img, xpos, ypos)
        self.notifiedSprites = []
        self.drawer = None
        
    def receiveMessage(self, message, sender):
        if isinstance(message, WakeupMessage):
            self._notifySpritesInRange()
            self.wakeupAfter(timedelta(milliseconds=30))
        elif isinstance(message, UpdateSpriteLocations):
            self.sprites = message.sprites
        elif isinstance(message, StartCrumb):
            self.xpos = message.xpos
            self.ypos = message.ypos
            self.sprites = message.sprites
            self.drawer = message.drawer
            self.send(self.drawer, AddCrumbSprite(self.img, self.xpos, self.ypos))
            self._notifySpritesInRange()
            self.wakeupAfter(timedelta(milliseconds=30))
        
    def _notifySpritesInRange(self):
        for sprite in self.sprites:
            if sprite in self.notifiedSprites:
                continue
            _, spritexpos, spriteypos = self.sprites[sprite]
            if self._sprite_in_range(spritexpos, spriteypos):
                '''send the sprite a new destination'''
                self.send(sprite, MoveSpriteTo(self.xpos+80, 
                                               self.ypos+80, 
                                               self.myAddress))
                self.notifiedSprites.append(sprite)
        
    def _sprite_in_range(self, spritexpos, spriteypos):    
        return (self.xpos <= spritexpos <= self.xpos + 160) and \
           (self.ypos <= spriteypos <= self.ypos + 160)
