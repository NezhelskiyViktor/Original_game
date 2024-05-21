import pygame as pg
import game.physics as ph
import game.resources as res


# Переводит милисекунды в удобный формат
def format_time(milliseconds):
    # Преобразуем миллисекунды в секунды
    seconds = milliseconds // 1000
    # Получаем минуты и секунды
    minutes = seconds // 60
    seconds = seconds % 60
    # Форматируем время в строку MM:SS
    time_str = f"{minutes:02}:{seconds:02}"
    return time_str


# функция для создания любых, но ОДИНАКОВЫХ платформ
def create_grass(x, y, length, platforms):  # вводные данные - стартовые координаты (х,у) и длина
    platform_end = x + length
    while x < platform_end:
        grass = pg.sprite.Sprite()
        grass.image = pg.image.load('res/graphics/grass01.png')
        grass.rect = grass.image.get_rect()
        grass.rect.y = y - grass.rect.height  # Позиционируем у нижнего края окна
        grass.rect.x = x
        platforms.add(grass)
        x += grass.rect.width  # Перемещаем X на ширину спрайта для следующего спрайта


class Levels_game:
    # пока задаём текщий уровень жёстко в коде, потом будет считываться из файла
    current_level = 1
    elapsed_time = 0

    def __init__(self, settings, lives, score):
        self.start_ticks = pg.time.get_ticks()
        self.setting = settings
        self.clock = pg.time.Clock()
        self.lives = lives
        self.score = score

        self.font, _, _, _ = res.load_fonts()


        # Создаю 2 группы спрайтов (пока пустые), чтобы потом обновлять все разом
        self.all_sprites = pg.sprite.Group()  # все остальные спрайты
        self.platforms = pg.sprite.Group()  # платформы - отдельно для проверки коллизии (для прыжков и падений)

        # создаю фон
        self.bg = res.load_background()[2]

        # создаю землю и платформы
        create_grass(0, self.setting.screen_height, self.setting.screen_width, self.platforms)  # ЗЕМЛЯ
        create_grass(200, 620, 300, self.platforms)  # ПЛАТФОРМА 1
        create_grass(500, 520, 200, self.platforms)  # ПЛАТФОРМА 2
        create_grass(350, 420, 100, self.platforms)  # ПЛАТФОРМА 3
        create_grass(500, 320, 400, self.platforms)  # ПЛАТФОРМА 4

        # создаю колобка
        self.kolobok = ph.Char(5, 3, 'res/graphics/kolobok_50x50_right.png', 670)
        self.kolobok.rect.x = 30
        self.kolobok.rect.y = self.setting.screen_height - 30
        self.all_sprites.add(self.kolobok)
        self.kolobok.image = pg.image.load('res/graphics/kolobok_50x50_left.png')

        # Количество жизней показываем сердечками
        self.heart = pg.sprite.Group()
        for i in range(self.lives):   #  Количество жизней
            heart = pg.sprite.Sprite()
            heart.image = pg.transform.scale(pg.image.load('res/graphics/heart.png') , (30, 30))   # Масштабирование
            heart.rect = heart.image.get_rect()
            heart.rect.x = 10 + i * heart.rect.width
            heart.rect.y = 10
            self.heart.add(heart)
            self.all_sprites.add(heart)


    def run_game(self, screen):
        # ОСНОВНОЙ ЦИКЛ ИГРЫ
        running = True
        while running:
            # Держим цикл на правильной скорости
            self.clock.tick(self.setting.fps)
            # Ввод процесса (события)
            for event in pg.event.get():
                if event.type == pg.QUIT: running = False

            # Считаем прошедшее время с начала игры
            self.elapsed_time = pg.time.get_ticks() - self.start_ticks

            # Обработка нажатий клавиш
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                # self.kolobok.image = pg.image.load('res/graphics/kolobok_50x50_left.png')
                if self.kolobok.rect.left > 0: self.kolobok.rect.x -= self.kolobok.h_speed
            if keys[pg.K_d]:
                # self.kolobok.image = pg.image.load('res/graphics/kolobok_50x50_right.png')
                if self.kolobok.rect.right < self.setting.screen_width: self.kolobok.rect.x += self.kolobok.h_speed
            if keys[pg.K_SPACE]:
                self.kolobok.jump()

            if self.kolobok.find_nearest_platform(self.platforms):
                self.kolobok.current_ground_y = self.kolobok.find_nearest_platform(self.platforms)[1]

            # Проверка столкновения
            #     if pg.sprite.spritecollide(kolobok, platforms, False):
            #         kolobok.rect.y = kolobok.current_ground_y
            #         kolobok.v_speed = 0
            #         kolobok.on_ground = True

            # Обновление спрайтов
            self.platforms.update()
            self.all_sprites.update()

            # Рендеринг
            self.draw(screen)
        return format_time(self.elapsed_time), self.elapsed_time

    def draw(self, screen):
        # Рендеринг
        screen.blit(self.bg, (0, 0))
        self.platforms.draw(screen)
        self.all_sprites.draw(screen)
        # Отображение времени
        screen.blit(self.font.render(format_time(self.elapsed_time), True, res.RED), (1100, 20))
        # После отрисовки всего, переворачиваем экран
        pg.display.flip()
