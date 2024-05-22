import pygame as pg
import settings
import physics as ph
import level_manager as lm


# Создаём текущий уровень Level (index, platforms, enemies, obstacles, bonuses)
current_level = lm.Level(1, lm.LEVEL1_PLATFORMS, lm.LEVEL1_ENEMIES, lm.LEVEL1_OBSTACLES, lm.LEVEL1_BONUSES)

pg.init()
current_level.create_level()
start_ticks = pg.time.get_ticks()
settings = settings.Settings()
screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
pg.display.set_caption(settings.caption)
clock = pg.time.Clock()



# создаю колобка
kolobok = ph.Char(5, 3, '../res/graphics/kolobok_50x50_right.png', 670)
kolobok.rect = pg.Rect(30, settings.screen_height - 30, 50, 40)
current_level.all_sprites.add(kolobok)

# Создаю табло времени
time_box = lm.TextBox("00:00", 1100, 20)
current_level.all_sprites.add(time_box)

# ОСНОВНОЙ ЦИКЛ ИГРЫ
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(settings.fps)
    # Ввод процесса (события)
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False

# Считаем прошедшее время с начала игры
    # Получаем текущее время
    current_ticks = pg.time.get_ticks()
    # Вычисляем время работы приложения
    time_box.elapsed_time = current_ticks - start_ticks
    # Форматируем прошедшее время
    time_box.formatted_time = time_box.format_time(time_box.elapsed_time)

# Обработка нажатий клавиш
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        kolobok.image = pg.image.load('../res/graphics/kolobok_50x50_left.png')
        if kolobok.rect.left > 0: kolobok.rect.x -= kolobok.h_speed
    if keys[pg.K_d]:
        kolobok.image = pg.image.load('../res/graphics/kolobok_50x50_right.png')
        if kolobok.rect.right < settings.screen_width: kolobok.rect.x += kolobok.h_speed
    if keys[pg.K_SPACE]:
        kolobok.jump()


    if kolobok.find_nearest_platform(current_level.platforms):
        kolobok.current_ground_y = kolobok.find_nearest_platform(current_level.platforms)[1]

# Проверка столкновения
#     if pg.sprite.spritecollide(kolobok, platforms, False):
#         kolobok.rect.y = kolobok.current_ground_y
#         kolobok.v_speed = 0
#         kolobok.on_ground = True


# Рендеринг
    current_level.update()
    current_level.draw(screen)


# После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()