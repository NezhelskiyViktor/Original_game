import pygame as pg
import game.physics as ph
import game.resources as res
import game.level_manager as lm



class Levels_game:
    # пока задаём текщий уровень жёстко в коде, потом будет считываться из файла

    elapsed_time = 0

    def __init__(self, settings, lives, score):
        self.start_ticks = pg.time.get_ticks()
        self.setting = settings
        self.clock = pg.time.Clock()
        self.lives = lives
        self.score = score
        self.font, _, _, _ = res.load_fonts()
        self.current_level = lm.Level(1, lm.LEVEL1_PLATFORMS, lm.LEVEL1_ENEMIES, lm.LEVEL1_OBSTACLES, lm.LEVEL1_BONUSES)

        # создаю колобка
        self.kolobok = ph.Char(5, 3, 'res/graphics/kolobok_50x50_right.png', 670)
        self.kolobok.rect = pg.Rect(30, settings.screen_height - 30, 50, 40)
        self.current_level.all_sprites.add(self.kolobok)

        # Количество жизней показываем сердечками
        self.heart = pg.sprite.Group()
        for i in range(self.lives):   #  Количество жизней
            heart = pg.sprite.Sprite()
            heart.image = pg.transform.scale(pg.image.load('res/graphics/heart.png') , (30, 30))   # Масштабирование
            heart.rect = heart.image.get_rect()
            heart.rect.x = 10 + i * heart.rect.width
            heart.rect.y = 10
            self.heart.add(heart)
            self.current_level.all_sprites.add(heart)


    def run_game(self, screen):
        # ОСНОВНОЙ ЦИКЛ ИГРЫ
        #pg.init()
        #screen = pg.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        self.current_level.create_level()
        start_ticks = pg.time.get_ticks()
        #pg.display.set_caption(self.settings.caption)
        clock = pg.time.Clock()

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


            # Обработка нажатий клавиш
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                self.kolobok.image = pg.image.load('res/graphics/kolobok_50x50_left.png')
                if self.kolobok.rect.left > 0: self.kolobok.rect.x -= self.kolobok.h_speed
            if keys[pg.K_d]:
                self.kolobok.image = pg.image.load('res/graphics/kolobok_50x50_right.png')
                if self.kolobok.rect.right < self.setting.screen_width: self.kolobok.rect.x += self.kolobok.h_speed
            if keys[pg.K_SPACE]:
                self.kolobok.jump()

            # ищем землю под колобком
            if self.kolobok.find_nearest_platform(self.current_level.platforms):
                self.kolobok.current_ground_y = self.kolobok.find_nearest_platform(self.current_level.platforms)[1]

            # Рендеринг
            self.current_level.update()
            self.current_level.draw(screen)

            # После отрисовки всего, переворачиваем экран
            pg.display.flip()

        return time_box.formatted_time, self.elapsed_time

        #pg.quit()