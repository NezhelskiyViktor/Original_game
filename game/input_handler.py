# Обработка пользовательского ввода
import pygame as pg

class InputHandler:
    def handle_events(self, state_manager):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    state_manager.state = 'game'
                elif event.key == pg.K_F1:
                    state_manager.state = 'menu'
                elif event.key in (pg.K_w, pg.K_UP):
                    return 'U'
                elif event.key in (pg.K_s, pg.K_DOWN):
                    return 'D'
                elif event.key in (pg.K_a, pg.K_LEFT):
                    return 'L'
                elif event.key in (pg.K_d, pg.K_RIGHT):
                    return 'R'
        return True

