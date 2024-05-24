# Физический движок
import pygame as pg
import random


class Char(pg.sprite.Sprite):
    enemies = []
    def __init__(self, health, speed, image, current_ground_y, enemy=False):
        pg.sprite.Sprite.__init__(self)
        self.health = health
        self.h_speed = speed
        self.v_speed = 0
        self.on_ground = True
        self.current_ground_y = current_ground_y
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.gravity = 0.5
        self.jump_strength = -12
        self.vector = random.choice([-1, 1])
        if self.vector == -1: self.image = pg.transform.flip(self.image, True, False)
        if enemy: Char.enemies.append(self) # Добавляем врага в список врагов

    #отдельный метод с декоратором для того, чтобы обратиться ко всем экземплярам класса Char в списке Char.enemies, т.е. к врагам
    @classmethod
    def general_call(cls, method_name, platforms):
        # Вызываем метод по его имени для каждого экземпляра класса
        for enemy in cls.enemies:
            method = getattr(enemy, method_name, None)
            if method:
                method(platforms)

    def autorun(self, platforms):
        # Столкновение с краями экрана
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= 1200:
            self.vector *= -1
            self.image = pg.transform.flip(self.image, True, False)
        #current_ground = self.find_nearest_platform(platforms)[1]
        #print(self.rect.bottom, self.current_ground_y, self.find_nearest_platform(platforms)[1])

        # следим, чтобы враг не упал с платформы:

        if self.find_nearest_platform(platforms)[1] > self.current_ground_y:
            self.vector *= -1
            #print(self.rect.bottomleft, self.rect.bottomright, self.find_nearest_platform(platforms)[1])
            self.image = pg.transform.flip(self.image, True, False)
        #print(self.rect.bottom, self.find_nearest_platform(platforms)[1])
        self.rect.x += self.h_speed * self.vector



    def jump(self):
        if self.on_ground:
            self.v_speed = self.jump_strength
            self.on_ground = False
        if self.rect.bottom > self.current_ground_y:
            self.rect.bottom = self.current_ground_y
            self.on_ground = True
            self.v_speed = 0

    # Тут как бы вечное падение, пока не ударится о платформу:
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
            n = 0
            n += 1
            if platform.rect.top >= self.rect.bottom:

                # ...и пересекаться с персонажем по оси X на половину ширины колобка
                if platform.rect.right >= (self.rect.right-self.rect.width*0.5) and platform.rect.left <= (self.rect.left+self.rect.width*0.5):
                    distance = platform.rect.top - self.rect.bottom
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_platform = platform

        if closest_platform is not None:
            return closest_platform.rect.topleft  # Вернем координаты верхнего левого угла платформы
        else:
            return None  # Если подходящих платформ нет, возвращаем None


    def check_hit_enemy(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                print("BANG!!!")
                enemies.remove(enemy)

    def check_get_bonus(self, sprites, bonuses):
        for bonus in sprites:
            if self.rect.colliderect(bonus):
                if bonus.points == 0:
                    print("Level Cleared")
                else:
                    
                    print(f"Bonus collected, {bonus.points} points!")
                sprites.remove(bonus)

class Bonus(Char):
    def __init__(self, health, speed, image, current_ground_y, points):
        super().__init__(health, speed, image, current_ground_y)
        self.points = points