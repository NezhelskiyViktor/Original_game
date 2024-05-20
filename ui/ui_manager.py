# Управление пользовательским интерфейсом
#  Здесь будет окно с настройками звуков и музыки в игре
# которое вызывается по клавише F1 выход по клавише ESC, Enter
# Управление клавишами стрелок.
import pygame as pg
import game.resources as res
from game.state_manager import StateManager
from game.input_handler import InputHandler


class UiManager:
    WIDTH, HEIGHT = 200, 200
    SLIDER_WIDTH, SLIDER_HEIGHT = 150, 20
    SLIDER_COLOR = (100, 100, 100)
    HANDLE_COLOR = (255, 0, 0)
    BACKGROUND_COLOR = (255, 255, 255)
    HANDLE_WIDTH = 10
    HANDLE_HEIGHT = SLIDER_HEIGHT
    SLIDER_POSITIONS = [(25, 50), (25, 150)]

    # Ползунки
    class Slider:
        def __init__(self, x, y):
            self.rect = pg.Rect(x, y, SLIDER_WIDTH, SLIDER_HEIGHT)
            self.handle_rect = pg.Rect(x, y, HANDLE_WIDTH, HANDLE_HEIGHT)
            self.value = 0.5  # Начальное значение громкости (50% от ширины ползунка)
            self.update_handle_position()

        def update_handle_position(self):
            self.handle_rect.x = self.rect.x + int(self.value * (SLIDER_WIDTH - HANDLE_WIDTH))

        def draw(self, screen):
            pg.draw.rect(screen, SLIDER_COLOR, self.rect)
            pg.draw.rect(screen, HANDLE_COLOR, self.handle_rect)

        def move_handle(self, direction):
            step = 0.01
            if direction == 'left':
                self.value = max(0, self.value - step)
            elif direction == 'right':
                self.value = min(1, self.value + step)
            self.update_handle_position()

    def __init__(self, screen):
        self.music_volume = 0.125
        self.sound_volume = 0.125
        self.screen = screen
        self.font28, self.font22 = res.load_fonts()

    # Создание ползунков
    sliders = [Slider(*pos) for pos in SLIDER_POSITIONS]
    active_slider_index = 0

    # Главный цикл
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_TAB:
                    active_slider_index = (active_slider_index + 1) % len(sliders)
                elif event.key == pg.K_LEFT:
                    sliders[active_slider_index].move_handle('left')
                elif event.key == pg.K_RIGHT:
                    sliders[active_slider_index].move_handle('right')

        # Отрисовка
        screen.fill(BACKGROUND_COLOR)
        for slider in sliders:
            slider.draw(screen)

        pg.display.flip()
