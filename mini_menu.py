import pygame as pg
import game.resources as res


class MiniMenu:
    # Параметры изменений
    difficulty_levels = [1, 2, 3, 4]
    lives_counts = [1, 2, 3, 4]
    game_states = ["новая", "сохраненная"]
    # Изначальные значения
    difficulty_index = 0
    lives_index = 0
    game_state_index = 0
    # Индекс активного элемента (0 - сложность, 1 - жизни, 2 - игра)
    active_index = 0

    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 300
        self.height = 100
        self.subsurface = screen.subsurface((x, y, self.width, self.height))  # Создание мини-окна
        _, _, self.font18 = res.load_fonts()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def run(self, diffi_level, live_count, game_state):
        self.difficulty_index = diffi_level
        self.lives_index = live_count
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
                    elif event.key == pg.K_TAB:
                        self.active_index = (self.active_index + 1) % 3
                    elif event.key == pg.K_RIGHT:
                        if self.active_index == 0:
                            self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulty_levels)
                        elif self.active_index == 1:
                            self.lives_index = (self.lives_index + 1) % len(self.lives_counts)
                        elif self.active_index == 2:
                            self.game_state_index = (self.game_state_index + 1) % len(self.game_states)
                    elif event.key == pg.K_LEFT:
                        if self.active_index == 0:
                            self.difficulty_index = (self.difficulty_index - 1) % len(self.difficulty_levels)
                        elif self.active_index == 1:
                            self.lives_index = (self.lives_index - 1) % len(self.lives_counts)
                        elif self.active_index == 2:
                            self.game_state_index = (self.game_state_index - 1) % len(self.game_states)

            self.draw()
            pg.display.flip()
            clock.tick(60)

        return self.difficulty_index, self.lives_index, self.game_state_index

    def draw(self):
        yellow = (250, 250, 0)
        red = (20, 0, 0)

        # Очистка подокна
        self.subsurface.fill((77, 180, 80, 0))  # Прозрачный фон

        # Отрисовка неизменяемых текстов
        self.draw_text('Уровень сложности', self.font18, red, self.subsurface, 10, 5)
        self.draw_text('Кол-во жизней', self.font18, red, self.subsurface, 10, 35)
        self.draw_text('Игра', self.font18, red, self.subsurface, 10, 65)

        # Отрисовка изменяемых текстов
        self.draw_text(str(self.difficulty_levels[self.difficulty_index]), self.font18,
                       yellow if self.active_index == 0 else red, self.subsurface, 250, 5)
        self.draw_text(str(self.lives_counts[self.lives_index]), self.font18,
                       yellow if self.active_index == 1 else red, self.subsurface, 250, 35)
        self.draw_text(self.game_states[self.game_state_index], self.font18,
                       yellow if self.active_index == 2 else red, self.subsurface, 150, 65)

