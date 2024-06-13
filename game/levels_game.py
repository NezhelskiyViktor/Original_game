import pygame as pg
import game.physics as ph
from game.physics import Char
import game.resources as res
import game.level_manager as lm
import game.game_database as db


class LevelsGame:

    def __init__(self, settings, game_state, start_ticks):
        self.start_ticks = start_ticks
        self.setting = settings  # настройки игры
        self.clock = pg.time.Clock()  # часы игры
        self.lives = game_state['lives']  # кол-во жизней
        self.score = game_state['score']  # счёт игры
        self.font, _, _, _ = res.load_fonts()  # шрифт для вывода счёта
        self.kolobok_image_left = pg.image.load('res/graphics/kolobok_50x50_left.png')
        self.kolobok_image_right = pg.image.load('res/graphics/kolobok_50x50_right.png')
        self.level_index = game_state['current_level']  # индекс текущего уровня

        # Получаем значения параметров платформ из модуля level_manager
        platforms_list = getattr(lm, f'LEVEL{self.level_index}_PLATFORMS')

        # Получаем значения параметров врагов из модуля level_manager
        enemies_list = getattr(lm, f'LEVEL{self.level_index}_ENEMIES')

        # Получаем значения параметров препятствий из модуля level_manager
        obstacles_list = getattr(lm, f'LEVEL{self.level_index}_OBSTACLES')

        # Получаем значения параметров бонусов из модуля level_manager
        bonuses_list = getattr(lm, f'LEVEL{self.level_index}_BONUSES')

        # print(f"Текущий уровень = {self.level_index} - сообщение при создании уровня")
        # создаю объект класса Level
        self.current_level = lm.Level(self.level_index,
                                      platforms_list,
                                      enemies_list,
                                      obstacles_list,
                                      bonuses_list,
                                      settings)

        # создаю колобка
        self.kolobok = ph.Char(settings, 5, 3, res.load_images_kolobok(), 670, False, 2)
        self.kolobok.rect = self.kolobok.images[0][0].get_rect()
        # Задаем rect так, чтобы он был меньше на 10 пикселей со всех сторон
        self.kolobok.rect.inflate_ip(-10, -10)  # Уменьшаем размеры на 10 пикселей

        # Позиционируем колобка в левый нижний угол
        self.kolobok.rect.x = 30
        self.kolobok.rect.y = settings.screen_height - 90
        # В объект уровня добавляем колобка в список всех спрайтов
        self.current_level.all_sprites.add(self.kolobok)
        # создаю врагов
        self.current_level.create_enemies(enemies_list)
        # создаю бонусы
        self.current_level.crate_bonuses(bonuses_list)
        self.music = settings.music
        self.music_volume = settings.music_volume

    # ОСНОВНОЙ ЦИКЛ ИГРЫ запускается из main.py
    def run_game(self, screen):
        music2 = res.load_music()[1]
        if self.music:
            pg.mixer.music.load(music2)
            pg.mixer.music.set_volume(self.music_volume)
            pg.mixer.music.play(loops=-1)

        # создание уровня методом объекта класса Level модуля level_manager.py
        self.current_level.create_level()

        # Создаю табло времени
        time_box = lm.TextBox("00:00", 1000, 20)
        self.current_level.all_sprites.add(time_box)

        points = lm.PointsBox(self.score, (600, 20))
        self.current_level.all_sprites.add(points)

        running = True
        while running:
            # Держим цикл на правильной скорости
            self.clock.tick(self.setting.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False  # завершение игры через нажатие на крестик

            # Считаем прошедшее время с начала игры
            time_box.elapsed_time = pg.time.get_ticks() - self.start_ticks
            # time_box.formatted_time = time_box.format_time(time_box.elapsed_time)
            time_box.text = time_box.format_time(time_box.elapsed_time)

            # движение врагов
            Char.general_call("autorun", self.current_level.platforms)

            # Обработка нажатий клавиш
            keys = pg.key.get_pressed()
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                # self.kolobok.image = self.kolobok_image_left
                self.kolobok.vector = -1
                if self.kolobok.rect.left > 0:
                    self.kolobok.rect.x -= self.kolobok.h_speed
            if keys[pg.K_d] or keys[pg.K_RIGHT]:
                # self.kolobok.image = self.kolobok_image_right
                self.kolobok.vector = 1
                if self.kolobok.rect.right < self.setting.screen_width:
                    self.kolobok.rect.x += self.kolobok.h_speed
            if keys[pg.K_SPACE] or keys[pg.K_UP]:
                self.kolobok.jump()

            # ищем землю под колобком
            if self.kolobok.find_nearest_platform(self.current_level.platforms):
                self.kolobok.current_ground_y = (
                    self.kolobok.find_nearest_platform(
                        self.current_level.platforms
                    )[1])

            # проверяем столкновения с врагами
            self.lives = self.kolobok.check_hit_enemy(
                self.current_level.enemies_sprites_group,
                self.lives,
                self.current_level
            )
            if self.lives == 0:
                return False, time_box.text, self.lives, self.score, self.level_index

            # проверяем столкновения с бонусами (здесь level_completed = True означает окончание уровня)
            level_completed, self.score = (
                self.kolobok.check_get_bonus(
                    self.current_level.bonuses_sprites_group,
                    self.score
                ))

            if level_completed:
                self.level_index += 1
                db.update_game_state(
                    self.setting.difficulty_level,
                    self.level_index,
                    self.score,
                    time_box.text,
                    self.lives)
                # переход на следующий уровень, а не закрытие окна по крестику
                return running, time_box.text, self.lives, self.score, self.level_index

            # Рендеринг
            points.update_value(self.score)
            self.current_level.update()
            if self.lives > 0:
                self.current_level.draw(screen, self.lives, self.score)
                # После отрисовки всего, переворачиваем экран
                pg.display.flip()

        # Заканчиваем игру по закрытию окна по нажатию на крестик
        db.update_game_state(
            self.setting.difficulty_level,
            self.level_index,
            self.score,
            time_box.text,
            self.lives)
        print(f"Записано состояние игры поcле основного цикла в levels_game. self.current_level = {self.level_index}")
        return running, time_box.text, self.lives, self.score, self.level_index

        #pg.quit()
