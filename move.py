import pygame as pg
import time


def run_move(screen):
    # Загрузка звука
    pg.mixer.init()
    pg.mixer.music.load('move/intro.mp3')

    # Запуск воспроизведения звука
    pg.mixer.music.play()

    # Время отображения каждого изображения (в секундах)
    interval = 0.18
    total_time = 28  # Общее время отображения (в секундах)
    num_images = 141

    # Основной цикл отображения изображений
    start_time = time.time()
    frame_number = 1

    while (time.time() - start_time) < total_time:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.mixer.music.stop()
                return
        # Формируем имя файла текущего кадра
        frame_name = f'move/frame{frame_number:04d}.jpg'

        # Загрузка изображения
        image = pg.image.load(frame_name)

        # Отображение изображения на экране
        screen.blit(image, (0, 0))
        pg.display.flip()

        # Ожидание перед отображением следующего изображения
        time.sleep(interval)

        # Переход к следующему кадру
        frame_number += 1
        if frame_number > num_images:
            frame_number = 1

    # Остановка воспроизведения звука
    pg.mixer.music.stop()
    return

