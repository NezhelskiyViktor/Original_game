import pygame as pg
import time
import game.resources as res
from game.input_handler import InputHandler
from game.state_manager import StateManager
import volume_settings as vs
import mini_menu as mini

class GameEngine:
    kolobok_height = 50
    old_kolobok_x = 260
    old_kolobok_y = 28
    kolobok_x = old_kolobok_x
    kolobok_y = old_kolobok_y
    # Параметры платформ
    top_platform_y = old_kolobok_y + kolobok_height
    bottom_platform_y = 650
    top_platform_length = 300
    bottom_platform_length = 1400
    kolobok_running = False
    # Физические параметры
    gravity = 5
    new_x_speed = 5
    x_speed = 0
    y_speed = -1
    falling = False
    time_elapsed = 0

    def __init__(self):
        self.clock = pg.time.Clock()
        self.font28, self.font22, self.font18 = res.load_fonts()
        self.bg = res.load_background()
        self.kolobok, self.lisa, self.medved, self.zayac = res.load_images()
        self.state_manager = StateManager()

    def run(self, screen):
        res.load_music()
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.125)
        handler = InputHandler()
        running = True
        while running:
            running = handler.handle_events(self.state_manager)
            if self.state_manager.state == 'menu':
                self.go_menu(screen)
            elif self.state_manager.state == 'game':
                if running == 'L':
                    running = True
                    self.kolobok_x = self.old_kolobok_x
                    self.kolobok_y = self.old_kolobok_y
                    self.x_speed = 0
                    self.kolobok_running = False
                elif running == 'R':
                    self.kolobok_x += 1
                elif running == 'U':
                    self.kolobok_y -= 1
                elif running == 'D':
                    self.kolobok_y += 1

                if isinstance(running, str):
                    self.kolobok_running = True
                    self.x_speed = self.new_x_speed

                self.update()
                self.render(screen)
                pg.display.flip()
                self.clock.tick(60)

                if self.kolobok_x > screen.get_width():
                    return 'next_level'

    def update(self):
        if (self.top_platform_length - self.kolobok_height // 2) <= self.kolobok_x and (
                self.kolobok_y + self.kolobok_height) < self.bottom_platform_y:
            self.falling = True  # Колобок падает

        if self.falling:
            self.time_elapsed += 0.2  # Увеличиваем время падения
            self.kolobok_y += (self.y_speed * self.time_elapsed
                               + 0.5 * self.gravity * self.time_elapsed ** 2)

            if self.kolobok_y >= self.bottom_platform_y - self.kolobok_height // 2:
                self.kolobok_y = self.bottom_platform_y - self.kolobok_height
                self.falling = False
                self.time_elapsed = 0

        if self.bottom_platform_length - self.kolobok_height > self.kolobok_x:
            self.kolobok_x += self.x_speed

    def render(self, screen):
        screen.blit(self.bg[0], (0, 0))
        screen.blit(self.medved, (730, 460))
        if not self.kolobok_running:
            t = int(time.time() * 10 % 4)
            screen.blit(self.kolobok[2][-4], (self.kolobok_x, self.kolobok_y - t))
            screen.blit(self.font28.render('Помогите колобку вернуться домой!',
                                           True, pg.Color(0, 0, 0)), (340, 267))
            screen.blit(self.font18.render('Управление колобком клавишами W, A, S, D',
                                           True, pg.Color(0, 0, 0)), (500, 620))
        else:
            screen.blit(self.kolobok[2][(self.kolobok_x // 5) % 31], (int(self.kolobok_x), int(self.kolobok_y)))
        screen.blit(self.lisa, (10, 360))
        screen.blit(self.zayac, (950, 400))

    def go_menu(self, screen):
        diff_level, live_count, game_state = 2, 2, 1
        mini_menu = mini.MiniMenu(screen, 800, 5)
        diff_level, live_count, game_state = mini_menu.run(diff_level, live_count, game_state)
        self.state_manager.state = 'game'

        print(diff_level, live_count, game_state)
