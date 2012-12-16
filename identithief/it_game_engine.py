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
        self.FPS = 30
        self.computers = []
        self.packets = []
        self.score = 0
        self.high_score = 0
        self.m1_down = False
        self.running = True
        self.dodginess = 0
        self.stolen = 0
        self.paused = False
        self.message_anim = self.FPS * 1.5
        self.anim_count = 0
        self.curr_message = 0
        self.max_dodginess = 5
        self.p_down = False
        self.messages = ["click on packets to steal identities",
                         "four unique packets from one computer will do",
                         "you cannot tell which packet is which",
                         "packets that reach their target nullify stolen ones",
                         "sniffing packets increases dodginess",
                         "if you let the dodginess reach 5 you lose",
                         "dodginess decreases when packets reach their target",
                         "the pips on each screen represent stolen packets"]
        #self.computers.append(Victim(200, 200, pygame.Color(99, 99, 0), "DUR?"))
        #self.computers.append(Victim(600, 200, pygame.Color(0, 255, 0), "HNG!"))
        
        
    def update(self):
        self.event_e.update()
        if self.event_e.input.keys[K_ESCAPE] == True:
            pygame.quit()
            raise SystemExit
        if self.event_e.input.mouse_buttons[1] == True:
            if not self.m1_down:
                self.m1_down = True
        else:
            self.m1_down = False
        if self.event_e.input.keys[K_r] == True:
            if self.paused:
                self.game_reset()
        if self.event_e.input.keys[K_p] == True:
            if not self.p_down:
                self.pause_unpause()
                self.p_down = True
        else:
            self.p_down = False

        if not self.paused:
            self.update_computers()
            self.update_packets()
            self.collide()
            self.update_win()
        
        self.update_message()
        self.clock.tick(self.FPS)
    
    def draw(self):
        self.draw_e.begin_draw(pygame.Color(0,0,0))
        self.draw_e.draw(self.computers)
        self.draw_e.draw(self.packets)
        self.draw_e.draw([self._hud])
        self.draw_e.end_draw()
        
    def run(self):
        self.game_reset()
        while self.running:
            self.update()
            self.draw()
         
    def game_reset(self):
        print "Resetting game"
        del self.computers
        self.computers = []
        del self.packets
        self.packets = []
        self.computers.append(Victim(100, 100, pygame.Color(255, 0, 0), 
                                     "BLA."))
        self.computers.append(Victim(700, 100, pygame.Color(0, 0, 255), 
                                     "WFK$"))
        #self.computers.append(Victim(400, 200, pygame.Color(0, 255, 0), 
        #                             "MLN/"))
        self.computers.append(Victim(100, 500, pygame.Color(0, 255, 255), 
                                     "UYL)"))
        self.computers.append(Victim(700, 500, pygame.Color(255, 255, 0), 
                                     "POT@"))
        del self._hud
        self._hud = HUD()
        self._hud.add(HUDPolygon("Box1", pygame.Color(255, 255, 255),
                                  ((50, 50), (750, 50), 
                                  (750, 550), (50, 550), 2)))
        self._hud.add(HUDText("GameName", pygame.Color(255, 255, 255),
                               "identithief", (15, 20), 1, 2))
        self._hud.add(HUDText("Dodginess", pygame.Color(255, 255, 255),
                               "dodginess " + str(self.dodginess), 
                               (550, 20), 1, 2))
        self._hud.add(HUDText("Messages", pygame.Color(255, 255, 255),
                               self.messages[self.curr_message], (15, 575), 
                               1, 2))
        self.dodge(-self.dodginess)
        self.running = True
        self.paused = False
        self.stolen = 0
        self.anim_count = 0
    
    def pause_unpause(self):
        self.paused = not self.paused
        
    def update_computers(self):
        for c in self.computers:
            c.update()
            if c.send_next and len(self.computers) > 1:
                target = choice(self.computers)
                while target is c:
                    target = choice(self.computers)
                self.packets.append(c.send(target))
                t2 = target
                while t2 is c or t2 is target:
                    t2 = choice(self.computers)
                self.packets.append(c.send(t2)) 
    
    def update_packets(self):
        for p in self.packets:
            p.move()
            
    def update_message(self):
        self.anim_count += 1
        if self.anim_count % self.message_anim == 0:
            if self.curr_message < len(self.messages)-1:
                m = self.curr_message + 1
                self._hud.get("Messages").text = self.messages[m]
                self.curr_message = m
            else:
                self.curr_message = 0
        
    def manage_stolen(self):
        for c in self.computers:
            if len(c.captured) is len(c.identity):
                if not c.stolen:
                    c.steal()
                    self.dodge(-self.dodginess)
                    self.stolen += 1
            
    def update_win(self):
        if self.dodginess < self.max_dodginess:
            self.manage_stolen()
            if self.stolen == len(self.computers) - 1:
                self.game_over(True)   
        else:
            self.game_over(False)
        
    def game_over(self, won):
        if not won:
            print "DODGE ENOUGH"
            self._hud.add(HUDText("GameOver", pygame.Color(255, 0, 0),
                                  "dodge", (250, 300), 5, 6))             
        else:
            print "NICE WAAAAN"
            self._hud.add(HUDText("GameOver", pygame.Color(0, 255, 0),
                                  "niiice", (250, 300), 5, 6))             
        self.paused = True
        
    def dodge(self, num):
        self.dodginess += num
        if self.dodginess < 0:
            self.dodginess = 0
        self._hud.get("Dodginess").text = "dodginess " + str(self.dodginess)
    
    def capture(self, packet):
        print "Captured", packet.value
        packet.sender.sniff(packet.value)
        self.dodge(1)
        self.packets.remove(packet)

    
    def collide(self):
        v = None
        if self.m1_down:
            v = Vector2(self.event_e.input.mouse_pos[0], 
                        self.event_e.input.mouse_pos[1])
            for p in self.packets:
                if p.point_inside(v):
                    self.capture(p)
                    break
                    
        for p in self.packets:
            v = Vector2(p.x, p.y)
            for c in self.computers:
                if p.target is c and c.point_inside(v):
                    #print p.value
                    if not c.stolen:
                        c.receive(p)
                        self.dodge(-1)
                    self.packets.remove(p)
