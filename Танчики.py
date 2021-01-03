import pygame
import sys
import os

FPS = 30


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, wall_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class InterObject(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, hp):
        super().__init__(tiles_group, all_sprites, inter_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.hp = hp

    def update(self, *args, **kwargs):
        pass


class Gun(InterObject):
    def __init__(self, tile_type, pos_x, pos_y, hp):
        super().__init__(tile_type, pos_x, pos_y, hp)
        self.ch_shot = 4

    def update(self, *args, **kwargs):
        pass


class Bunker(InterObject):
    def __init__(self, tile_type, pos_x, pos_y, hp):
        super().__init__(tile_type, pos_x, pos_y, hp)

    def update(self, *args, **kwargs):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.ch_shot = 4
        self.hp = 5
        self.combus = 100
        self.ammun = 20

    def update(self, *args, **kwargs):
        pass


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Танки", "",
                  "Правила игры",
                  "Движение: стрелочки,",
                  "Стрельба: пробел,",
                  "Цель : уничтожить бункер противника"
                  " и забрать пакет данных",
                  '*Вы выезжаете из ангара, в нем вы можете',
                  'заправиться, пополнить боезопас и отремонтироваться,',
                  'сюда же нужно доставить пакет данных']
    intro_text = ["Танки", "",
                  "", ]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def regulations_screen():
    pass


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'пушка':
                '''Tile('empty', x, y)
                Пушка('пушка', x, y)'''
            elif level[y][x] == 'бункер':
                '''Tile('empty', x, y)
                бункер('бункер', x, y)'''
    return


tile_images = {'wall': load_image('box.png'),
               'empty': load_image('grass.png')}
tile_width = tile_height = 50
sp_level = []
if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 750, 750
    screen = pygame.display.set_mode(size)
    start_screen()
    regulations_screen()
    running = True
    screen.fill((125, 125, 125))
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    inter_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = None
    screen1 = pygame.Surface(screen.get_size())
    screen1.fill((0, 0, 0))
    clock = pygame.time.Clock()
    for name_level in sp_level:
        level = load_level(name_level)
        generate_level(level)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            screen.fill((0, 0, 0))
            pygame.display.flip()
'''Идея реализации сохранения запомнить индекс уровня в списке
подумать над минами
отправлять в классы списки групп спрайтов'''
