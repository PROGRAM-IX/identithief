from pystroke.vex import Vex
from pystroke.vector2 import Vector2
from packet import Packet

from random import choice, randint

class Victim(Vex):
    def __init__(self, x, y, colour, identity):
        points = [Vector2(-20, -20), Vector2(20, -20), Vector2(20, 20), 
                  Vector2(-15, 20), Vector2(-25, 25), Vector2(25, 25), 
                  Vector2(15, 20), Vector2(-20, 20), Vector2(-20, -20),
                  Vector2(-15, -15), Vector2(15, -15), Vector2(15, 15),
                  Vector2(-15, 15), Vector2(-15, -15)]
        Vex.__init__(self, x, y, colour, points, 2)
        self.send_mod = 60
        self.send_count = randint(0, self.send_mod)
        self.send_next = False
        self.identity = identity
        
    def update(self):
        if self.send_count % self.send_mod == 0:
            self.send_next = True
        self.send_count += 1
        
    def send(self, target):
        self.send_next = False
        return Packet(self, target, choice(self.identity))