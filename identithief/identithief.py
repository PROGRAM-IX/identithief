import pygame
from it_game_engine import ITGameEngine
from it_menu_engine import ITMenuEngine
from pystroke.event_engine import EventEngine
from pystroke.input_engine import InputEngine
from pystroke.game import Game

class IdentiThief(Game):
    def __init__(self, width, height):
        Game.__init__(self, width, height)
        
    def start(self):
        pygame.init()
        self.bg_music = pygame.mixer.Sound("assets/identithief.wav")
        self.input_e = InputEngine()
        self.event_e = EventEngine(self.input_e)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("IdentiThief")
        self.engines = [ITMenuEngine(self.screen), ITGameEngine(self.screen)]
        for e in self.engines:
            e.event_e = self.event_e
        self.bg_music.play(-1)
        self.engine = self.engines[0]
        while self.engine.run() == 0:
            if self.engines.index(self.engine) < len(self.engines) - 1:
                self.engine = self.engines[self.engines.index(self.engine) + 1]
            else:
                self.engine = self.engines[0]
        raise SystemExit
        
def main():
    game = IdentiThief(800, 600)
    game.start()
    
if __name__ == "__main__":
    main()