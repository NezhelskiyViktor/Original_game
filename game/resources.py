import pygame as pg


def load_fonts():
    font28 = pg.font.Font('res/font/arialbi.ttf', 28)
    font22 = pg.font.Font('res/font/arialbi.ttf', 22)
    return font28, font22


def load_images():
    bg = pg.image.load('res/graphics/fon_03.jpg').convert()
    kolobok_image_god = pg.image.load('res/graphics/Kolobok_god_mode.png').convert_alpha()
    kolobok_image = pg.image.load('res/graphics/Kolobok01.png').convert_alpha()
    kolobok_list = []
    for i in range(31):
        kolobok_ = pg.transform.rotate(kolobok_image, -i * 11.6129)
        kolobok = pg.transform.scale(kolobok_, (50, 50))  # Масштабирование
        kolobok_list.append(kolobok)
    kolobok = [pg.transform.scale(kolobok_image_god, (50, 50)), \
               pg.transform.scale(kolobok_image, (50, 50)),\
               kolobok_list]
    lisa_image = pg.image.load('res/graphics/lisa.png').convert_alpha()
    lisa = pg.transform.scale(lisa_image, (282, 360))  # Масштабирование
    medved_image = pg.image.load('res/graphics/medved.png').convert_alpha()
    medved = pg.transform.scale(medved_image, (160, 160))  # Масштабирование
    medved = pg.transform.flip(medved, True, False)  # Отражение по горизонтали
    zayac_image = pg.image.load('res/graphics/zayac01.png').convert_alpha()
    zayac = pg.transform.scale(zayac_image, (282, 360))  # Масштабирование

    return bg, kolobok, lisa, medved, zayac


def load_music():
    pg.mixer.music.load('res/sounds/music_fon_01.mp3')
