# Точка входа в игру, инициализация и запуск игрового цикла
import pygame as pg
import settings               # Конфигурационные настройки игры
import move
from game.engine import GameEngine  # Основные механики игры
from game.levels_game import Levels_game


if __name__ == '__main__':
    pg.init()
    settings = settings.Settings()
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    pg.display.set_caption(settings.caption)

    if settings.show_move:
        move.run_move(screen)

    game = GameEngine(settings)
    message = game.run(screen)

    # Запуск основного цикла игры
    level = Levels_game(settings)
    formated_time, elapsed_time = level.run_game(screen)

    # Завершение работы
    print("Время игры:", formated_time, "Милисекунд:", elapsed_time)

    pg.quit()

