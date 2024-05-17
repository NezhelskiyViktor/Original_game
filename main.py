# Точка входа в игру, инициализация и запуск игрового цикла
import time
import pygame as pg
import move
from game.engine import GameEngine  # Основные механики игры
import game.resources as res       # Загрузка ресурсов

import settings               # Конфигурационные настройки игры
import game.state_manager      # Управление состояниями игры
import game.input_handler      # Обработка пользовательского ввода
import game.level_manager      # Загрузка и управление уровнями
import game.physics            # Физический движок
import game.persistence        # Управление сохранениями
import ui.ui_manager         # Управление пользовательским интерфейсом
import ui.components         # Компоненты интерфейса


if __name__ == '__main__':
    pg.init()
    font28, font22 = res.load_fonts()
    window_width, window_height = 1200, 720
    screen = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption("Оригинальная игра")

    # Показ видеозаставки начала игры
    move.run_move(screen)

    # Запуск основного цикла игры
    game = GameEngine()
    game.run(screen)

    pg.quit()

