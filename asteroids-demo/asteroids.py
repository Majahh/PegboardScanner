#!/usr/bin/env python3

import math
import asyncio
from random import randrange, uniform
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import gamepad

LEDWIDTH=64
LEDHEIGHT=64
blue = graphics.Color(0, 0, 255)
white = graphics.Color(255, 255, 255)
        
class Object():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xvel = 0
        self.yvel = 0
        self.radius = 0

    def move(self):
        self.x += self.xvel
        self.y += self.yvel
        if self.x < 0:
            self.x = LEDWIDTH
        if self.x > LEDWIDTH:
            self.x = 0
        if self.y < 0:
            self.y = LEDHEIGHT
        if self.y > LEDHEIGHT:
            self.y = 0

    def collision(self, obj):
        return ((self.x - obj.x)**2 + (self.y - obj.y)**2
                   <= (self.radius + obj.radius)**2)
            
class Rock(Object):
    def __init__(self):
        super(Rock, self)
        self.x = randrange(0, 64)
        self.y = randrange(0, 64)
        self.xvel = uniform(-0.4, 0.4)
        self.yvel = uniform(-0.4, 0.4)
        self.radius = 1

    def draw(self, canvas):
        graphics.DrawCircle(canvas, self.x, self.y, self.radius, white)

class SpaceShip(Object):
    def __init__(self):
        super(SpaceShip, self)
        self.x = LEDWIDTH/2
        self.y = LEDWIDTH/2
        self.xvel = 0
        self.yvel = 0
        self.orientation = -math.pi / 2
        self.radius = 2

    def draw(self, canvas):
        graphics.DrawLine(canvas,
                          self.x + self.radius * math.cos(self.orientation),
                          self.y + self.radius * math.sin(self.orientation), 
                          self.x + self.radius * math.cos(self.orientation + 90),
                          self.y + self.radius * math.sin(self.orientation + 90),
                          blue)
        graphics.DrawLine(canvas,
                          self.x + self.radius * math.cos(self.orientation),
                          self.y + self.radius * math.sin(self.orientation), 
                          self.x + self.radius * math.cos(self.orientation - 90),
                          self.y + self.radius * math.sin(self.orientation - 90),
                          blue)

class Asteroids():
    def __init__(self, gamepad):
        self.gamepad = gamepad
        self.player = SpaceShip()
        self.num_rocks = 10
        self.rocks = []
        for i in range(self.num_rocks):
            self.rocks.append(Rock())

        
        options = RGBMatrixOptions()
        options.hardware_mapping = "regular"
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        options.pwm_lsb_nanoseconds = 130
        #options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        self.matrix = RGBMatrix(options = options)

    def moveObjects(self):
        self.player.move()
        for i in range(len(self.rocks)):
            self.rocks[i].move()
        
    def drawFrame(self):
        canvas = self.matrix.CreateFrameCanvas()
        self.player.draw(canvas)
        for i in range(len(self.rocks)):
            self.rocks[i].draw(canvas)
        offset_canvas = self.matrix.SwapOnVSync(canvas)

    def run(self):
        while True:
            if (self.gamepad.buttons[gamepad.leftCode]):
                self.player.orientation -= 0.125
            elif (self.gamepad.buttons[gamepad.rightCode]):
                self.player.orientation += 0.125
            elif (self.gamepad.buttons[gamepad.upCode]):
                self.player.xvel += 0.0125 * math.cos(self.player.orientation)
                self.player.yvel += 0.0125 * math.sin(self.player.orientation)

            for i in range(len(self.rocks)):
                if self.player.collision(self.rocks[i]):
                    self.player = SpaceShip()
                    break
            self.moveObjects()
            self.drawFrame()

if __name__ == "__main__":
    gamepad_thread = gamepad.GamePad("/dev/input/event0")
    gamepad_thread.setDaemon(True)
    gamepad_thread.start()

    asteroids = Asteroids(gamepad_thread)
    asteroids.run()
