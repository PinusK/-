import pygame
import sys
import os
import random

FPS = 30


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, activiti=False, fun=None):
        super().__init__(button_group, all_sprites)
        self.image = pygame.Surface((w, h),
                                    pygame.SRCALPHA, 32)
        if activiti:
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, w, h), 0)
            self.fun = fun
        else:
            pygame.draw.rect(self.image, (75, 75, 75), (0, 0, w, h), 0)
            self.fun = None
        self.rect = pygame.Rect(x, y, w, h)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(text, True, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.centery = self.rect.centery + 10
        intro_rect.centerx = self.rect.centerx
        screen.blit(self.image, (x, y))
        screen.blit(string_rendered, (x, y))
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update(self, *args, **kwargs):
        if (args[0][0] >= self.x or args[0][0] <= self.x + self.w) and \
                (args[0][1] >= self.y or args[0][1] <= self.y + self.h):
            if self.fun is not None:
                args[0][2] = self.fun


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
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class InterObject(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, hp):
        super().__init__(tiles_group, all_sprites, inter_group)
        self.indx = random.randint(0, 1)
        self.image = tile_images[tile_type][self.indx]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.hp = hp

    def update(self, *args, **kwargs):
        hp_down(self)
        if self.hp == 0:
            self.image = tile_images[self.tile_type][self.indx + len(tile_images[self.tile_type]) / 2]


class Gun(InterObject):
    def __init__(self, tile_type, pos_x, pos_y, hp):
        super().__init__(tile_type, pos_x, pos_y, hp)
        self.ch_shot = 4

    def update(self, *args, **kwargs):
        hp_down(self)
        if self.hp == 0:
            self.image = tile_images[self.tile_type][self.indx + len(tile_images[self.tile_type]) / 2]


class Bunker(InterObject):
    def __init__(self, tile_type, pos_x, pos_y, hp):
        super().__init__(tile_type, pos_x, pos_y, hp)

    def update(self, *args, **kwargs):
        hp_down(self)
        if self.hp == 0:
            self.image = tile_images[self.tile_type][self.indx + len(tile_images[self.tile_type]) / 2]


class Player(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.player_life_portal(tile_type, pos_x, pos_y)
        self.flag = False
        self.flag1 = False

    def update(self, *args, **kwargs):
        global life_player
        event = args[0]
        if event.key == pygame.K_LEFT:
            self.image = pygame.transform.rotate(self.image, 45)
            self.position += 1
        if event.key == pygame.K_RIGHT:
            self.image = pygame.transform.rotate(self.image, -45)
            self.position -= 1
            if self.position == -1:
                self.position = 8 - 1
        self.rect = self.image.get_rect()
        if self.position == 8 or self.position == -8:
            self.position = 0
        if self.position == 0:
            self.vx = 0
            self.vy = -10
            self.nx = self.x
            self.ny = self.y
        elif self.position == 1:
            self.vx = -7.1
            self.vy = -7.1
            self.nx -= self.x * 2 / (2 ** (1 / 2))
            self.ny += self.y * 2 / (2 ** (1 / 2))
        elif self.position == 2:
            self.vx = -10
            self.vy = 0
            self.nx -= self.x * 2 / (2 ** (1 / 2))
            self.ny += self.y * 2 / (2 ** (1 / 2))
        elif self.position == 3:
            self.vx = -7.1
            self.vy = 7.1
            self.nx += self.x * 2 / (2 ** (1 / 2))
            self.ny += self.y * 2 / (2 ** (1 / 2))
        elif self.position == 4:
            self.vx = 0
            self.vy = 10
            self.nx += self.x * 2 / (2 ** (1 / 2))
            self.ny += self.y * 2 / (2 ** (1 / 2))
        elif self.position == 5:
            self.vx = 7.1
            self.vy = 7.1
            self.nx += self.x * 2 / (2 ** (1 / 2))
            self.ny -= self.y * 2 / (2 ** (1 / 2))
        elif self.position == 6:
            self.vx = 10
            self.vy = 0
            self.nx += self.x * 2 / (2 ** (1 / 2))
            self.ny -= self.y * 2 / (2 ** (1 / 2))
        elif self.position == 7:
            self.vx = 7.1
            self.vy = -7.1
            self.nx -= self.x * 2 / (2 ** (1 / 2))
            self.ny -= self.y * 2 / (2 ** (1 / 2))
        if event.key == pygame.K_DOWN or self.flag:
            self.rect.move(-self.vx, -self.vy)
            self.x -= self.vx
            self.y -= self.vy
            self.combus -= 0.1
            self.flag = True
        elif event.key == pygame.K_UP or self.flag1:
            self.rect.move(self.vx, self.vy)
            self.x += self.vx
            self.y += self.vy
            self.combus -= 0.1
            self.flag1 = True
        if event.key == pygame.K_KP_ENTER:
            # 'снаряд' = 'сняряд'(self.nx, self.ny, vx * 2, vy * 2)
            # 'снаряд'.update()
            # 'снаряд'.update()
            self.ammun -= 1
        hp_down(self)
        if self.hp == 0:
            life_player -= 1
            self.player_life_portal('', 1, 1)

    def player_life_portal(self, tile_type, pos_x, pos_y):
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.ch_shot = 4
        self.hp = 5
        self.combus = 100
        self.ammun = 20
        self.vx = 10
        self.vy = 10
        self.x = 25
        self.y = 50
        self.nx = 25
        self.ny = 50
        self.position = 0


def hp_down(self):
    if pygame.sprite.spritecollideany(self, 'группа пуль'):
        self.hp -= 1


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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


def start_screen():
    intro_text = ["Танки", "", "", "", "",
                  "Нажмите любую клавишу для продолжения"]
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
    intro_text = ["Танки", "",
                  "Правила игры",
                  "Движение: стрелочки,",
                  "Стрельба: пробел,",
                  "Цель : уничтожить бункер противника"
                  " и забрать пакет данных",
                  '*Вы выезжаете из ангара, в нем вы можете',
                  'заправиться, пополнить боезопас и отремонтироваться,',
                  'сюда же нужно доставить пакет данных',
                  "Нажмите любую клавишу для продолжения"]
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
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_play_screen():
    image = pygame.Surface((WIDTH, HEIGHT),
                           pygame.SRCALPHA, 32)
    pygame.draw.rect(image, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 0)
    screen.blit(image, (0, 0))
    button_coord = 100
    x = 100
    button_width = button_height = 50
    sp_text_button = ['Играть', 'Результаты', 'Выйти']
    sp_fun_button = [level_choice, record, terminate]
    for i in range(len(sp_text_button)):
        Button(x, button_coord, button_width, button_height, sp_text_button[i], activiti=True, fun=sp_fun_button[i])
        button_coord += 10
        button_coord += 50

    flag_mouse = False
    x = y = 0
    fun = None
    sp = [x, y, fun]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag_mouse = True
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if flag_mouse:
                    button_group.update(sp)
                    return sp[2]
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('box.png'),
               'empty': load_image('grass.png')}
tile_width = tile_height = 50
sp_level = []
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    sound_war = pygame.mixer.Sound('data\\arthur-vyncke-black-sails.mp3')
    sound_peace = pygame.mixer.Sound('data\\Ekshen_-_Prost_ekshen_(iPleer.com).mp3')
    # sound_pleace
    size = WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode(size)
    screen.fill((125, 125, 125))
    running = True
    player = None
    ind_level = 0
    '''screen1 = pygame.Surface(screen.get_size())
    screen1.fill((0, 0, 0))'''
    name_level = sp_level[ind_level]
    level = load_level(name_level)
    generate_level(level)
    life_player = 3
    clock = pygame.time.Clock()
    button_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    inter_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    start_screen()
    regulations_screen()
    fun = start_play_screen()
    while running:
        fun = fun()
        '''flag = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                player_group.update()
                flag = False
        'пуля_гроуп.update()'
        if flag:
            player_group.update()
        inter_group.update()
        'gun_group.update()'
        all_sprites.draw()
        screen.fill((125, 125, 125))
        pygame.display.flip()'''


'''Идея реализации сохранения запомнить индекс уровня в списке
подумать над минами
отправлять в классы списки групп спрайтов
Отправлять из функций отображения игры функцию следующего окна'''
