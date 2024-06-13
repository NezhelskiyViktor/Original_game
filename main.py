# Точка входа в игру, инициализация и запуск игрового цикла
import pygame as pg
import settings               # Конфигурационные настройки игры
import move
import game.game_database as db  #
from game.engine import GameEngine  # Основные механики игры
from game.levels_game import LevelsGame
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
    # Начало игры с колобком на дереве и настройками игры
    game = GameEngine(settings)
    message = game.run(screen)
    # Обращиемся к базе данных за значениями сохранёнными после предыдущей игры
    game_state = db.get_game_state()
    level_index = game_state['current_level']  # Индекс текущего уровня
    # Если в мини меню выбрана новая игра или текущий уровень больше 3, то начинаем с первого уровня
    if settings.game_state == 0 or level_index > 3:
        level_index = 1
        settings.game_state = 1   # В следующий раз в меню пусть будет сохраненная игра
        db.update_game_state(     # здесь надо обнулить все настройки, потому что начинается новая игра
            settings.difficulty_level,
            1,
            0,
            0,
            5)

    # Запуск основного цикла игры
    time_start = pg.time.get_ticks()  # время начала игры
    running = True
    while running and level_index <= 3:
        game = LevelsGame(settings, db.get_game_state(), time_start)
        running, formatted_time, lives, score, level_index = game.run_game(screen)

    # Сохраняем настройки мини-меню в базу данных
    db.update_settings(
        settings.music,
        settings.sound,
        settings.music_volume,
        settings.sound_volume,
        settings.show_move,
        settings.difficulty_level
    )

    # Сохраняем состояние игры в базу данных
    lives = 5 if lives == 0 else lives
    db.update_game_state(
        settings.difficulty_level,
        level_index,
        score,
        formatted_time,
        lives)

    if running:  # Если игра завершена не через закрытие окна, то выходим на окно успешного окончания.
        end_game = end.End_game(settings)
        end_game.run(screen)
        # print('Все уровни пройдены')

#    print(f"Текущий уровень = {level_index}, Время игры: {formatted_time}, \
#     набрано {score} очков. Количество жизней: {lives}.")

    pg.quit()

