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

    #game = GameEngine(settings)
    #message = game.run(screen)

    '''
    чисто на время отладки

    db.update_game_state(
        settings.difficulty_level,
        1,
        0,
        0,
        5)
        '''


    # Проверка номера текущего уровня. Если > 4, то начинаем с первого
    game_state = db.get_game_state()
    level_index = game_state['current_level']
    #print(f'Текущий уровень = {level_index} - сообщени при старте программы')
    if level_index > 4:
        level_index = 1
        db.update_game_state(                   # здесь надо обнулить все настройки, потому что начинается новая игра
            settings.difficulty_level,
            1,
            0,
            0,
            5)
        #print(f"Записано состояние игры, т.к. текущий уровень > 4. self.current_level = {level_index}")
    # Запуск основного цикла игры
    while level_index <=4:
        #print(f'Текущий уровень = {level_index} (сообщение изнутри основного цикла while в main)')
        game = Levels_game(settings, db.get_game_state())
        formatted_time, lives, score, level_index = game.run_game(screen)
        #level_index += 1

        # Завершение работы
    print(f'Все уровни пройдены, текущий уровень = {level_index}')
    print(f"Время игры: {formatted_time}, набрано {score} очков. Количество жизней: {lives}.")

    db.update_settings(
        settings.music,
        settings.sound,
        settings.music_volume,
        settings.sound_volume,
        settings.show_move,
        settings.difficulty_level)

    db.update_game_state(
        settings.difficulty_level,
        level_index,
        score,
        formatted_time,
        lives)
    #print(f"Записано состояние игры перед выходом. self.current_level = {level_index}")
    pg.quit()

