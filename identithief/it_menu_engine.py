import pygame
from pygame.locals import *
from pystroke.hud import *
from pystroke.vector2 import Vector2

from pystroke.game_engine import GameEngine

class ITMenuEngine(GameEngine):
    def __init__(self, screen):
        GameEngine.__init__(self, screen)
        self.FPS = 60
        
    def update(self):
        self.event_e.update()
        if self.event_e.input.mouse_buttons[1] == True:
            print "Switching from menu"
            return 0
        if self.event_e.input.mouse_buttons[3] == True:
            print "Quitting from menu"
            return 1
        self.clock.tick(self.FPS)
    
    def draw(self):
        self.draw_e.begin_draw(pygame.Color(0,0,0))
        self.draw_e.draw([self._hud])
        self.draw_e.end_draw()
        
    def run(self):
        self._hud.add(HUDText("GameTitle", pygame.Color(255, 255, 255), 
                              "identithief", (100, 200), 4, 2))
        self._hud.add(HUDText("Instructions1", pygame.Color(255, 255, 255),
                              "left click to start", (100, 350), 2, 2))
        self._hud.add(HUDText("Instructions", pygame.Color(255, 255, 255),
                              "right click to exit", (100, 450), 2, 2))
        self._hud.add(HUDText("AuthorName", pygame.Color(255, 255, 255),
                              "by program_ix", (200, 500), 1, 2))
        self._hud.add(HUDPolygon("Envelope", pygame.Color(0, 255, 0), 
                                 ((500, 50), (650, 50), 
                                  (575, 125), (500, 50),
                                  (500, 150), (650, 150),
                                  (650, 50), 2)))
        self._hud.add(HUDLine("CrossOut", pygame.Color(255, 0, 0), 
                              ((480, 170), (670, 30), 2)))
        while True:
            r = self.update()
            if r == 0 or r == 1:
                self.event_e.input.keys = [False]*1024
                return r
            self.draw()