import pygame as pg


def load_fonts():
    font30 = pg.font.Font('res/font/arialbi.ttf', 30)
    font28 = pg.font.Font('res/font/arialbi.ttf', 28)
    font22 = pg.font.Font('res/font/arialbi.ttf', 22)
    font18 = pg.font.Font('res/font/arialbi.ttf', 18)
    return font30, font28, font22, font18


def load_background():
    bg = [
    pg.image.load('res/graphics/fon_00.jpg').convert(),  # 0
    pg.image.load('res/graphics/fon_01.jpg').convert(),  # 1
    pg.image.load('res/graphics/fon_03-2.jpg').convert()  # 2
    ]
    return bg


def load_images():
    kolobok_image_god = pg.image.load('res/graphics/Kolobok_god_mode.png').convert_alpha()
    kolobok_image = pg.image.load('res/graphics/Kolobok_Ivan.png').convert_alpha()
    kolobok_list = []
    for i in range(1, 32):
        kolobok_ = pg.transform.rotate(kolobok_image, -i * 11.6129)
        kolobok = pg.transform.scale(kolobok_, (50, 50))  # Масштабирование
        kolobok_list.append(kolobok)

    kolobok = [pg.transform.scale(kolobok_image_god, (50, 50)), \
               pg.transform.scale(kolobok_image, (50, 50)), \
               kolobok_list]
    lisa_image = pg.image.load('res/graphics/lisa.png').convert_alpha()
    lisa = pg.transform.scale(lisa_image, (282, 360))  # Масштабирование
    medved_image = pg.image.load('res/graphics/medved01.png').convert_alpha()
    medved = pg.transform.scale(medved_image, (160, 160))  # Масштабирование
    medved = pg.transform.flip(medved, True, False)  # Отражение по горизонтали
    zayac_image = pg.image.load('res/graphics/zayac01.png').convert_alpha()
    zayac = pg.transform.scale(zayac_image, (282, 360))  # Масштабирование

    return kolobok, lisa, medved, zayac


def load_music():
    music = [
        'res/sounds/music_fon_01.mp3'
    ]
    return music


def load_sound():
    sound = [
        'res/sounds/teases01.wav'
    ]
    return sound

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY =(200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)