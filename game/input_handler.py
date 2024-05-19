# Обработка пользовательского ввода
import pygame as pg

class InputHandler:
    def handle_events(self, state_manager):
        # for event in pg.event.get():
        #     if event.type == pg.QUIT:
        #         state_manager.running = False
        #
        for event in pg.event.get():
            if event.type == pg.QUIT:
                state_manager.running = False
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return False

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            direction = 'L'
        elif keys[pg.K_d]:
            direction = 'R'
        elif keys[pg.K_w]:
            direction = 'U'
        elif keys[pg.K_s]:
            direction = 'D'
        else:
            direction = True

        return direction

