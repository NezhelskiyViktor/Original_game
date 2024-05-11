# Точка входа в игру, инициализация и запуск игрового цикла

import pygame as pg
from game.engine import GameEngine  # Основные механики игры
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
    game = GameEngine()
    game.run()
    pg.quit()

