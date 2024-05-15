# Обработка пользовательского ввода
import pygame as pg


def handle_events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
    return True
