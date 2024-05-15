# Основные механики игры
import pygame as pg
import time
from game.resources import load_resources
from game.input_handler import handle_events


class GameEngine:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.font28, self.font22, self.bg, self.kolobok, self.lisa = load_resources()

    def run(self, screen):
        running = True
        while running:
            running = handle_events()
            self.update(screen)
            self.render(screen)
            pg.display.flip()
            self.clock.tick(60)

    def update(self, screen):
        # Обновление состояния игры, если необходимо
        pass

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        t = int(time.time()*10 % 4)
        screen.blit(self.kolobok, (235, 28 + t))
        screen.blit(self.lisa, (10, 360))
        screen.blit(self.font28.render('Помогите колобку вернуться домой!', True, pg.Color(0, 0, 0)), (340, 267))
        screen.blit(self.font22.render('Управление колобком клавишами W, A, S, D', True, pg.Color(0, 0, 0)), (500, 620))


