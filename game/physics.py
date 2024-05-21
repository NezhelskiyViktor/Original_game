# Физический движок
import pygame as pg


class Char(pg.sprite.Sprite):
    def __init__(self, health, speed, image, current_ground_y):
        pg.sprite.Sprite.__init__(self)
        self.health = health
        self.h_speed = speed
        self.v_speed = 0
        self.on_ground = True
        self.current_ground_y = current_ground_y
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.gravity = 0.5
        self.jump_strength = -13


    def jump(self):
        if self.on_ground:
            self.v_speed = self.jump_strength
            self.on_ground = False
        if self.rect.bottom > self.current_ground_y:
            self.rect.bottom = self.current_ground_y
            self.on_ground = True
            self.v_speed = 0

    def update(self):
        self.v_speed += self.gravity
        self.rect.y += self.v_speed

        if self.rect.bottom > self.current_ground_y: # если нижняя граница персонажа опустилсь ниже позиции платформы под ним
            self.rect.bottom = self.current_ground_y
            self.on_ground = True
            self.v_speed = 0

    def find_nearest_platform(self, platforms):
        closest_platform = None
        closest_distance = float('inf')  # Установим очень большое начальное значение

        for platform in platforms:
            # Платформа должна быть ниже персонажа...
            if platform.rect.top >= self.rect.bottom:
                # ...и пересекаться с персонажем по оси X на половину ширины колобка
                if platform.rect.right >= (self.rect.left+self.rect.width*0.5) and platform.rect.left <= (self.rect.right-self.rect.width*0.5):
                    distance = platform.rect.top - self.rect.bottom
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_platform = platform

        if closest_platform is not None:
            return closest_platform.rect.topleft  # Вернем координаты верхнего левого угла платформы
        else:
            return None  # Если подходящих платформ нет, возвращаем None