import pygame as pg


def load_resources():
    font28 = pg.font.Font('res/font/arialbi.ttf', 28)
    font22 = pg.font.Font('res/font/arialbi.ttf', 22)

    bg = pg.image.load('res/graphics/fon_03.jpg').convert()
    kolobok_image = pg.image.load('res/graphics/Kolobok_god_mode.png').convert_alpha()
    kolobok = pg.transform.scale(kolobok_image, (50, 50))  # Масштабирование
    lisa_image = pg.image.load('res/graphics/lisa.png').convert_alpha()
    lisa = pg.transform.scale(lisa_image, (282, 360))  # Масштабирование

    return font28, font22, bg, kolobok, lisa
