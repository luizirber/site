import os.path

import cocos
from cocos.director import director
from cocos.actions import JumpBy, MoveBy, CallFunc, FlipX

from pyglet.window import key

import pyglet

class Level(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, speed=0):
        super(Level, self).__init__()

        self.stopped = pyglet.resource.image('pinutinho-small.png')
        self.stopped.anchor_x = self.stopped.width / 2.
        self.stopped.anchor_y = self.stopped.height / 2.
        
        self.running_1 = pyglet.resource.image('pinutinho_correndo-small-1.png')
        self.running_1.anchor_x = self.running_1.width / 2.
        self.running_1.anchor_y = self.running_1.height / 2.
        
        self.running_2 = pyglet.resource.image('pinutinho_correndo-small-2.png')
        self.running_2.anchor_x = self.running_2.width / 2.
        self.running_2.anchor_y = self.running_2.height / 2.
        
        self.jumping = pyglet.resource.image('pinutinho_pulando-small.png')
        self.jumping.anchor_x = self.jumping.width / 2.
        self.jumping.anchor_y = self.jumping.height / 2.
        
        self.sprite = cocos.sprite.Sprite(self.stopped)

        self.sprite.position = 50, 240

        self.add(self.sprite, z=1)

        self._jumping = False
        self._walking = False
        self._direction = 'Right'

    def start_jumping(self):
        self._jumping = True
        self.sprite.image = self.jumping
        
    def stop_jumping(self):
        self._jumping = False
        self.sprite.image = self.stopped

    def start_walking(self, direction):
        self._direction = direction
        if direction == 'Right':
            self.sprite.image = self.running_1
        else:
            self.sprite.image = self.running_2
        self._walking = True

        
    def stop_walking(self):
        self._walking = False
        if self._jumping:
            self.sprite.image = self.jumping
        else:
            self.sprite.image = self.stopped

    def on_key_press(self, k, m):
        if self._jumping:
            return False

        if k in (key.UP, key.LEFT, key.RIGHT):
            if k == key.UP:
                if self._walking:
                    if self._direction == 'Right':
                        offset = 50
                    else:
                        offset = -50
                    self.sprite.do( CallFunc(self.start_jumping) + 
                                    JumpBy((offset,0), height=50, duration=1) + 
                                    CallFunc(self.stop_jumping) +
                                    CallFunc(self.stop_walking) )
                else:
                    self.sprite.do( CallFunc(self.start_jumping) + 
                                    JumpBy(height=50, duration=1) + 
                                    CallFunc(self.stop_jumping) )
            elif k == key.LEFT:
                self.sprite.do( CallFunc(self.start_walking, 'Left') +
                                MoveBy(delta=(-50, 0), duration=0.5) +
                                CallFunc(self.stop_walking) )
            elif k == key.RIGHT:
                self.sprite.do( CallFunc(self.start_walking, 'Right') +
                                 MoveBy(delta=(50, 0), duration=0.5) +
                                 CallFunc(self.stop_walking) )
            return True
        return False

if __name__ == "__main__":
    director.init(resizable=True)
    # Run a scene with our event displayers:
    director.run( cocos.scene.Scene(Level()) )
