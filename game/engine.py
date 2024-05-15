# Основные механики игры
import pygame as pg
import time


class GameEngine:
    def run(self, screen):

        clock = pg.time.Clock()
        font28 = pg.font.Font('res/font/arialbi.ttf', 28)
        font22 = pg.font.Font('res/font/arialbi.ttf', 22)

        bg = pg.image.load('res/graphics/fon_03.jpg').convert()
        kolobok_image = pg.image.load('res/graphics/Kolobok_god_mode.png').convert_alpha()
        kolobok = pg.transform.scale(kolobok_image, (50, 50))  # Масштабирование
        lisa_image = pg.image.load('res/graphics/lisa.png').convert_alpha()
        lisa = pg.transform.scale(lisa_image, (282, 360))  # Масштабирование

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            screen.blit(bg, (0, 0))
            t = int(time.time()*10 % 4)
            print(t)
            screen.blit(kolobok, (235, 28 + t))
            screen.blit(lisa, (10, 360))
            screen.blit(font28.render('Помогите колобку вернуться домой!', True, pg.Color(0, 0, 0)), (340, 267))
            screen.blit(font22.render('Управление колобком клавишами W, A, S, D', True, pg.Color(0, 0, 0)), (500, 620))

            pg.display.flip()
            clock.tick(60)


