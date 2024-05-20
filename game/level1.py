import pygame as pg
import settings
import resources
import physics as ph


# функция для создания любых, но ОДИНАКОВЫХ платформ
def create_grass(x, y, length): # вводные данные - стартовые координаты (х,у) и длина
    platform_end = x+length
    while x < platform_end:
        grass = pg.sprite.Sprite()
        grass.image = pg.image.load('../res/graphics/grass2.png')
        grass.rect = grass.image.get_rect()
        grass.rect.y = y - grass.rect.height  # Позиционируем у нижнего края окна
        grass.rect.x = x
        platforms.add(grass)
        print(platforms)
        x += grass.rect.width  # Перемещаем X на ширину спрайта для следующего спрайта



pg.init()
level1 = settings.Settings()
screen = pg.display.set_mode((level1.screen_width, level1.screen_height))
pg.display.set_caption(level1.caption)
clock = pg.time.Clock()

# Создаю 2 группы спрайтов (пока пустые), чтобы потом обновлять все разом
all_sprites = pg.sprite.Group() # все остальные спрайты
platforms = pg.sprite.Group() # платформы - отдельно для проверки коллизии (для прыжков и падений)

# создаю фон
bg = pg.sprite.Sprite()
bg.image = pg.image.load('../res/graphics/fon_03.jpg')
bg.rect = bg.image.get_rect()
bg.rect.y = 0
bg.rect.x = 0
all_sprites.add(bg)

# создаю землю и платформы
create_grass(0, level1.screen_height,level1.screen_width) # ЗЕМЛЯ
create_grass(200, 620, 300) # ПЛАТФОРМА 1
create_grass(600, 350, 200) # ПЛАТФОРМА 2

# создаю колобка
kolobok = ph.Char(5, 3, '../res/graphics/kolobok_50x50_right.png')
kolobok.rect.x = 30
kolobok.rect.y = 720 - 100 #level1.screen_height - 50
all_sprites.add(kolobok)

# ОСНОВНОЙ ЦИКЛ ИГРЫ
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(level1.fps)
    # Ввод процесса (события)
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False


# Обработка нажатий клавиш
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        kolobok.image = pg.image.load('../res/graphics/kolobok_50x50_left.png')
        if kolobok.rect.left > 0: kolobok.rect.x -= kolobok.h_speed
    if keys[pg.K_d]:
        kolobok.image = pg.image.load('../res/graphics/kolobok_50x50_right.png')
        if kolobok.rect.right < level1.screen_width: kolobok.rect.x += kolobok.h_speed
    if keys[pg.K_SPACE]:
        kolobok.jump()

    kolobok.on_platform = kolobok.check_platforms_below(platforms)
    if not kolobok.on_platform:
        # Тут логика падения или "смерти" персонажа
        print(kolobok.rect.x, kolobok.rect.y)
        print("Персонаж должен падать или умереть")
        #pg.quit()
    else:
        # Тут может быть логика, которая обрабатывает стояние игрока на платформе
        print(kolobok.rect.x, kolobok.rect.y)
        print("Персонаж находится на платформе")


# Обновление спрайтов
    all_sprites.update()  # Важно вызвать метод update у всех спрайтов
    platforms.update()

# Рендеринг

    all_sprites.draw(screen)
    platforms.draw(screen)

# После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()