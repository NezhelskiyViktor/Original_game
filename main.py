# Точка входа в игру, инициализация и запуск игрового цикла
import pygame as pg
from game.engine import GameEngine  # Основные механики игры
import settings               # Конфигурационные настройки игры


if __name__ == '__main__':
    pg.init()
    settings = settings.Settings()
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    pg.display.set_caption(settings.caption)

    # Запуск основного цикла игры
    game = GameEngine()
    message = game.run(screen)
    print(message)

    pg.quit()

