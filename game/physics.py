# Физический движок
import pygame as pg
import random
import game.resources as res


class Char(pg.sprite.Sprite):
    enemies = []
    def __init__(self, settings, health, speed, images, current_ground_y, enemy=False, delay=0):
        pg.sprite.Sprite.__init__(self)
        self.settings = settings
        self.health = health
        self.h_speed = speed
        self.v_speed = 0
        self.on_ground = True
        self.current_ground_y = current_ground_y
        self.gravity = 0.5
        self.jump_strength = -12
        self.vector = random.choice([-1, 1])
        self.sound_priz = pg.mixer.Sound(res.load_sound()[1])
        self.sound_oj = pg.mixer.Sound(res.load_sound()[2])
        self.sound_new_level = pg.mixer.Sound(res.load_sound()[3])
        self.sound = self.settings.sound
        self.sound_volume = self.settings.sound_volume
        self.delay = delay
        self.time_delay = 0
        self.current_image = 0



        # if self.vector == -1: self.image = pg.transform.flip(self.image, True, False)
        self.images = images
        if enemy:
            self.image = self.images[0][0]
            self.rect = self.image.get_rect()
            Char.enemies.append(self) # Добавляем врага в список врагов
        elif self.delay == 2:
            self.image = self.images[0][0]
            self.rect = self.image.get_rect()
        else:
            self.image = self.images
            self.rect = self.image.get_rect()

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
        if self.rect.x <= 60 or self.rect.x + self.rect.width >= 1200:
            self.vector *= -1
            self.image = pg.transform.flip(self.image, True, False)

        # следим, чтобы враг не упал с платформы:
        if self.find_nearest_platform(platforms)[1] > self.current_ground_y:
            self.vector *= -1
            self.image = pg.transform.flip(self.image, True, False)
        self.rect.x += self.h_speed * self.vector

    def jump(self):
        if self.on_ground:
            self.v_speed = self.jump_strength
            self.on_ground = False

    # Тут как бы вечное падение, пока не ударится о платформу:
    def update(self):
        if self.delay > 0:
            self.v_speed += self.gravity
            self.rect.y += self.v_speed
            # если нижняя граница персонажа опустилась ниже позиции платформы под ним
            if self.rect.bottom > self.current_ground_y:
                self.rect.bottom = self.current_ground_y
                self.on_ground = True
                self.v_speed = 0

            self.time_delay += 1
            if self.time_delay > self.delay:
                self.time_delay = 0
                if self.delay > 2:
                    self.current_image = (self.current_image + 1) % len(self.images[0])
                    if self.vector == 1:
                        self.image = self.images[0][self.current_image]
                    else:
                        self.image = self.images[1][self.current_image]
                else:
                    self.current_image = (self.current_image + 1) % len(self.images)
                    self.image = self.images[0][self.rect.x % 12]


    def find_nearest_platform(self, platforms):
        closest_platform = None
        closest_distance = float('inf')  # Установим очень большое начальное значение
        #n = 0
        for platform in platforms:
            #n += 1
            # Платформа должна быть ниже персонажа...
            if platform.rect.top >= self.rect.bottom:
                # ...и пересекаться с персонажем по оси X на половину ширины колобка
                if (platform.rect.right >= (self.rect.right-self.rect.width*0.5)
                        and platform.rect.left <= (self.rect.left+self.rect.width*0.5)):
                    distance = platform.rect.top - self.rect.bottom
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_platform = platform

        if closest_platform is not None:
            return closest_platform.rect.topleft  # Вернем координаты верхнего левого угла платформы
        else:
            return None  # Если подходящих платформ нет, возвращаем None

    def check_hit_enemy(self, enemies, lives, current_level):
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                lives -= 1
                if self.sound:
                    self.sound_oj.set_volume(self.sound_volume)
                    self.sound_oj.play()

                if lives > 0:
                    current_level.show_hearts(lives) # показываем жизни
                    print("BANG!!! Осталось жизней:", lives)
                    self.rect.x = 30
                    self.rect.y = 670
                    current_level.hearts_sprites_group.remove(len(current_level.hearts_sprites_group) - 1)
        return lives

    def got_more_lives(self, lives):
        if lives > 0:
            return False
        else:
            print("Game Over")
            return True

    def check_get_bonus(self, bonuses, score):
        for bonus in bonuses:
            if self.rect.colliderect(bonus): # если персонаж соприкасается с бонусом
                if bonus.points == 0:
                    if self.sound:
                        self.sound_new_level.set_volume(self.sound_volume)
                        self.sound_new_level.play()
                    return True, score # уровень пройден
                else:
                    score += bonus.points  # увеличиваем счет
                    if self.sound:
                        self.sound_priz.set_volume(self.sound_volume)
                        self.sound_priz.play()
                bonuses.remove(bonus)  # удаляем бонус
        return False, score  # уровень не пройден


class Bonus(Char):
    def __init__(self, settings, health, speed, image, current_ground_y, points):
        super().__init__(settings, health, speed, image, current_ground_y)
        self.points = points