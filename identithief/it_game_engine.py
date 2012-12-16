import pygame
from pygame.locals import *
from pystroke.hud import *
from pystroke.game_engine import GameEngine
from pystroke.vector2 import Vector2
from pystroke.vex import Vex

from packet import Packet
from victim import Victim

from random import randint, choice



class ITGameEngine(GameEngine):
    def __init__(self, screen):
        GameEngine.__init__(self, screen)
        self.FPS = 60
        self.computers = []
        self.packets = []
        self.score = 0
        self.high_score = 0
        self.m1_down = False
        self.computers.append(Victim(400, 300, pygame.Color(99, 99, 0), "DUR?"))
        self.computers.append(Victim(300, 200, pygame.Color(0, 255, 0), "HNG!"))
        self.computers.append(Victim(100, 400, pygame.Color(255, 0, 0), "BLA."))
        self.computers.append(Victim(500, 100, pygame.Color(0, 0, 255), "WFK$"))
    def update(self):
        self.event_e.update()
        if self.event_e.input.keys[K_ESCAPE] == True:
            raise SystemExit
        if self.event_e.input.mouse_buttons[1] == True:
            if not self.m1_down:
                self.packets.append(Packet(self.computers[0], 
                                           self.computers[1],
                                           choice(self.computers[0].identity)))
                self.m1_down = True
        else:
            self.m1_down = False
        
        self.update_computers()
        self.update_packets()
        self.collide()
        
        self.clock.tick(self.FPS)
    
    def draw(self):
        self.draw_e.begin_draw(pygame.Color(0,0,0))
        self.draw_e.draw(self.computers)
        self.draw_e.draw(self.packets)
        self.draw_e.draw([self._hud])
        self.draw_e.end_draw()
        
    def run(self):
        self._hud.add(HUDPolygon("Box1", pygame.Color(255, 255, 255),
                                  ((50, 50), (750, 50), 
                                  (750, 550), (50, 550), 2)))
        self._hud.add(HUDText("GameName", pygame.Color(255, 255, 255),
                               "identithief", (15, 20), 1, 2))
        self._hud.add(HUDText("Instructions", pygame.Color(255, 255, 255),
                               "click on packets to steal identities", (15, 575), 
                               1, 2))
        while True:
            self.update()
            self.draw()
            
    def update_computers(self):
        for c in self.computers:
            c.update()
            if c.send_next and len(self.computers) > 1:
                target = self.computers[0]
                while target is c:
                    target = choice(self.computers)
                self.packets.append(c.send(target))
    
    def update_packets(self):
        for p in self.packets:
            p.move()
            
    def collide(self):
        v = None
        for p in self.packets:
            v = Vector2(p.x, p.y)
            for c in self.computers:
                if p.target is c and c.point_inside(v):
                    print p.value
                    self.packets.remove(p)
                    
    