import pygame as pg
from ui.components import Player, Obstacle, Enemy
import game.resources as res

def _create_level(level_index):
    background = pg.image.load(f"../res/graphics/fon_0{level_index}.jpg")
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

    # Создаем фон уровня


    # Создаем игрока
    player = Player(level_index)  # Пример начальной позиции

    # Создаем препятствия
    obstacles = [
        # Obstacle(position=(200, 300), size=(50, 50)),
        # Obstacle(position=(400, 300), size=(50, 50))
    ]

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


