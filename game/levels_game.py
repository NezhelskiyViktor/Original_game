import pygame as pg
import game.physics as ph
from game.physics import Char
import game.resources as res
import game.level_manager as lm
import game.game_database as db
import settings

class Levels_game:


    def __init__(self, settings, game_state):
        self.start_ticks = pg.time.get_ticks()
        self.setting = settings
        self.clock = pg.time.Clock()
        self.lives = game_state['lives']
        self.score = game_state['score']
        self.font, _, _, _ = res.load_fonts()
        self.level_index = game_state['current_level']
        platforms_list_name = 'LEVEL{}_PLATFORMS'.format(self.level_index)# Конструируем имя списка платформ как строку
        platforms_list = getattr(lm, platforms_list_name)# Используем getattr для получения соответствующего списка платформ из модуля lm
        enemies_list_name = 'LEVEL{}_ENEMIES'.format(self.level_index)
        enemies_list = getattr(lm, enemies_list_name)
        obstacles_list_name = 'LEVEL{}_OBSTACLES'.format(self.level_index)
        obstacles_list = getattr(lm, obstacles_list_name)
        bonuses_list_name = 'LEVEL{}_BONUSES'.format(self.level_index)
        bonuses_list = getattr(lm, bonuses_list_name)
        print(f"Текущий уровень = {self.level_index} - сообщение при создании уровня")
        self.current_level = lm.Level(self.level_index, platforms_list, enemies_list, obstacles_list, bonuses_list)



        # создаю колобка
        self.kolobok = ph.Char(5, 3, 'res/graphics/kolobok_50x50_right.png', 670)
        #self.kolobok.rect = pg.Rect(30, settings.screen_height - 30, 50, 40)
        # Задаем rect так, чтобы он был меньше на 10 пикселей со всех сторон
        self.kolobok.rect = self.kolobok.image.get_rect()

        self.kolobok.rect.inflate_ip(-10, -10)  # Уменьшаем размеры на 10 пикселей
        #self.kolobok.rect.topleft = (self.kolobok.rect.left + 100, self.kolobok.rect.top + 100) #- этот код не работает(((
        #self.kolobok.rect.move(50,50) # тоже не смещает rect((((

        self.kolobok.rect.x = 30
        self.kolobok.rect.y = settings.screen_height - 90
        self.current_level.all_sprites.add(self.kolobok)

        # создаю врагов
        self.current_level.create_enemies(enemies_list)
        # создаю бонусы
        self.current_level.crate_bonuses(bonuses_list)

        # Количество жизней показываем сердечками
        self.heart = pg.sprite.Group()
        for i in range(self.lives):   #  Количество жизней
            heart = pg.sprite.Sprite()
            heart.image = pg.transform.scale(pg.image.load('res/graphics/heart.png'), (30, 30))   # Масштабирование
            heart.rect = heart.image.get_rect()
            heart.rect.x = 10 + i * heart.rect.width
            heart.rect.y = 10
            self.heart.add(heart)
            self.current_level.all_sprites.add(heart)


    def run_game(self, screen):
        # ОСНОВНОЙ ЦИКЛ ИГРЫ

        # создание уровня
        self.current_level.create_level()#self.level_index)

        # Создаю табло времени
        time_box = lm.TextBox("00:00", 1100, 20)
        self.current_level.all_sprites.add(time_box)

        running = True
        while running:
            # Держим цикл на правильной скорости
            self.clock.tick(self.setting.fps)
            for event in pg.event.get():

                if event.type == pg.QUIT: running = False

            # Считаем прошедшее время с начала игры
            time_box.elapsed_time = pg.time.get_ticks() - self.start_ticks
            time_box.formatted_time = time_box.format_time(time_box.elapsed_time)

            # движение врагов
            Char.general_call("autorun", self.current_level.platforms)

            # Обработка нажатий клавиш
            keys = pg.key.get_pressed()
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                self.kolobok.image = pg.image.load('res/graphics/kolobok_50x50_left.png')
                if self.kolobok.rect.left > 0: self.kolobok.rect.x -= self.kolobok.h_speed
            if keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.kolobok.image = pg.image.load('res/graphics/kolobok_50x50_right.png')
                if self.kolobok.rect.right < self.setting.screen_width: self.kolobok.rect.x += self.kolobok.h_speed
            if keys[pg.K_SPACE] or keys[pg.K_UP]:
                self.kolobok.jump()

            # ищем землю под колобком
            if self.kolobok.find_nearest_platform(self.current_level.platforms):
                self.kolobok.current_ground_y = self.kolobok.find_nearest_platform(self.current_level.platforms)[1]

            # проверяем столкновения с врагами
            self.kolobok.check_hit_enemy(self.current_level.enemies_sprites_group)

            # проверяем столкновения с бонусами (здесь level_completed = True означает окончание уровня)
            level_completed, self.score = self.kolobok.check_get_bonus(self.current_level.bonuses_sprites_group, self.score)
            if level_completed:
                self.level_index += 1
                db.update_game_state(
                    self.setting.difficulty_level,
                    self.level_index,
                    self.score,
                    time_box.formatted_time,
                    self.lives)
                print(
                    f"Записано состояние игры поcле основного цикла в levels_game. self.current_level = {self.level_index}")
                return time_box.formatted_time, self.lives, self.score, self.level_index

            # Рендеринг
            self.current_level.update()
            self.current_level.draw(screen)

            # После отрисовки всего, переворачиваем экран
            pg.display.flip()
        db.update_game_state(
            self.setting.difficulty_level,
            self.level_index,
            self.score,
            time_box.formatted_time,
            self.lives)
        print(f"Записано состояние игры поcле основного цикла в levels_game. self.current_level = {self.level_index}")
        return time_box.formatted_time, self.lives, self.score, self.level_index


        #pg.quit()