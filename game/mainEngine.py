import pygame as pg
import settings
import resources
import physics as ph

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

# Текстовые блоки.
class TextBox(pg.sprite.Sprite):
    def __init__(self, text, x, y):
        pg.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pg.font.Font("../res/font/arialbi.ttf", 30)
        self.image = self.font.render(self.text, False, resources.RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.text = formatted_time
        self.image = self.font.render(self.text, False, resources.RED)


# функция для создания любых, но ОДИНАКОВЫХ платформ
def create_grass(x, y, length): # вводные данные - стартовые координаты (х,у) и длина
    platform_end = x+length
    while x < platform_end:
        grass = pg.sprite.Sprite()
        grass.image = pg.image.load('../res/graphics/grass01.png')
        grass.rect = grass.image.get_rect()
        grass.rect.y = y - grass.rect.height  # Позиционируем у нижнего края окна
        grass.rect.x = x
        platforms.add(grass)
        x += grass.rect.width  # Перемещаем X на ширину спрайта для следующего спрайта

# пока задаём текщий уровень жёстко в коде, потом будет считываться из файла
current_level=1

pg.init()
start_ticks = pg.time.get_ticks()
level1 = settings.Settings()
screen = pg.display.set_mode((level1.screen_width, level1.screen_height))
pg.display.set_caption(level1.caption)
clock = pg.time.Clock()

# Создаю 2 группы спрайтов (пока пустые), чтобы потом обновлять все разом
all_sprites = pg.sprite.Group() # все остальные спрайты
platforms = pg.sprite.Group() # платформы - отдельно для проверки коллизии (для прыжков и падений)

# создаю фон
bg = pg.sprite.Sprite()
bg.image = pg.image.load('../res/graphics/fon_03-2.jpg')
bg.rect = bg.image.get_rect()
bg.rect.y = 0
bg.rect.x = 0
screen.blit(bg.image, (0, 0))
#all_sprites.add(bg)

# создаю землю и платформы
create_grass(0, level1.screen_height,level1.screen_width) # ЗЕМЛЯ
create_grass(200, 620, 300) # ПЛАТФОРМА 1
create_grass(500, 520, 200) # ПЛАТФОРМА 2
create_grass(350, 420, 100) # ПЛАТФОРМА 3
create_grass(500, 320, 400) # ПЛАТФОРМА 4

# создаю колобка
kolobok = ph.Char(5, 3, '../res/graphics/kolobok_50x50_right.png', 670)
kolobok.rect.x = 30
kolobok.rect.y = level1.screen_height - 30
all_sprites.add(kolobok)

# Создаю табло времени
time_box = TextBox("00:00", 1100, 20)
all_sprites.add(time_box)

# ОСНОВНОЙ ЦИКЛ ИГРЫ
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(level1.fps)
    # Ввод процесса (события)
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False

# Считаем прошедшее время с начала игры
    # Получаем текущее время
    current_ticks = pg.time.get_ticks()
    # Вычисляем время работы приложения
    elapsed_time = current_ticks - start_ticks
    # Форматируем прошедшее время
    formatted_time = format_time(elapsed_time)

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


    if kolobok.find_nearest_platform(platforms):
        kolobok.current_ground_y = kolobok.find_nearest_platform(platforms)[1]

# Проверка столкновения
#     if pg.sprite.spritecollide(kolobok, platforms, False):
#         kolobok.rect.y = kolobok.current_ground_y
#         kolobok.v_speed = 0
#         kolobok.on_ground = True


# Обновление спрайтов
    platforms.update()
    all_sprites.update()

# Рендеринг
    screen.blit(bg.image, (0, 0))
    platforms.draw(screen)
    all_sprites.draw(screen)

# После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()