import pygame as pg
from ui.components import Player, Obstacle, Enemy
import game.resources as res

def create_level(level_index):
    background = pg.image.load(f"../res/graphics/fon_0{level_index}.jpg")
    grass = pg.image.load(f"../res/graphics/grass_0{level_index}.png")
    match level_index:
        case 0:
            pass
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass

def create_grass(x, y, length):  # вводные данные - стартовые координаты (х,у) и длина
    platform_end = x + length
    while x < platform_end:
        grass = pg.sprite.Sprite()
        grass.image = pg.image.load('../res/graphics/grass2.png')
        grass.rect = grass.image.get_rect()
        grass.rect.y = y - grass.rect.height  # Позиционируем у нижнего края окна
        grass.rect.x = x
        mainEngine.platforms.add(grass)
        x += grass.rect.width  # Перемещаем X на ширину спрайта для следующего спрайта

    # Создаем игрока
    player = Player(level_index)  # Пример начальной позиции



    # Создаем врагов
    if level_index == 0:
        enemies = [
            Enemy(position=(10, 550)),
        ]
    elif level_index == 1:
        enemies = []
    elif level_index == 2:
        enemies = []
    elif level_index == 3:
        enemies = []
    elif level_index == 4:
        enemies = []
    else:
        enemies = []

    return {
        "background": background,
        "player": player,
        "obstacles": obstacles,
        "enemies": enemies
    }


class LevelManager:
    def __init__(self):
        self.levels = ["level0", "level1", "level2", "level3", "level4"]
        self.current_level_index = 0
        self.current_level = None

    def load_level(self, level_index):
        # if level_index < 0 or level_index >= len(self.levels):
        #     raise ValueError("Invalid level index")
        level_name = self.levels[level_index]
        self.current_level = _create_level(level_index)
        self.current_level_index = level_index
        if level_index == 0:
            res.load_music()
            pg.mixer.music.play(loops=-1)
            pg.mixer.music.set_volume(0.125)
            running = True

    def update(self, screen):
        if self.current_level is None:
            return

        # Отрисовка фона
        screen.blit(self.current_level["background"], (0, 0))

        # Обновление и отрисовка игрока
        self.current_level["player"].update()
        screen.blit(self.current_level["player"].kolobok[1], self.current_level["player"].rect)

        # Обновление и отрисовка препятствий
        for obstacle in self.current_level["obstacles"]:
            obstacle.update()
            screen.blit(obstacle.image, obstacle.rect)

        # Обновление и отрисовка врагов
        for enemy in self.current_level["enemies"]:
            enemy.update()
            screen.blit(enemy.lisa, enemy.rect)


