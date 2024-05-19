# Компоненты интерфейса
import pygame
import game.resources as res


class Player:
    def __init__(self, level_index):
        if level_index == 0:  # Начальный уровень
            self.kolobok_height = 50
            self.kolobok_x = 285
            self.kolobok_y = 51
            # Параметры платформ
            self.top_platform_y = self.kolobok_y + self.kolobok_height
            self.bottom_platform_y = 650
            self.top_platform_length = 300
            self.bottom_platform_length = 1400
            self.kolobok_running = False
            # Физические параметры
            self.gravity = 5
            self.new_x_speed = 5
            self.x_speed = 0
            self.y_speed = -1
            self.falling = False
            self.time_elapsed = 0
            self.font28, self.font22 = res.load_fonts()
            self.kolobok, self.lisa, self.medved, self.zayac = res.load_images()
            self.rect = self.kolobok[0].get_rect()
            self.rect.center = (self.kolobok_x, self.kolobok_y)


        elif level_index == 1:
            starting_position = (200, 100)
        elif level_index == 2:
            starting_position = (300, 100)
        elif level_index == 3:
            starting_position = (300, 100)
        elif level_index == 4:
            starting_position = (300, 100)
        else:
            starting_position = (400, 100)

        self.rect = self.kolobok[0].get_rect()
        self.rect.center = (self.kolobok_x, self.kolobok_y)


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed


class Enemy:
    def __init__(self, position):
        self.kolobok, self.lisa, self.medved, self.zayac = res.load_images()
        self.rect = self.lisa.get_rect()
        self.rect.center = position
        self.speed = 5

    def update(self):
        self.rect.x = 0


class Obstacle:
    def __init__(self, position, size):
        self.image = pygame.image.load("res/graphics/kust01.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.size = size

    def update(self):
        pass
        #self.rect.x -= 0

