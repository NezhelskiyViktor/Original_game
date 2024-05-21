# Точка входа в игру, инициализация и запуск игрового цикла
import pygame as pg
import settings               # Конфигурационные настройки игры
import move
import game.game_database as db  #
from game.engine import GameEngine  # Основные механики игры
from game.levels_game import Levels_game


if __name__ == '__main__':
    pg.init()
    settings = settings.Settings()
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    pg.display.set_caption(settings.caption)

    db.init_database()
    db_settings = db.get_settings()
    settings.difficulty_level = db_settings['difficulty_level']
    settings.music_volume = db_settings['music_volume']
    settings.sound_volume = db_settings['sound_effects_volume']
    settings.sound = db_settings['use_sound_effects']
    settings.music = db_settings['use_music']
    settings.show_move = db_settings['show_intro']

    if settings.show_move:
        move.run_move(screen)

    game = GameEngine(settings)
    message = game.run(screen)

    # Запуск основного цикла игры
    level = Levels_game(settings, lives=4, score=10)
    formated_time, elapsed_time = level.run_game(screen)
    # Завершение работы
    print("Время игры:", formated_time, "Милисекунд:", elapsed_time)

    db.update_settings(
        settings.music,
        settings.sound,
        settings.music_volume,
        settings.sound_volume,
        settings.show_move,
        settings.difficulty_level)

    pg.quit()

