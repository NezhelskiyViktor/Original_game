import pygame as pg
import settings
import resources
import physics as ph


def create_grass(x, y, length):
    platform_end = x+length
    while x < platform_end:
        grass = pg.sprite.Sprite()
        grass.image = pg.image.load('../res/graphics/grass2.png')
        grass.rect = grass.image.get_rect()
        grass.rect.y = y - grass.rect.height  # Позиционируем у нижнего края окна
        grass.rect.x = x
        all_sprites.add(grass)
        x += grass.rect.width  # Перемещаем X на ширину спрайта для следующего спрайта



pg.init()
level1 = settings.Settings()
screen = pg.display.set_mode((level1.screen_width, level1.screen_height))
pg.display.set_caption(level1.caption)
clock = pg.time.Clock()

# Создаю группу спрайтов, чтобы потом обновлять все разом
all_sprites = pg.sprite.Group()

# создаю землю и платформы
create_grass(0, level1.screen_height,level1.screen_width) # ЗЕМЛЯ
create_grass(200, 550, 300) # ПЛАТФОРМА
create_grass(600, 350, 300) # ПЛАТФОРМА

# создаю колобка
kolobok = ph.Char(5, 5, '../res/graphics/kolobok01.png')
kolobok = pg.transform.scale(kolobok, (50, 50))
kolobok.rect.x = 30
kolobok.rect.y = level1.screen_height - 220
all_sprites.add(kolobok)

# ОСНОВНОЙ ЦИКЛ ИГРЫ
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(level1.fps)
    # Ввод процесса (события)
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False





# Обновление спрайтов
    all_sprites.update()  # Важно вызвать метод update у всех спрайтов

# Рендеринг
    screen.fill(resources.GREY)
    all_sprites.draw(screen)

# После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()