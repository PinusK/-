import pygame
import sys
import os
import math

FPS = 30


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, activiti=False, fun=None):
        super().__init__(button_group)
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
        intro_rect.centery = self.rect.centery
        intro_rect.centerx = self.rect.centerx
        screen.blit(self.image, (x, y))
        screen.blit(string_rendered, intro_rect)
        self.string_rendered = string_rendered
        self.intro_rect = intro_rect
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
                if self.text.isdigit():
                    ind_level = int(self.text) - 1
                args[0][2] = self.fun

    def blit_text(self):
        screen.blit(self.string_rendered, self.intro_rect)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class TileTank(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


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
        sub_x = 0
        sub_y = 0
        if ind == 0:
            self.vx = 0
            self.vy = -v
            self.image = pygame.transform.rotate(self.image, 0)
            sub_x = self.image.get_rect().w // 2
        elif ind == 1:
            self.vx = -int(math.sqrt(v ** 2 // 2))
            self.vy = -int(math.sqrt(v ** 2 // 2))
        elif ind == 2:
            self.vx = -v
            self.vy = 0
            self.image = pygame.transform.rotate(self.image, 90)
            sub_y = self.image.get_rect().h // 2
        elif ind == 3:
            self.vx = -int(math.sqrt(v ** 2 // 2))
            self.vy = int(math.sqrt(v ** 2 // 2))
        elif ind == 4:
            self.vx = 0
            self.vy = v
            self.image = pygame.transform.rotate(self.image, 90)
            self.image = pygame.transform.rotate(self.image, 90)
            sub_x = self.image.get_rect().w // 2
        elif ind == 5:
            self.vx = int(math.sqrt(v ** 2 // 2))
            self.vy = int(math.sqrt(v ** 2 // 2))
        elif ind == 6:
            self.vx = v
            self.vy = 0
            self.image = pygame.transform.rotate(self.image, -90)
            sub_y = self.image.get_rect().h // 2
        elif ind == 7:
            self.vx = int(math.sqrt(v ** 2 // 2))
            self.vy = -int(math.sqrt(v ** 2 // 2))
        self.rect = self.image.get_rect().move(pos_x - sub_x, pos_y - sub_y)

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(self.vx, self.vy)
        flag_explosion = False
        if pygame.sprite.spritecollideany(self, inter_group):
            if pygame.sprite.spritecollideany(self, inter_group) != self.hunter:
                self.kill()
                flag_explosion = True
                hp_down(pygame.sprite.spritecollideany(self, inter_group))
        elif pygame.sprite.spritecollideany(self, player_group):
            if pygame.sprite.spritecollideany(self, player_group) != self.hunter:
                flag_explosion = True
                self.kill()
                hp_down(pygame.sprite.spritecollideany(self, player_group))
        if pygame.sprite.spritecollideany(self, wall_group):
            flag_explosion = True
            self.kill()
        if flag_explosion:
            if not channel3.get_busy():
                channel3.play(sound_explosion)
            elif not channel4.get_busy():
                channel4.play(sound_explosion)
            elif not channel5.get_busy():
                channel5.play(sound_explosion)
            elif not channel6.get_busy():
                channel6.play(sound_explosion)
            elif not channel7.get_busy():
                channel7.play(sound_explosion)
            elif not channel8.get_busy():
                channel8.play(sound_explosion)


class InterObject(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, inter_group)
        self.tile_type = tile_type
        self.image = tile_images[self.tile_type][0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.hp = 3
        self.points_kill = -100


class Gun(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, data=False):
        super().__init__(all_sprites, bunker_group, inter_group)
        self.tile_type = tile_type
        self.image2 = tile_images[self.tile_type][0]
        self.image = tile_images[self.tile_type][0]
        self.rect = self.image2.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.ind = 0
        self.ch_shot = 100
        self.hp = 3
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y
        self.w = self.rect.w
        self.h = self.rect.h
        self.pos_0 = (self.x + self.w // 2, self.y)
        self.pos_6 = (self.x + self.w, self.y + self.h // 2)
        self.pos_4 = (self.x + self.w // 2, self.y + self.h)
        self.pos_2 = (self.x, self.y + self.h // 2)
        self.data = data
        self.points_kill = 1000

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
            Bullet('rocket', self.x + self.w // 2,
                   self.y + self.h // 2, 20, pos[-1], self)


class Bunker(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, data=False):
        super().__init__(all_sprites, bunker_group, inter_group)
        self.tile_type = tile_type
        self.image = tile_images[self.tile_type][0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.ch_shot = 100
        self.hp = 3
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y
        self.w = self.rect.w
        self.h = self.rect.h
        self.pos_1 = (self.x, self.y)
        self.pos_0 = (self.x + self.w // 2, self.y)
        self.pos_7 = (self.x + self.w, self.y)
        self.pos_6 = (self.x + self.w, self.y + self.h // 2)
        self.pos_5 = (self.x + self.w, self.y + self.h)
        self.pos_4 = (self.x + self.w // 2, self.y + self.h)
        self.pos_3 = (self.x, self.y + self.h)
        self.pos_2 = (self.x, self.y + self.h // 2)
        self.data = data
        self.points_kill = 1500

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
            Bullet('snaryad', self.x + self.w // 2,
                   self.y + self.h // 2, 10, pos[-1], self)


class Data(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, data_groop)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.tile_type = tile_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.player_life_portal(self.tile_type, self.pos_x, self.pos_y)
        self.points = 0

    def update(self, *args, **kwargs):
        global life_player
        event = args[0]
        if event is not None:
            if event.key == pygame.K_SPACE:
                if self.ch_shot == 0 and self.ammun != 0:
                    Bullet('rocket', self.nx, self.ny, 20, self.position, self)
                    self.ch_shot = 30
                    self.ammun -= 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.flag = False
                if event.key == pygame.K_DOWN:
                    self.flag1 = False
            elif event.type == pygame.KEYDOWN:
                if self.flag1 or event.key == pygame.K_DOWN:
                    self.rect = self.rect.move(-self.vx, -self.vy)
                    self.combus -= 0.2
                    self.flag1 = True
                if self.flag or event.key == pygame.K_UP:
                    self.rect = self.rect.move(self.vx, self.vy)
                    self.combus -= 0.2
                    self.flag = True
                if pygame.sprite.spritecollideany(self, wall_group) or \
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
                self.vy = -5
            elif self.position == 2:
                self.vx = -5
                self.vy = 0
            elif self.position == 4:
                self.vx = 0
                self.vy = 5
            elif self.position == 6:
                self.vx = 5
                self.vy = 0
            if self.combus <= 0:
                if self.vx != 0:
                    if self.vx < 0:
                        self.vx += 4
                    if self.vx > 0:
                        self.vx -= 4
                if self.vy != 0:
                    if self.vy < 0:
                        self.vy += 4
                    if self.vy > 0:
                        self.vy -= 4
        if self.flag:
            self.rect = self.rect.move(self.vx, self.vy)
            self.combus -= 0.05
        if self.flag1:
            self.rect = self.rect.move(-self.vx, -self.vy)
            self.combus -= 0.05
        if pygame.sprite.spritecollideany(self, wall_group) or \
                pygame.sprite.spritecollideany(self, inter_group):
            vx = 0
            vy = 0
            if self.vx < 0:
                vx = -1
            if self.vx > 0:
                vx = 1
            if self.vy < 0:
                vy = -1
            if self.vy > 0:
                vy = 1
            while pygame.sprite.spritecollideany(self, wall_group) or \
                    pygame.sprite.spritecollideany(self, inter_group):
                if self.flag:
                    self.rect = self.rect.move(-vx, -vy)
                if self.flag1:
                    self.rect = self.rect.move(vx, vy)
        self.nx = self.rect.x + tile_width // 2
        self.ny = self.rect.y + tile_height // 2
        if self.hp == 0:
            life_player -= 1
            if self.flag_data:
                Data('data', self.rect.x + tile_width / 4, self.rect.y + tile_height / 4)
                self.flag_data = False
            TileTank('skeleton_tank', self.rect.x, self.rect.y)
            self.points -= 10000
            self.player_life_portal(self.tile_type, self.pos_x, self.pos_y)
        if self.ch_shot > 0:
            self.ch_shot -= 1
        if pygame.sprite.spritecollideany(self, data_groop):
            self.flag_data = True
            data = pygame.sprite.spritecollideany(self, data_groop)
            data.kill()

    def player_life_portal(self, tile_type, pos_x, pos_y):
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.flag = False
        self.flag1 = False
        self.flag_data = False
        self.ch_shot = 30
        self.hp = 3
        self.combus = 100
        self.ammun = 20
        self.vx = 0
        self.vy = 0
        self.nx = self.rect.x + tile_width / 2
        self.ny = self.rect.y
        self.position = 0

    def in_the_hangar(self):
        if self.ammun < 20:
            self.ammun += 1
            self.points -= 300
        if self.combus < 100:
            self.combus += 0.5
            self.points -= 50
        if self.hp < 3:
            self.hp += 1
            self.points -= 100


def hp_down(self):
    if self.hp > 0:
        self.hp -= 1
    if self.hp == 0:
        if self == player_group.sprites()[0]:
            pass
        else:
            if self in bunker_group:
                if self.data:
                    Data('data', self.x + tile_width / 4, self.y + tile_height / 4)
            self.image = tile_images[self.tile_type][1]
            self.remove(bunker_group, inter_group)
            player_group.sprites()[0].points += self.points_kill


def terminate():
    pygame.mixer.quit()
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
    with open(filename, 'r') as textFile:
        text = [line.strip() for line in textFile]
    # и подсчитываем максимальную длину
    # дополняем каждую строку пустыми клетками ('.')
    return text


def write_text_record(record, flag=False):
    with open('data/Record.txt', 'r') as textFile:
        text = [line.strip() for line in textFile]
    if int(text[ind_level + 2].split()[1]) < abs(int(record)):
        text[ind_level + 2] = str(text[ind_level + 2].split()[0]) + '    ' + str(record)
    if flag:
        if ind_level + 1 == int(text[0].split()[-1]):
            text[0] = text[0].split()[0] + ' ' + str(int(text[0].split()[-1]) + 1)
    text = '\n'.join(text)
    with open('data/Record.txt', 'w') as write_text:
        write_text.write(text)


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
    global angar
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == 'W':
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
            elif level[y][x] == 'D':
                Tile('empty', x, y)
                Bunker('bunker', x, y, data=True)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                angar = Tile('angar', x, y)
                Player('player', x, y)
    return


def start_screen():
    intro_text = ["                    ТАНКИ",
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
        intro_rect.x = 200
        text_coord += 600
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONUP:
                return
        pygame.display.flip()
        clock.tick(FPS)


def regulations_screen():
    intro_text = ["Правила игры:",
                  "Движение: стрелочки,",
                  "Стрельба: пробел",
                  "Пауза: ESC",
                  "Цель:уничтожить бункер противника"
                  " и забрать пакет данных",
                  '*Вы выезжаете из Ремонтной зоны, в ней вы можете',
                  'заправиться, пополнить боезопас и отремонтироваться,',
                  'сюда же нужно доставить пакет данных', '', '', '', '',
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
                    event.type == pygame.MOUSEBUTTONUP:
                return
        pygame.display.flip()
        clock.tick(FPS)


def record():
    intro_text = load_text_file('Record.txt')[1:]
    intro_text.insert(1, '')
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    Button(300, text_coord + 50, button_width / 1.5, button_height / 1.5,
           'Назад', activiti=True, fun=start_play_screen)
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
    button_coord_y = 100
    button_coord_x = 100
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
                Button(button_coord_x, button_coord_y, button_width * 1.5, button_height * 1.5,
                       sp_text_button[x], activiti=True, fun=sp_fun_button[0])
                button_coord_x += 75 * 1.5
            else:
                Button(button_coord_x, button_coord_y, button_width * 1.5, button_height * 1.5,
                       sp_text_button[x], activiti=False, fun=None)
                button_coord_x += 75 * 1.5
            if x - shag_x == 4:
                shag_x += 5
                break
        button_coord_y += 75 * 1.5
        button_coord_x = 100
        if shag_x == ln:
            break

    Button(300, button_coord_y, button_width / 1.5, button_height / 1.5, 'Назад', activiti=True, fun=start_play_screen)
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
    channel2.stop()
    if not channel1.get_busy():
        channel1.play(sound_peace, -1)
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_coord_y = 300
    button_coord_x = 300
    sp_text_button = ['Играть', 'Результаты', 'Выйти']
    sp_fun_button = [level_choice, record, terminate]
    for i in range(len(sp_text_button)):
        Button(button_coord_x, button_coord_y, button_width * 1.5, button_height * 1.5,
               sp_text_button[i], activiti=True, fun=sp_fun_button[i])
        button_coord_y += 50 * 2

    x = y = 0
    fun = None
    sp = [x, y, fun]
    flag = True
    while True:
        for event in pygame.event.get():
            if flag:
                flag = False
                break
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


def victory():
    global life_player
    channel2.stop()
    channel1.play(sound_peace, -1)
    fon = pygame.transform.scale(load_image('victory_game.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    intro_text = ["                    Победа", '', '',
                  f'Ваши очки: {player_group.sprites()[0].points + 10000}', '', '',
                  "Нажмите Enter для продолжения"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += 100
        screen.blit(string_rendered, intro_rect)

    write_text_record(player_group.sprites()[0].points + 10000, flag=True)
    life_player = 3
    button_group.empty()
    all_sprites.empty()
    tiles_group.empty()
    wall_group.empty()
    inter_group.empty()
    player_group.empty()
    bunker_group.empty()
    bullet_group.empty()
    data_groop.empty()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    return start_play_screen
        pygame.display.flip()
        clock.tick(FPS)


def over_game():
    global life_player
    channel2.stop()
    channel1.play(sound_peace, -1)
    fon = pygame.transform.scale(load_image('game_over.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    intro_text = ["                    Поражение", '', '',
                  f'Ваши очки: {player_group.sprites()[0].points}', '', '',
                  "Нажмите Enter для продолжения"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += 100
        screen.blit(string_rendered, intro_rect)

    write_text_record(player_group.sprites()[0].points)
    life_player = 3
    button_group.empty()
    all_sprites.empty()
    tiles_group.empty()
    wall_group.empty()
    inter_group.empty()
    player_group.empty()
    bunker_group.empty()
    bullet_group.empty()
    data_groop.empty()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    return start_play_screen
        pygame.display.flip()
        clock.tick(FPS)


def consol_game():
    size_combus = (400, 8)
    size_ammun = (400, 20)
    size_life = (100, 10)
    size_player_life = (200, 200)
    image = pygame.transform.scale(load_image('panel.jpg'), (WIDTH, 200))
    rect_image = image.get_rect().move(0, HEIGHT - 200)
    screen.blit(image, rect_image)
    # Топливо
    combus = player_group.sprites()[0].combus / 100
    image = pygame.Surface(size_combus,
                           pygame.SRCALPHA, 32)
    pygame.draw.rect(image, (255, 255, 0), (0, 0, size_combus[0] * combus, size_combus[1]))
    pygame.draw.rect(image, (0, 0, 0), (size_combus[0] * combus, 0,
                                        size_combus[0] - size_combus[0] * combus, size_combus[1]))
    rect_image = image.get_rect().move(200, HEIGHT - 150)
    screen.blit(image, rect_image)
    # Патроны
    image = pygame.Surface(size_ammun,
                           pygame.SRCALPHA, 32)
    ammun_ch = player_group.sprites()[0].ammun
    for i in range(0, 400, 20):
        image_cartridge = load_image('rocket.png')
        rect_image = image_cartridge.get_rect().move(i, 0)
        image.blit(image_cartridge, rect_image)
        ammun_ch -= 1
        if ammun_ch == 0:
            rect_image = image.get_rect().move(200, HEIGHT - 130)
            screen.blit(image, rect_image)
            break
    # Жизни Танка
    image = pygame.Surface(size_life,
                           pygame.SRCALPHA, 32)
    pygame.draw.rect(image, (0, 0, 0), (0, 0, size_life[0] - 5, size_life[1]))
    ch_hp = 0
    ch_iter = 5
    for i in range(3, size_life[0], 6):
        if ch_hp == 0:
            color = (255, 0, 0)
        elif ch_hp == 1:
            color = (255, 255, 0)
        else:
            color = (0, 255, 0)
        if ch_iter == 0:
            ch_iter = 5
            ch_hp += 1
        if ch_hp == player_group.sprites()[0].hp:
            rect_image = image.get_rect().move(300, HEIGHT - 100)
            screen.blit(image, rect_image)
            break
        pygame.draw.rect(image, color, (i, 0, 5, 10))
        ch_iter -= 1
    # Жизни Игрока
    image = pygame.Surface(size_player_life,
                           pygame.SRCALPHA, 32)
    spek_y = 20
    for i in range(0, life_player):
        image_life = load_image('tank_player.png')
        rect_image = image_life.get_rect()
        rect_image.y = spek_y
        spek_y += tile_height + 10
        image.blit(image_life, rect_image)
    rect_image = image.get_rect().move(50, HEIGHT - 200)
    screen.blit(image, rect_image)

    # Очки
    line = f'{player_group.sprites()[0].points}'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(line, True, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = HEIGHT - 75
    intro_rect.x = 250
    screen.blit(string_rendered, intro_rect)
    # qwertyuiop
    # сделаны игровые очки, музыка, игровой дисплей,


def start_mission():
    global life_player
    channel1.stop()
    if not channel2.get_busy():
        channel2.play(sound_peace, -1)
    pygame.display.flip()
    name_level = sp_level[ind_level]
    level = load_level(name_level)
    generate_level(level)

    button_coord_y = HEIGHT - 175
    button_coord_x = WIDTH - 175
    sp_text_button = ['Начать занова', 'Выйти']
    sp_fun_button = [start_mission, start_play_screen]
    for i in range(len(sp_text_button)):
        Button(button_coord_x, button_coord_y, button_width * 1.3, button_height * 1.3,
               sp_text_button[i], activiti=True, fun=sp_fun_button[i])
        button_coord_y += 75
    mouse_x = mouse_y = 0
    fun_button = None
    sp_button = [mouse_x, mouse_y, fun_button]
    stop_game = False
    while running:
        flag = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_game = not stop_game
                    break
            if stop_game:
                continue
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.KEYUP:
                player_group.update(event)
                flag = False
            if event.type == pygame.MOUSEBUTTONUP:
                sp_button[0], sp_button[1] = event.pos
                button_group.update(sp_button)
                if sp_button[2] is not None:
                    button_group.empty()
                    life_player = 3
                    button_group.empty()
                    all_sprites.empty()
                    tiles_group.empty()
                    wall_group.empty()
                    inter_group.empty()
                    player_group.empty()
                    bunker_group.empty()
                    bullet_group.empty()
                    data_groop.empty()
                    return sp_button[2]
        if stop_game:
            continue
        if life_player == 0:
            life_player = 3
            return over_game
        if pygame.sprite.spritecollideany(angar, player_group):
            if player_group.sprites()[0].flag_data:
                return victory
            else:
                player_group.sprites()[0].in_the_hangar()
        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        consol_game()
        bullet_group.update()
        if flag:
            player_group.update(None)
        x = player_group.sprites()[0].rect.x + 25
        y = player_group.sprites()[0].rect.y + 25
        bunker_group.update(x, y)
        all_sprites.draw(screen)
        data_groop.draw(screen)
        player_group.draw(screen)
        button_group.draw(screen)
        for i in button_group.sprites():
            i.blit_text()
        pygame.display.flip()
        clock.tick(FPS)


button_width = button_height = tile_width = tile_height = 50
sp_level = ['Mission01.txt', 'Mission02.txt', 'Mission03.txt',
            'Mission04.txt', 'Mission05.txt', 'Mission06.txt',
            'Mission07.txt', 'Mission08.txt', 'Mission09.txt',
            'Mission10.txt']
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    sound_war = pygame.mixer.Sound('data\\arthur-vyncke-black-sails.mp3')
    sound_peace = pygame.mixer.Sound('data\\Ekshen_-_Prost_ekshen_(iPleer.com).mp3')
    sound_explosion = pygame.mixer.Sound('data\\explosion.mp3')
    channel1 = pygame.mixer.Channel(1)
    channel2 = pygame.mixer.Channel(2)
    channel3 = pygame.mixer.Channel(3)
    channel4 = pygame.mixer.Channel(4)
    channel5 = pygame.mixer.Channel(5)
    channel6 = pygame.mixer.Channel(6)
    channel7 = pygame.mixer.Channel(7)
    channel8 = pygame.mixer.Channel(0)
    channel1.play(sound_peace, -1)
    size = WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode(size)
    tile_images = {'wall': load_image('wall.png'),
                   'empty': load_image('grass.png'),
                   'gun': [load_image('gun.png'), load_image('voronka.png')],
                   'bunker': [load_image('bunker.png'), load_image('voronka.png')],
                   'inter_object': [load_image('dom.png'), load_image('destroir_dom.png')],
                   'player': load_image('tank_player.png'),
                   'skeleton_tank': load_image('skeleton_tank.png'),
                   'rocket': load_image('rocket.png'),
                   'snaryad': load_image('snaryad.png'),
                   'angar': load_image('angar.png'),
                   'data': load_image('data.png')}
    screen.fill((125, 125, 125))
    running = True
    player = None
    ind_level = 0
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
    data_groop = pygame.sprite.Group()
    angar = None
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
