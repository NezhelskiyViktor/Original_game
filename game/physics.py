# Физический движок
import pygame as pg


class Char(pg.sprite.Sprite):
    def __init__(self, health, speed, image):
        pg.sprite.Sprite.__init__(self)
        self.health = health
        self.h_speed = speed
        self.v_speed = 0
        self.on_ground = True
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
        if self.rect.bottom > 720-50: # тут надо понять, как поймать координату Х поверхности, над которой он находится
            self.rect.bottom = 720-50
            self.on_ground = True
            self.v_speed = 0

    def update(self):
        self.v_speed += self.gravity
        self.rect.y += self.v_speed

        if self.rect.bottom > 720 - self.rect.height:
            self.rect.bottom = 720 - self.rect.height
            self.on_ground = True
            self.velocity = 0

'''
# Обработка нажатий клавиш. Здесь именно факт зажатия и удерживания, если нужно непрерывное движение
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player.rect.x > 0: player.rect.x -= 10
    if keys[pygame.K_RIGHT]:
        if player.rect.right < monster.rect.left + 25: player.rect.x += 10
'''