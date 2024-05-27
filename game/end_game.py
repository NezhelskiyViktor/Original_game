import pygame as pg
import time
import game.resources as res


class End_game:
    kolobok_height = 50
    old_kolobok_x = -50
    old_kolobok_y = 600
    kolobok_x = old_kolobok_x
    kolobok_y = old_kolobok_y
    # Параметры платформ
    bottom_platform_y = 650
    bottom_platform_length = 1400
    kolobok_running = True
    # Физические параметры
    x_speed = 5
    time_elapsed = 0
    etap = 0
    def __init__(self, settings):
        self.settings = settings
        self.clock = pg.time.Clock()
        _, self.font28, _, self.font18 = res.load_fonts()
        self.bg = res.load_background()[4], res.load_background()[5]
        self.kolobok, _, _, _ = res.load_images()
        self.music = self.settings.music
        self.music_volume = self.settings.music_volume

    def run(self, screen):
        music1 = res.load_music()[0]
        if self.music:
            pg.mixer.music.load(music1)
            pg.mixer.music.play(loops=-1)
            pg.mixer.music.set_volume(self.music_volume)
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            self.time_elapsed += 1
            if self.time_elapsed > 600:
                running = False
            self.kolobok_x += self.x_speed
            self.render(screen)
            if self.etap == 0:
                if self.kolobok_x > screen.get_width():
                    self.etap += 1
                    self.kolobok_x = -50
                    self.kolobok_y = 343
            else:
                if self.kolobok_x > 210:
                    self.kolobok_x = 233
                    self.x_speed = 0
                    self.kolobok_running = False
            self.clock.tick(60)

    def render(self, screen):
        screen.blit(self.bg[self.etap], (0, 0))
        if not self.kolobok_running:
            screen.blit(self.kolobok[0], (self.kolobok_x, self.kolobok_y))
            screen.blit(self.font28.render('Колобок вернулься домой!',
                                           True, pg.Color(255, 0, 0)), (340, 5))
        else:
            screen.blit(self.kolobok[2][(self.kolobok_x // 5) % 31], (int(self.kolobok_x), int(self.kolobok_y)))

        pg.display.flip()

