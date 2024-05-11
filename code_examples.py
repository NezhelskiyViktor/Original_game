import pygame
import sys

# Инициализация Pygame
pygame.init()


def rotate_image(a_image, a_angle):
    """Поворот изображения, сохраняя его центр."""
    the_image = pygame.transform.rotate(a_image, a_angle)
    rect = a_image.get_rect()
    the_image_rect = the_image.get_rect(center=rect.center)
    return the_image, the_image_rect


FPS = 60
clock = pygame.time.Clock()
# Создание окна
screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Пример преобразования функциями Pygame")

# Загрузка изображения
image_path = " resources/ graphics/Kolobok_regular.png"  # Укажите путь к вашему файлу
image = pygame.image.load(image_path)

# Трансформации
scaled_image = pygame.transform.scale(image, (50, 50))  # Масштабирование
rotated_image = pygame.transform.rotate(image, 30)  # Поворот на 45 градусов
flipped_image = pygame.transform.flip(image, True, False)  # Отражение по горизонтали
angle = 0


# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Заполняем экран белым цветом

    # Отображение изображений
    screen.blit(image, (50, 50))
    screen.blit(scaled_image, (250, 50))
    screen.blit(rotated_image, (350, 50))
    screen.blit(flipped_image, (50, 250))
    new_image, new_rect = rotate_image(scaled_image, angle)
    new_rect = new_rect.move(650, 50)
    screen.blit(new_image, new_rect)

    pygame.display.flip()  # Обновление экрана
    angle += 3
    clock.tick(FPS)

pygame.quit()
sys.exit()

if __name__ == "__main__":
    main()
