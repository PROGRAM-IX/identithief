import pygame
from pystroke.vex import Vex
from pystroke.vector2 import Vector2

class Packet(Vex):
    def __init__(self, sender, target, value):
        points = [Vector2(10, -5), Vector2(10, 5), 
                  Vector2(-10, 5), Vector2(-10, -5), Vector2(0, 0),
                  Vector2(10, -5), Vector2(-10, -5)]
        Vex.__init__(self, sender.x, sender.y, sender.colour, points, 1)
        self.sender = sender
        self.target = target
        self.value = value
        p = Vector2(target.x, target.y)
        v = self.vector_between(p)
        #print v
        self.x_mod = v.normalised().x * 3
        self.y_mod = v.normalised().y * 3
        self.x += self.x_mod
        self.y += self.y_mod
        self.rotate_to_face_point(p)
    
    def move(self):
        self.x += self.x_mod
        self.y += self.y_mod
