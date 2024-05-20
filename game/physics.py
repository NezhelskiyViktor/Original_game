# Физический движок
import pygame as pg
import settings

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
        self.jump_strength = -10

    #определяем, есть под ним что-то, или надо упасть:
    def on_ground(self):
        # if self.rect.bottom >= HEIGHT - 30:
        #     return True
        # else:
        #     return False
        pass

    # def update(self):
    #     self.v_speed += self.gravity
    #     self.rect.y += self.v_speed
    #
    #     if self.rect.bottom > pg.display.height - self.rect.height:
    #         self.rect.bottom = pg.display.height - self.rect.height
    #         self.on_ground = True
    #         self.velocity = 0

'''
# Обработка нажатий клавиш. Здесь именно факт зажатия и удерживания, если нужно непрерывное движение
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player.rect.x > 0: player.rect.x -= 10
    if keys[pygame.K_RIGHT]:
        if player.rect.right < monster.rect.left + 25: player.rect.x += 10
'''