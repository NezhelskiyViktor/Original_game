# Точка входа в игру, инициализация и запуск игрового цикла
import pygame as pg
import settings               # Конфигурационные настройки игры
import move
import game.game_database as db  #
from game.engine import GameEngine  # Основные механики игры
from game.levels_game import Levels_game
import game.end_game as end


if __name__ == '__main__':
    pg.init()
    settings = settings.Settings()
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    pg.display.set_caption(settings.caption)
    formatted_time = "00:00"
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

    '''
    чисто на время отладки

    db.update_game_state(
        settings.difficulty_level,
        1,
        0,
        0,
        5)
        '''


    game_state = db.get_game_state()
    level_index = game_state['current_level']
    # Если в мини меню выбрана новая игра или текущий уровень больше 4, то начинаем с первого
    if settings.game_state == 0 or level_index > 4:
        level_index = 1
        settings.game_state = 1   # В следующий раз в меню пусть будет сохраненная игра
        db.update_game_state(                   # здесь надо обнулить все настройки, потому что начинается новая игра
            settings.difficulty_level,
            1,
            0,
            0,
            5)

    # Запуск основного цикла игры
    running = True
    while running and level_index <=4:
        game = Levels_game(settings, db.get_game_state())
        running, formatted_time, lives, score, level_index = game.run_game(screen)

    # Завершение работы
    db.update_settings(
        settings.music,
        settings.sound,
        settings.music_volume,
        settings.sound_volume,
        settings.show_move,
        settings.difficulty_level
    )

    db.update_game_state(
        settings.difficulty_level,
        level_index,
        score,
        formatted_time,
        lives)

    if running:
        end_game = end.End_game(settings)
        end_game.run(screen)

    print(f'Все уровни пройдены, текущий уровень = {level_index}')
    print(f"Время игры: {formatted_time}, набрано {score} очков. Количество жизней: {lives}.")
    #print(f"Записано состояние игры перед выходом. self.current_level = {level_index}")
    pg.quit()

