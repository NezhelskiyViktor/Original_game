import pygame as pg

pg.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Оконные настройки
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Прыжки персонажа')
clock = pg.time.Clock()
FPS = 60

# Игрок
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect(midbottom = (WIDTH // 2, HEIGHT - 30))
        self.velocity = 0
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity = JUMP_STRENGTH
            self.on_ground = False

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.bottom > HEIGHT - 30:
            self.rect.bottom = HEIGHT - 30
            self.on_ground = True
            self.velocity = 0

player = Player()

# Игровой цикл
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()

    player.update()

    # Отрисовка
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    pg.display.flip()

    clock.tick(FPS)

pg.quit()