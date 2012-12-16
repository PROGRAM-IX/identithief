import pygame
from it_game_engine import ITGameEngine
from pystroke.game import Game

class IdentiThief(Game):
    def __init__(self, width, height):
        Game.__init__(self, width, height)
        
    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.engine = ITGameEngine(self.screen)
        self.engine.run()
        
def main():
    game = IdentiThief(800, 600)
    game.start()
    
if __name__ == "__main__":
    main()