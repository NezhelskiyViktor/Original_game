import pygame as pg
import time
import game.resources as res
from game.input_handler import InputHandler
from game.state_manager import StateManager
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

    def __init__(self, settings):
        self.clock = pg.time.Clock()
        _, self.font28, _, self.font18 = res.load_fonts()
        self.bg = res.load_background()[0]
        self.kolobok = res.load_images_kolobok()
        self.lisa = pg.image.load('res/graphics/lisa.png')  # .convert_alpha()
        self.zayac = pg.image.load('res/graphics/zayac.png')
        self.medved = pg.image.load('res/graphics/medved_01.png')
        self.state_manager = StateManager()
        self.settings = settings
        self.set_settings()

    def set_settings(self):
        self.sound = self.settings.sound
        self.sound_volume = self.settings.sound_volume
        self.music = self.settings.music
        self.music_volume = self.settings.music_volume
        self.show_move = self.settings.show_move

    def run(self, screen):

        sound1 = pg.mixer.Sound(res.load_sound()[0])
        music1 = res.load_music()[0]
        use_sound = True

        if self.music:
            pg.mixer.music.load(music1)
            pg.mixer.music.play(loops=-1)
            pg.mixer.music.set_volume(self.music_volume)
        handler = InputHandler()
        running = True
        while running:
            running = handler.handle_events(self.state_manager)
            if self.state_manager.state == 'menu':
                self.go_menu(screen)
                self.set_settings()
                pg.mixer.music.stop()
                if self.settings.music:
                    pg.mixer.music.load(music1)
                    pg.mixer.music.set_volume(self.music_volume)
                    pg.mixer.music.play(loops=-1)

            elif self.state_manager.state == 'game':
                if running == 'L':
                    running = True
                    self.kolobok_x = self.old_kolobok_x
                    self.kolobok_y = self.old_kolobok_y
                    self.x_speed = 0
                    self.kolobok_running = False
                    use_sound = True
                elif running == 'R':
                    self.kolobok_x += 1
                elif running == 'U':
                    self.kolobok_y -= 1
                elif running == 'D':
                    self.kolobok_y += 1

                if isinstance(running, str):
                    self.kolobok_running = True
                    self.x_speed = self.new_x_speed
                    if use_sound and self.sound:
                        sound1.set_volume(self.sound_volume)
                        sound1.play()
                        use_sound = False

                self.update()
                self.render(screen)
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
        t = int(time.time() * 10 % 4) - 2
        screen.blit(self.bg, (0, 0))
        screen.blit(self.medved, (730, 460))
        if not self.kolobok_running:
            # t = int(time.time() * 10 % 4)
            screen.blit(self.kolobok[1][1], (self.kolobok_x, self.kolobok_y - t))
            screen.blit(self.font28.render('Помогите колобку вернуться домой!',
                                           True, res.YELLOW), (340, 267 + t))
            # screen.blit(self.font18.render('Управление колобком клавишами W, A, S, D',
            #                                True, res.BLUE), (500, 620))
        else:
            screen.blit(self.kolobok[0][(self.kolobok_x // 5) % 12], (int(self.kolobok_x), int(self.kolobok_y)))
        screen.blit(self.lisa, (10, 360))
        screen.blit(self.zayac, (950, 400))

        pg.display.flip()

    def go_menu(self, screen):
        installations = (
            self.settings.difficulty_level,
            self.settings.game_state,
            self.settings.sound,
            self.settings.music,
            self.settings.sound_volume,
            self.settings.music_volume,
            self.settings.show_move
        )

        mini_menu = mini.MiniMenu(screen, 800, 5)
        installations = mini_menu.run(installations)

        self.state_manager.state = 'game'
        (self.settings.difficulty_level,
         self.settings.game_state,
         self.settings.sound,
         self.settings.music,
         self.settings.sound_volume,
         self.settings.music_volume,
         self.settings.show_move
         ) = installations
        return
