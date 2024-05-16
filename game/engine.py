# Основные механики игры
import pygame as pg
import time
from game.resources import load_resources, load_music
from game.input_handler import handle_events


class GameEngine:
    x = 235
    y = 28

    def __init__(self):
        self.clock = pg.time.Clock()
        self.font28, self.font22, self.bg, self.kolobok, self.lisa, self.medved, self.zayac = load_resources()
        self.medved = pg.transform.flip(self.medved, True, False)  # Отражение по горизонтали

    def run(self, screen):
        load_music()
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.125)
        running = True
        while running:
            running = handle_events()
            if running == 'L':
                self.x -= 1
            if running == 'R':
                self.x += 1
            if running == 'U':
                self.y -= 1
            if running == 'D':
                self.y += 1
            self.update(screen)
            self.render(screen)
            pg.display.flip()
            self.clock.tick(60)

    def update(self, screen):
        # Обновление состояния игры, если необходимо
        pass

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        t = int(time.time() * 10 % 4)
        screen.blit(self.kolobok, (self.x, self.y + t))
        screen.blit(self.lisa, (10, 360))
        screen.blit(self.medved, (730, 460))
        screen.blit(self.zayac, (950, 400))
        screen.blit(self.font28.render('Помогите колобку вернуться домой!', True, pg.Color(0, 0, 0)), (340, 267))
        screen.blit(self.font22.render('Управление колобком клавишами W, A, S, D', True, pg.Color(0, 0, 0)), (500, 620))
