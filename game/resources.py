import pygame as pg


def load_fonts():
    font30 = pg.font.Font('res/font/segoeprb.ttf', 30)
    font28 = pg.font.Font('res/font/segoeprb.ttf', 28)
    font22 = pg.font.Font('res/font/segoeprb.ttf', 22)
    font18 = pg.font.Font('res/font/segoeprb.ttf', 18)
    return font30, font28, font22, font18


def load_background():
    bg = [
    pg.image.load('res/graphics/fon_00.jpg').convert(),  # 0
    pg.image.load('res/graphics/fon_01.jpg').convert(),  # 1
    pg.image.load('res/graphics/fon_03.jpg').convert(),  # 2
    pg.image.load('res/graphics/fon_04.jpg').convert(),  # 3
    pg.image.load('res/graphics/fon_05.jpg').convert(),  # 4
    pg.image.load('res/graphics/fon_06.jpg').convert()  # 5
    ]
    return bg


def load_images_kolobok():
    kolobok_list = [[], [], []]
    for i in range(1, 13):
        kolobok = pg.image.load(f'res/graphics/colobok_{i:02}.png').convert_alpha()
        kolobok_list[0].append(kolobok)
        kolobok = pg.transform.flip(kolobok, True, False)
        kolobok_list[1].append(kolobok)
    kolobok = pg.transform.scale(kolobok, (25, 25))
    kolobok_list[2].append(kolobok)
    return kolobok_list


def load_images_zayac():
    # zayac_images = [[], []]
    # for i in range(1, 5):
    #     zayac = pg.image.load(f'res/graphics/zayac_{i:02}.png').convert_alpha()
    #     zayac_images[0].append(zayac)
    #     zayac = pg.transform.flip(zayac, True, False)
    #     zayac_images[1].append(zayac)
    zayac_images = [[
    pg.image.load('res/graphics/zayac_01.png'),
    pg.image.load('res/graphics/zayac_02.png'),
    pg.image.load('res/graphics/zayac_03.png'),
    pg.image.load('res/graphics/zayac_04.png')
], [
    pg.transform.flip(pg.image.load('res/graphics/zayac_01.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/zayac_02.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/zayac_03.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/zayac_04.png'), True, False)
]]
    return zayac_images


def load_images_medved():
    medved_images = [[
    pg.image.load('res/graphics/medved_01.png'),
    pg.image.load('res/graphics/medved_02.png'),
    pg.image.load('res/graphics/medved_01.png'),
    pg.image.load('res/graphics/medved_04.png')
], [
    pg.transform.flip(pg.image.load('res/graphics/medved_01.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/medved_02.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/medved_01.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/medved_04.png'), True, False)
]]
    return medved_images


def load_images_lisa():
    lisa_images = [[
    pg.image.load('res/graphics/lisa_01.png'),
    pg.image.load('res/graphics/lisa_02.png'),
    pg.image.load('res/graphics/lisa_03.png'),
    pg.image.load('res/graphics/lisa_04.png'),
    pg.image.load('res/graphics/lisa_05.png'),
    pg.image.load('res/graphics/lisa_06.png'),
    pg.image.load('res/graphics/lisa_05.png'),
    pg.image.load('res/graphics/lisa_04.png'),
    pg.image.load('res/graphics/lisa_03.png'),
    pg.image.load('res/graphics/lisa_02.png'),
    pg.image.load('res/graphics/lisa_01.png'),
    ], [
    pg.transform.flip(pg.image.load('res/graphics/lisa_01.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_02.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_03.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_04.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_05.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_06.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_05.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_04.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_03.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_02.png'), True, False),
    pg.transform.flip(pg.image.load('res/graphics/lisa_01.png'), True, False),
    ]]
    return lisa_images


def load_music():
    music = [
        'res/sounds/music_fon_01.mp3',
        'res/sounds/music_fon_02.mp3'
    ]
    return music


def load_sound():
    sound = [
        'res/sounds/teases01.wav',
        'res/sounds/priz.wav',
        'res/sounds/Oj.mp3',
        'res/sounds/new_level.mp3'
    ]
    return sound

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY =(200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (235, 155, 0)