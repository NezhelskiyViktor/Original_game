import pygame as pg
import game.resources as res


class MiniMenu:
    # Параметры изменений
    difficulty_levels = [1, 2, 3, 4]
    sound = ["выкл", "вкл"]
    music = ["выкл", "вкл"]
    sound_volume = [0.125, 0.25, 0.5, 1.0]
    music_volume = [0.125, 0.25, 0.5, 1.0]
    game_states = ["новая", "сохраненная"]

    # Изначальные значения
    difficulty_index = 0
    sound_index = 0
    music_index = 0
    s_v_index = 0
    m_v_index = 0
    game_state_index = 0

    # Индекс активного элемента (0 - сложность, 1 - звук, 2 - музыка и т.д.)
    active_index = 0

    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 300
        self.height = 190
        self.subsurface = screen.subsurface((x, y, self.width, self.height))  # Создание мини-окна
        _, _, _, self.font18 = res.load_fonts()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def run(self, installations):
        diffi_level, game_state, sound, music, sound_volume, music_volume = installations
        self.difficulty_index = diffi_level
        self.sound_index = 1 if sound else 0
        self.music_index = 1 if music else 0
        self.s_v_index = self.sound_volume.index(sound_volume)
        self.m_v_index = self.music_volume.index(music_volume)
        self.game_state_index = game_state

        running = True
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_UP:
                        self.active_index = (self.active_index - 1) % 7
                    elif event.key == pg.K_DOWN:
                        self.active_index = (self.active_index + 1) % 7
                    elif event.key == pg.K_RIGHT:
                        if self.active_index == 0:
                            self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulty_levels)
                        if self.active_index == 1:
                            self.sound_index = (self.sound_index + 1) % len(self.sound)
                        elif self.active_index == 2:
                            self.music_index = (self.music_index + 1) % len(self.music)
                        elif self.active_index == 3:
                            self.s_v_index = (self.s_v_index + 1) % len(self.sound_volume)
                        elif self.active_index == 4:
                            self.m_v_index = (self.m_v_index + 1) % len(self.music_volume)
                        elif self.active_index == 5:
                            self.game_state_index = (self.game_state_index + 1) % len(self.game_states)

                    elif event.key == pg.K_LEFT:
                        if self.active_index == 0:
                            self.difficulty_index = (self.difficulty_index - 1) % len(self.difficulty_levels)
                        if self.active_index == 1:
                            self.sound_index = (self.sound_index - 1) % len(self.sound)
                        elif self.active_index == 2:
                            self.music_index = (self.music_index - 1) % len(self.music)
                        elif self.active_index == 3:
                            self.s_v_index = (self.s_v_index - 1) % len(self.sound_volume)
                        elif self.active_index == 4:
                            self.m_v_index = (self.m_v_index - 1) % len(self.music_volume)
                        elif self.active_index == 5:
                            self.game_state_index = (self.game_state_index - 1) % len(self.game_states)

            self.draw()
            pg.display.flip()
            clock.tick(60)

        return (self.difficulty_index, self.game_state_index,
                self.sound_index, self.music_index, self.sound_volume[self.s_v_index],
                self.music_volume[self.m_v_index])

    def draw(self):
        yellow = (250, 250, 0)
        red = (20, 0, 0)

        # Очистка подокна
        self.subsurface.fill((77, 180, 80, 0))  # Прозрачный фон

        # Отрисовка неизменяемых текстов
        self.draw_text('Уровень сложности', self.font18, red, self.subsurface, 10, 5)
        self.draw_text('Звуки', self.font18, red, self.subsurface, 10, 35)
        self.draw_text('Музыка', self.font18, red, self.subsurface, 10, 65)
        self.draw_text('Громкость звуков', self.font18, red, self.subsurface, 10, 95)
        self.draw_text('Громкость музыки', self.font18, red, self.subsurface, 10, 125)
        self.draw_text('Игра', self.font18, red, self.subsurface, 10, 155)

        # Отрисовка изменяемых текстов
        self.draw_text(str(self.difficulty_levels[self.difficulty_index]), self.font18,
                       yellow if self.active_index == 0 else red, self.subsurface, 250, 5)
        self.draw_text(self.sound[self.sound_index], self.font18,
                       yellow if self.active_index == 1 else red, self.subsurface, 120, 35)
        self.draw_text(self.music[self.music_index], self.font18,
                       yellow if self.active_index == 2 else red, self.subsurface, 120, 65)
        self.draw_text(str(self.sound_volume[self.s_v_index]), self.font18,
                       yellow if self.active_index == 3 else red, self.subsurface, 200, 95)
        self.draw_text(str(self.music_volume[self.m_v_index]), self.font18,
                       yellow if self.active_index == 4 else red, self.subsurface, 200, 125)
        self.draw_text(self.game_states[self.game_state_index], self.font18,
                       yellow if self.active_index == 5 else red, self.subsurface, 120, 155)
