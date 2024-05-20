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
        self.jump_strength = -11

    #определяем, есть под ним что-то, или надо упасть:
    def check_platforms_below(self, platforms):
        # Сдвигаем rect игрока вниз на 1 пиксель для проверки столкновения с платформами
        self.rect.y += 1
        for platform in platforms:
            # Проверяем столкновение игрока с платформой
            if self.rect.colliderect(platform.rect):
                # Если нашли столкновение с перемещением вниз,
                # значит, под игроком есть платформа, и он не должен падать
                self.rect.y -= 1  # Отменяем перемещение rect игрока
                return True

        # Если перебрали все платформы и не нашли столкновений,
        # возвращаем игрока на его первоначальную позицию и сообщаем, что он должен падать
        self.rect.y -= 1
        return False

    def jump(self):
        if self.on_ground:
            self.v_speed = self.jump_strength
            self.on_ground = False

# КОСТЫЛЬ!!!!!! надо потом сделать универсальную передачу констант, ведь уровни будут разные
# сейчас проверяю только находждение на полу
        if self.rect.bottom > self.current_ground_y:
            self.rect.bottom = self.current_ground_y
            self.on_ground = True
            self.v_speed = 0

    def update(self):
        self.v_speed += self.gravity
        self.rect.y += self.v_speed

        if self.rect.bottom > self.current_ground_y: #- self.rect.height:
            self.rect.bottom = self.current_ground_y #- self.rect.height
            self.on_ground = True
            self.velocity = 0

    def find_nearest_platform(self, platforms):
        closest_platform = None
        closest_distance = float('inf')  # Установим очень большое начальное значение

        for platform in platforms:
            # Платформа должна быть ниже персонажа...
            if platform.rect.top >= self.rect.bottom:
                # ...и пересекаться с персонажем по оси X
                if platform.rect.right >= self.rect.left and platform.rect.left <= self.rect.right:
                    distance = platform.rect.top - self.rect.bottom
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_platform = platform

        if closest_platform is not None:
            return closest_platform.rect.topleft  # Вернем координаты верхнего левого угла платформы
        else:
            return None  # Если подходящих платформ нет, возвращаем None