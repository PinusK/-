import pygame
import sys
import os
import math

FPS = 30


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, activiti=False, fun=None):
        super().__init__(button_group, all_sprites)
        if len(text) > 3:
            w = w * 2.5
        self.image = pygame.Surface((w, h),
                                    pygame.SRCALPHA, 32)
        if activiti:
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, w, h), 0)
            self.fun = fun
        else:
            pygame.draw.rect(self.image, (75, 75, 75), (0, 0, w, h), 0)
            self.fun = None
        self.rect = pygame.Rect(x, y, w, h)
        font = pygame.font.Font(None, 32)
        string_rendered = font.render(text, True, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.centery = self.rect.centery + 10
        intro_rect.centerx = self.rect.centerx
        screen.blit(self.image, (x, y))
        screen.blit(string_rendered, (x, y))
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update(self, *args, **kwargs):
        global ind_level
        if self.x + self.w >= args[0][0] >= self.x and \
                self.y + self.h >= args[0][1] >= self.y:
            if self.fun is not None:
                args[0][2] = self.fun
            if self.fun == start_mission:
                ind_level = int(self.text) - 1
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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, v, ind, hunter):
        super().__init__(bullet_group, all_sprites)
        self.hunter = hunter
        self.image = tile_images[tile_type]
        if ind == 0:
            self.vx = 0
            self.vy = -v
            self.image = pygame.transform.rotate(self.image, 0)
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        elif ind == 1:
            self.vx = -int(math.sqrt(v ** 2 // 2))
            self.vy = -int(math.sqrt(v ** 2 // 2))
            self.rect = self.image.get_rect().move(pos_x - 25, pos_y)
        elif ind == 2:
            self.vx = -v
            self.vy = 0
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect().move(pos_x - 25, pos_y + 25)
        elif ind == 3:
            self.vx = -int(math.sqrt(v ** 2 // 2))
            self.vy = int(math.sqrt(v ** 2 // 2))
            self.rect = self.image.get_rect().move(pos_x - 25, pos_y + 50)
        elif ind == 4:
            self.vx = 0
            self.vy = v
            self.image = pygame.transform.rotate(self.image, 90)
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect().move(pos_x, pos_y + 50)
        elif ind == 5:
            self.vx = int(math.sqrt(v ** 2 // 2))
            self.vy = int(math.sqrt(v ** 2 // 2))
            self.rect = self.image.get_rect().move(pos_x + 25, pos_y + 50)
        elif ind == 6:
            self.vx = v
            self.vy = 0
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect().move(pos_x + 25, pos_y + 25)
        elif ind == 7:
            self.vx = int(math.sqrt(v ** 2 // 2))
            self.vy = -int(math.sqrt(v ** 2 // 2))
            self.rect = self.image.get_rect().move(pos_x + 50, pos_y)

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, inter_group):
            if pygame.sprite.spritecollideany(self, inter_group) != self.hunter:
                self.kill()
                hp_down(pygame.sprite.spritecollideany(self, inter_group))
        elif pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            hp_down(pygame.sprite.spritecollideany(self,player_group))
        if pygame.sprite.spritecollideany(self, wall_group):
            self.kill()


class InterObject(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, inter_group)
        self.tile_type = tile_type
        self.image = tile_images[self.tile_type][0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.hp = 3

    def update(self, *args, **kwargs):
        print(2)
        if self.hp == 0:
            print(1)
            self.image = tile_images[self.tile_type][1]
            self.remove(inter_group)


class Gun(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, bunker_group, inter_group)
        self.tile_type = tile_type
        self.image2 = tile_images[self.tile_type][0]
        self.rect = self.image2.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.ind = 0
        self.ch_shot = 100
        self.hp = 3
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y
        self.pos_0 = (self.x + 25, self.y)
        self.pos_6 = (self.x + 50, self.y + 25)
        self.pos_4 = (self.x + 25, self.y + 50)
        self.pos_2 = (self.x, self.y + 25)

    def update(self, *args, **kwargs):
        x = args[0]
        y = args[1]
        r = list()
        r.append([abs(self.pos_0[0] - x) + abs(self.pos_0[1] - y), 0])
        r.append([abs(self.pos_2[0] - x) + abs(self.pos_2[1] - y), 2])
        r.append([abs(self.pos_4[0] - x) + abs(self.pos_4[1] - y), 4])
        r.append([abs(self.pos_6[0] - x) + abs(self.pos_6[1] - y), 6])
        pos = min(r)
        if pos[-1] != self.ind:
            self.image = pygame.transform.rotate(self.image2, pos[-1] // 2 * 90)
            self.ind = pos[-1]
        self.ch_shot -= 1
        if self.ch_shot == 0:
            self.ch_shot = 100
            Bullet('rocket', self.x + 25, self.y, 10, pos[-1], self)
        if self.hp == 0:
            self.image = tile_images[self.tile_type][1]
            self.remove(bunker_group, inter_group)


class Bunker(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, bunker_group, inter_group)
        self.tile_type = tile_type
        self.image = tile_images[self.tile_type][0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.ch_shot = 100
        self.hp = 3
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y
        self.pos_1 = (self.x, self.y)
        self.pos_0 = (self.x + 25, self.y)
        self.pos_7 = (self.x + 50, self.y)
        self.pos_6 = (self.x + 50, self.y + 25)
        self.pos_5 = (self.x + 50, self.y + 50)
        self.pos_4 = (self.x + 25, self.y + 50)
        self.pos_3 = (self.x, self.y + 50)
        self.pos_2 = (self.x, self.y + 25)

    def update(self, *args, **kwargs):
        x = args[0]
        y = args[1]
        r = list()
        r.append([abs(self.pos_1[0] - x) + abs(self.pos_1[1] - y), 1])
        r.append([abs(self.pos_0[0] - x) + abs(self.pos_0[1] - y), 0])
        r.append([abs(self.pos_7[0] - x) + abs(self.pos_7[1] - y), 7])
        r.append([abs(self.pos_6[0] - x) + abs(self.pos_6[1] - y), 6])
        r.append([abs(self.pos_5[0] - x) + abs(self.pos_5[1] - y), 5])
        r.append([abs(self.pos_4[0] - x) + abs(self.pos_4[1] - y), 4])
        r.append([abs(self.pos_3[0] - x) + abs(self.pos_3[1] - y), 3])
        r.append([abs(self.pos_2[0] - x) + abs(self.pos_2[1] - y), 2])
        pos = min(r)
        self.ch_shot -= 1
        if self.ch_shot == 0:
            self.ch_shot = 100
            Bullet('snaryad', self.x + 25, self.y, 10, pos[-1], self)
        if self.hp == 0:
            self.image = tile_images[self.tile_type][1]
            self.remove(bunker_group, inter_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.tile_type = tile_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.player_life_portal(self.tile_type, self.pos_x, self.pos_y)

    def update(self, *args, **kwargs):
        global life_player
        event = args[0]
        if event is not None:
            if event.key == pygame.K_SPACE:
                if self.ch_shot == 0 and self.ammun != 0:
                    Bullet('rocket', self.nx, self.ny, 20, self.position, self)
                    self.ch_shot = 40
                    self.ammun -= 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.flag = False
                if event.key == pygame.K_DOWN:
                    self.flag1 = False
            elif event.type == pygame.KEYDOWN:
                if self.flag1 or event.key == pygame.K_DOWN:
                    self.rect = self.rect.move(-self.vx, -self.vy)
                    self.combus -= 0.1
                    self.flag1 = True
                if self.flag or event.key == pygame.K_UP:
                    self.rect = self.rect.move(self.vx, self.vy)
                    self.combus -= 0.1
                    self.flag = True
                if pygame.sprite.spritecollideany(self, wall_group) or\
                        pygame.sprite.spritecollideany(self, inter_group):
                    if event.key == pygame.K_UP or self.flag:
                        self.rect = self.rect.move(-self.vx, -self.vy)
                    if event.key == pygame.K_DOWN or self.flag1:
                        self.rect = self.rect.move(self.vx, self.vy)
                if event.key == pygame.K_LEFT:
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.position += 2
                    if self.position == 8:
                        self.position = 0
                elif event.key == pygame.K_RIGHT:
                    self.image = pygame.transform.rotate(self.image, -90)
                    self.position -= 2
                    if self.position == -2:
                        self.position = 8 - 2
            if self.position == 0:
                self.vx = 0
                self.vy = -2
            elif self.position == 2:
                self.vx = -2
                self.vy = 0
            elif self.position == 4:
                self.vx = 0
                self.vy = 2
            elif self.position == 6:
                self.vx = 2
                self.vy = 0
            self.nx = self.rect.x + tile_width // 3.5
            self.ny = self.rect.y - tile_height // 3.5
        if self.flag:
            self.rect = self.rect.move(self.vx, self.vy)
        if self.flag1:
            self.rect = self.rect.move(-self.vx, -self.vy)
        if pygame.sprite.spritecollideany(self, wall_group) or\
                pygame.sprite.spritecollideany(self, inter_group):
            if self.flag:
                self.rect = self.rect.move(-self.vx, -self.vy)
            if self.flag1:
                self.rect = self.rect.move(self.vx, self.vy)
        if self.hp == 0:
            life_player -= 1
            self.player_life_portal(self.tile_type, self.pos_x, self.pos_y)
        if self.ch_shot > 0:
            self.ch_shot -= 1

    def player_life_portal(self, tile_type, pos_x, pos_y):
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        print(self.rect)
        self.flag = False
        self.flag1 = False
        self.ch_shot = 40
        self.hp = 5
        self.combus = 100
        self.ammun = 20
        self.vx = 0
        self.vy = 0
        self.nx = self.rect.x + tile_width / 2
        self.ny = self.rect.y
        self.position = 0


def hp_down(self):
    self.hp -= 1
    if self.hp == 0:
        self.image = tile_images[self.tile_type][1]
        self.remove(bunker_group, inter_group)



def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, 'w'), level_map))


def load_text_file(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    # дополняем каждую строку пустыми клетками ('.')
    return level_map


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
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == 'w':
                Tile('empty', x, y)
                Wall('wall', x, y)
            elif level[y][x] == 'O':
                Tile('empty', x, y)
                InterObject('inter_object', x, y)
            elif level[y][x] == 'P':
                Tile('empty', x, y)
                Gun('gun', x, y)
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                Bunker('bunker', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                Player('player', x, y)
    return


def start_screen():
    intro_text = ["Танки", "", "", "", "",
                  "Нажмите любую клавишу для продолжения"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('red'))
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


def regulations_screen():
    intro_text = ["Правила игры",
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
        string_rendered = font.render(line, True, pygame.Color('red'))
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


def record():
    intro_text = load_text_file('record')[1:]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    Button(200, 300, button_width, button_height, 'Назад', activiti=True, fun=start_play_screen)
    x = y = 0
    fun = None
    sp = [x, y, fun]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                sp[0], sp[1] = event.pos
                button_group.update(sp)
                if sp[2] is not None:
                    button_group.empty()
                    return sp[2]
        pygame.display.flip()
        clock.tick(FPS)


def level_choice():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_coord_y = 75
    button_coord_x = 25
    line = 'Миссия'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(line, True, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 100
    intro_rect.y = 25
    screen.blit(string_rendered, intro_rect)
    sp_text_button = load_text_file('Missii.txt')
    max_level = int(load_text_file('Record.txt')[0].split()[-1])
    sp_fun_button = [start_mission]
    ln = len(sp_text_button)
    shag_x = 0
    for y in range(ln):
        for x in range(shag_x, ln):
            if int(sp_text_button[x]) <= max_level:
                Button(button_coord_x, button_coord_y, button_width, button_height,
                       sp_text_button[x], activiti=True, fun=sp_fun_button[0])
                button_coord_x += 75
            else:
                Button(button_coord_x, button_coord_y, button_width, button_height,
                       sp_text_button[x], activiti=False, fun=None)
                button_coord_x += 75
            if x - shag_x == 9:
                shag_x += 10
                break
        button_coord_y += 75
        button_coord_x = 25

    x = y = 0
    fun = None
    sp = [x, y, fun]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                sp[0], sp[1] = event.pos
                button_group.update(sp)
                if sp[2] is not None:
                    button_group.empty()
                    return sp[2]
        pygame.display.flip()
        clock.tick(FPS)


def start_play_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_coord = 100
    x = 100
    sp_text_button = ['Играть', 'Результаты', 'Выйти']
    sp_fun_button = [level_choice, record, terminate]
    for i in range(len(sp_text_button)):
        Button(x, button_coord, button_width, button_height, sp_text_button[i], activiti=True, fun=sp_fun_button[i])
        button_coord += 10
        button_coord += 50

    x = y = 0
    fun = None
    sp = [x, y, fun]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                sp[0], sp[1] = event.pos
                button_group.update(sp)
                if sp[2] is not None:
                    button_group.empty()
                    return sp[2]
        pygame.display.flip()
        clock.tick(FPS)


def start_mission():
    channel1.stop()
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    channel2.play(sound_war, -1)
    name_level = sp_level[ind_level]
    level = load_level(name_level)
    generate_level(level)
    while running:
        flag = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.KEYUP:
                player_group.update(event)
                flag = False
        screen.fill((125, 125, 125))
        bullet_group.update()
        if flag:
            player_group.update(None)
        x = player_group.sprites()[0].rect.x + 25
        y = player_group.sprites()[0].rect.y + 25
        bunker_group.update(x, y)
        all_sprites.draw(screen)
        bunker_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


button_width = button_height = tile_width = tile_height = 50
sp_level = ['Mission01.txt']
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    sound_war = pygame.mixer.Sound('data\\arthur-vyncke-black-sails.mp3')
    sound_peace = pygame.mixer.Sound('data\\Ekshen_-_Prost_ekshen_(iPleer.com).mp3')
    channel1 = pygame.mixer.Channel(1)
    channel2 = pygame.mixer.Channel(2)
    channel1.play(sound_peace, -1)
    size = WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode(size)
    tile_images = {'wall': load_image('wall.png'),
                   'empty': load_image('grass.png'),
                   'gun': [load_image('gun.png'), load_image('voronka.png')],
                   'bunker': [load_image('bunker.png'), load_image('voronka.png')],
                   'inter_object': [load_image('dom.png'), load_image('destroir_dom.png')],
                   'player': load_image('tank_player.png'),
                   'rocket': load_image('rocket.png'),
                   'snaryad': load_image('snaryad.png')}
    # screen_rect = (0, 0, WIDTH, HEIGHT)
    screen.fill((125, 125, 125))
    running = True
    player = None
    ind_level = 0
    '''screen1 = pygame.Surface(screen.get_size())
    screen1.fill((0, 0, 0))'''
    life_player = 3
    clock = pygame.time.Clock()
    button_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    inter_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bunker_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
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
                player_group.update(event)
                flag = False
        'пуля_гроуп.update()'
        if flag:
            player_group.update(None)
        inter_group.update()
        'gun_group.update()'
        all_sprites.draw()
        screen.fill((125, 125, 125))
        pygame.display.flip()'''

'''Идея реализации сохранения запомнить индекс уровня в списке
подумать над минами
отправлять в классы списки групп спрайтов
Отправлять из функций отображения игры функцию следующего окна'''
