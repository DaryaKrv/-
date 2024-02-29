import os
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 50
WIDTH = 500
HEIGHT = 500
STEP = 50
CELL_SIZE = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, png=False, del_background=False):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл не найден")
        quit()
    image = pygame.image.load(fullname)
    if del_background:
        del_color = image.get_at((0, 0))
        image.set_colorkey(del_color)
    if not png:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image


def start_game():
    fon = pygame.transform.scale(load_image(name='fon.png', png=True, del_background=True), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    coords_y = 125
    intro_text = ["Стартовый экран","пробел, чтобы начать игру"]
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        coords_y += 5
        intro_rect.top = coords_y
        intro_rect.x = 111
        coords_y += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_levels(name):
    with open(os.path.join('data', name), mode='r') as file:
        level_map = [i.strip() for i in file]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_levels(level):
    player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == "@":
                Tile('empty', x, y)
                player = Player(x, y)
            elif level[y][x] == "#":
                Tile('box', x, y)
    return player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        self.tile_images_and_sprites = {'box': load_image(name='box.png', png=True, del_background=False),
                                        'empty': load_image(name='grass.png', png=True, del_background=False),

                                        }
        super().__init__(tiles_group, all_sprites)
        self.image = self.tile_images_and_sprites[obj]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect().move(CELL_SIZE * x, CELL_SIZE * y)
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = load_image(name='mario.png', png=True, del_background=True)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 15
        self.rect.y = y * CELL_SIZE + 5

    def update(self, event):
        x, y = self.rect.x // CELL_SIZE, self.rect.y // CELL_SIZE
        if event.key == pygame.K_LEFT:
            if x - 1 >= 0 and level[y][x - 1] != '#':
                self.rect.x -= STEP
        if event.key == pygame.K_RIGHT:
            if x + 1 < all_x and level[y][x + 1] != '#':
                self.rect.x += STEP
        if event.key == pygame.K_UP:
            if y - 1 >= 0 and level[y - 1][x] != '#':
                self.rect.y -= STEP
        if event.key == pygame.K_DOWN:
            if y + 1 < all_y and level[y + 1][x] != "#":
                self.rect.y += STEP


start_game()
level = load_levels('level.txt')
player, all_x, all_y = generate_levels(level)
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.update(event)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
