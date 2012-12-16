import pygame

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
        self.send_mod = 240
        self.send_count = randint(0, self.send_mod)
        self.send_next = False
        self.identity = identity
        self.captured = []
        self.stolen = False
        self.nit_width = 20/len(self.identity)
        
    def update(self):
        if not self.stolen:
            if self.send_count % self.send_mod == 0:
                self.send_next = True
            self.send_count += 1
    
    def draw(self, surface):
        Vex.draw(self, surface)
        if not self.stolen:
            pos = -10 + self.nit_width/2
            for i in xrange(0, len(self.identity)):
                if i in self.captured:
                    pygame.draw.line(surface, self.colour, 
                    (self.x + pos, self.y + 0), 
                    (self.x + pos + self.nit_width/2, self.y + 0), 2)
                pos += self.nit_width
        else:
            pygame.draw.line(surface, self.colour,
            (self.x - 30, self.y - 30), (self.x + 30, self.y + 30),
            2)
            pygame.draw.line(surface, self.colour,
            (self.x + 30, self.y - 30), (self.x - 30, self.y + 30),
            2)    
        
    def send(self, target):
        self.send_next = False
        return Packet(self, target, choice(self.identity))
    
    def sniff(self, value):
        if value in self.identity:
            if self.identity.index(value) not in self.captured:
                self.captured.append(self.identity.index(value))
            
    def receive(self, packet):
        packet.sender.delivered(packet.value)
        
    def delivered(self, value):
        if self.identity.index(value) in self.captured:
            self.captured.remove(self.identity.index(value))        
            
    def steal(self):
        self.stolen = True