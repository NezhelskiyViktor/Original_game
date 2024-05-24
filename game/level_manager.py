import pygame as pg
import game.resources as res
import game.physics as ph

class Level():
    def __init__(self, index, platforms, enemies, obstacles, bonuses):
        self.index = index
        self.platforms_coord = platforms
        self.enemies = enemies
        self.obstacles = obstacles
        self.bonuses = bonuses
        self.bg = pg.sprite.Sprite()
        self.enemies_sprites_group = pg.sprite.Group() # отдельная группа для спрайтов врагов
        self.bonuses_sprites_group = pg.sprite.Group() # отдельная группа для спрайтов бонусов
        self.bg_group = pg.sprite.Group() # отдельная группа спрайтов для одного фона
        self.all_sprites = pg.sprite.Group()  # основные спрайты (колобок, бонусы и т.п.)
        self.platforms = pg.sprite.Group()  # платформы - отдельно для проверки коллизий (для прыжков и падений)

    def create_level(self):
    # создание фона
        self.bg.image = pg.image.load(f"res/graphics/fon_0{self.index}.jpg")
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.y = 0
        self.bg.rect.x = 0
        self.bg_group.add(self.bg)
    # создание платформ
        for platform in self.platforms_coord:
            self.create_grass(platform[0], platform[1], platform[2])


    def create_grass(self,x, y, length):  # вводные данные - стартовые координаты (х,у) и длина
        platform_end = x + length
        while x < platform_end:
            grass = pg.sprite.Sprite()
            grass.image = pg.image.load(f"res/graphics/grass_0{self.index}.png")
            grass.rect = grass.image.get_rect()
            grass.rect.y = y  # Позиционируем у нижнего края окна
            grass.rect.x = x
            self.platforms.add(grass)
            x += grass.rect.width  # Перемещаем X на ширину спрайта для следующего спрайта


    def create_enemies(self, enemies):
        self.enemies = {}  # Создаем пустой словарь для хранения врагов

        for index, enemy_data in enumerate(enemies): # Проходим по списку врагов, вытаскиваем индекс и характеристики
            enemy_id = f'enemy{index}'  # Создаем уникальный идентификатор для каждого врага
            self.enemies[enemy_id] = ph.Char(enemy_data[0], enemy_data[1], enemy_data[2], enemy_data[4], True) # Создаем экземпляр класса Char с использованием данных из enemy_data
            # Хитбокс меньше размеров картинки (-10 px снизу, чтобы персонаж ходил, чуть погружаясь в траву), по бокам - компенсируем воздух на картинке.
            self.enemies[enemy_id].rect = self.enemies[enemy_id].image.get_rect()
            self.enemies[enemy_id].rect.inflate_ip(-10, -10)  # Уменьшаем размеры на 10 пикселей по каждой оси
            self.enemies[enemy_id].rect.topleft = (self.enemies[enemy_id].rect.left + 5, self.enemies[enemy_id].rect.top + 5)  # Смещаем на 10 пикселей от начала
            self.enemies[enemy_id].rect.x = enemy_data[3]
            self.enemies[enemy_id].rect.y = enemy_data[4] - self.enemies[enemy_id].rect.height
            self.enemies_sprites_group.add(self.enemies[enemy_id])


    def crate_bonuses(self, bonuses):
        self.bonuses = {}

        for index, bonus in enumerate(bonuses):
            bonus_id = f'bonus{index}'
            self.bonuses[bonus_id] = ph.Bonus(1, 0, bonus[2], bonus[1], bonus[3])
            self.bonuses[bonus_id].rect = self.bonuses[bonus_id].image.get_rect()
            self.bonuses[bonus_id].rect.inflate_ip(0, -10)
            self.bonuses[bonus_id].rect.topleft = (self.bonuses[bonus_id].rect.left + 5, self.bonuses[bonus_id].rect.top + 5)
            self.bonuses[bonus_id].rect.x = bonus[0]
            self.bonuses[bonus_id].rect.y = bonus[1] - self.bonuses[bonus_id].rect.height
            self.bonuses_sprites_group.add(self.bonuses[bonus_id])

    def update(self):        # Обновление спрайтов
        self.bg_group.update()
        self.platforms.update()
        self.all_sprites.update()
        self.enemies_sprites_group.update()
        #print(self.all_sprites)

    def draw(self, screen):
        # Метод для отрисовки объектов уровня
        self.bg_group.draw(screen)
        self.platforms.draw(screen)
        self.all_sprites.draw(screen)
        self.bonuses_sprites_group.draw(screen)
        self.enemies_sprites_group.draw(screen)




# Табло времени
class TextBox(pg.sprite.Sprite):
    def __init__(self, text, x, y):
        pg.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pg.font.Font("res/font/arialbi.ttf", 30)
        self.image = self.font.render(self.text, False, res.RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.elapsed_time = 0
        self.formatted_time = self.format_time(self.elapsed_time)

    def format_time(self,milliseconds):
        # Преобразуем миллисекунды в секунды
        seconds = milliseconds // 1000
        # Получаем минуты и секунды
        minutes = seconds // 60
        seconds = seconds % 60
        # Форматируем время в строку MM:SS
        time_str = f"{minutes:02}:{seconds:02}"
        return time_str

    def update(self):
        self.text = self.format_time(self.elapsed_time)
        self.image = self.font.render(self.text, False, res.RED)



# Платформы. Нулевая - всегда земля. [Х, Y, длина в рх (по факту будет кратна спрайту)]
LEVEL1_PLATFORMS =[
    [0, 670, 1200],
    [200, 570, 300],
    [600, 470, 200],
    [450, 380, 50],
    [0, 270, 400],
    [500, 170, 200],
    [800, 250, 200],
    [1100, 350, 100],
    [1000, 570, 200],
]

# Враги [здоровье, скорость, фото, x (платформы, на которой оно стоит), y (верх платформы)]
LEVEL1_ENEMIES = [
    [1, 2, 'res/graphics/lisa84x165_right.png', 100, 270],
    [1, 1, 'res/graphics/zayac57x150_hitbox.png', 650, 470],
    [1, 5, 'res/graphics/zayac57x150_right.png', 800, 670]
]

LEVEL1_OBSTACLES = [

]

# Бонусы [x, y, фото стоимость]. Нулевая запись - всегда выход с уровня
LEVEL1_BONUSES = [
    [1100, 350, 'res/graphics/door_locked.png', 0],
    [400, 670, 'res/graphics/grib03.png', 10],
    [820, 250, 'res/graphics/grib03.png', 10],
    [1120, 570, 'res/graphics/grib03.png', 10],
    #[400, 670, 'res/graphics/grib03.png', 10],
]




LEVEL2_PLATFORMS =[
    [0, 670, 1200],
    [200, 620, 300],
    [700, 520, 200],
    [470, 430, 100],
    [500, 360, 400]
]

LEVEL2_ENEMIES = [

]

LEVEL2_OBSTACLES = [

]

LEVEL2_BONUSES = [

]