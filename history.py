import pygame
import os
import sys
import random


pygame.init()
pygame.mixer.init()
size = width, height = 1300, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Алмазная пещера: Новые приключения")
FPS = 50
GRAVITY = 1
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 100)

TIME = pygame.USEREVENT + 2
pygame.time.set_timer(TIME, 1000)

screen_rect = (0, 0, width, height)


def load_image(name, color_key=None):
    fullname = os.path.join('D:/data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def load_image_intro(name, color_key=None):
    fullname = os.path.join('D:/data/intro', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Particle(pygame.sprite.Sprite):
    fire0 = load_image("diamond.png")
    fire = []
    for scale in (5, 10, 15, 20, 25, 30):
        fire.append(pygame.transform.scale(fire0, (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


tile_images = {
    'wall': pygame.transform.scale(load_image('wall.jpg'), (50, 50)),
    'empty': pygame.transform.scale(load_image('pol.jpg'), (50, 50)),
    'diamond_wall': pygame.transform.scale(load_image('diamondblock.png'), (50, 50)),
    'fall': pygame.transform.scale(load_image('fall.jpg'), (50, 50)),
    'shadow_wall_1': pygame.transform.scale(load_image('wall1.png'), (50, 50)),
    'shadow_wall_2': pygame.transform.scale(load_image('shadow.png'), (50, 50)),
    'axe': pygame.transform.scale(load_image('axe.png'), (50, 50)),
    'pickaxe': pygame.transform.scale(load_image('pickaxe.png'), (50, 50)),
    'diamond': pygame.transform.scale(load_image('diamond.png'), (50, 50)),
    'box': pygame.transform.scale(load_image('box.png'), (50, 50)),
    'box_with_pickaxe': pygame.transform.scale(load_image('box.png'), (50, 50)),
    'box_with_heath': pygame.transform.scale(load_image('box.png'), (50, 50)),
    'box_with_time': pygame.transform.scale(load_image('box.png'), (50, 50)),
    'finish': pygame.transform.scale(load_image('finish.png'), (50, 50)),
    'heart': pygame.transform.scale(load_image('heart.png'), (50, 50)),
    'time': pygame.transform.scale(load_image('time.png'), (50, 50))
}
player_image = pygame.transform.scale(load_image("player3.png"), (50, 50))
arrow_image = load_image("arrow.png")
player_image1 = pygame.transform.rotate(player_image, 180)
player_image2 = pygame.transform.rotate(player_image, 90)
player_image3 = pygame.transform.rotate(player_image, 270)

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, width, height)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.heath = 100
        self.have_axe = False
        self.pickaxes = 0
        if self.pickaxes <= 0:
            self.have_pickaxe = False
        else:
            self.have_pickaxe = True
        self.time = 63
        self.diamonds = 0
        self.points = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def get_points(self):
        self.points += self.time + 50
        self.points *= (self.diamonds + 1) * 10
        return self.points

    def get_damaged(self, damage):
        self.heath -= damage
        if self.heath <= 0:
            defeat()
            pygame.mixer.quit()
            pygame.mixer.init()

    def find_axe(self):
        self.have_axe = True
        return self.have_axe

    def find_pickaxe(self):
        self.pickaxes += 1
        self.have_pickaxe = True
        return self.have_pickaxe

    def use_pickaxe(self):
        self.pickaxes -= 1
        if self.pickaxes == 0:
            self.have_pickaxe = False
            return self.have_pickaxe


class Arrow(Sprite):
    arrow = arrow_image
    arrow0 = []

    def __init__(self, pos):
        super().__init__(arrow_group)
        self.image = self.arrow
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        if not self.rect.colliderect(screen_rect):
            self.kill()


player = None
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
all_sprites = pygame.sprite.Group()
arrow_group = SpriteGroup()
enemy_group = SpriteGroup()
special_list = ['#', 'd', 'm', 'g', 'h', 't']
special_list_1 = ['#']


def terminate():
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


def create_particles(position):
    particle_count = 5
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def create_arrow(position):
    Arrow(position)


def intro():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    pygame.mixer.Sound('D:/data/sounds/icicles-shiny-bells.mp3').play()
    a = 0
    screen.blit(pygame.transform.scale(load_image_intro(f'{a}.png'), size1), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound('D:/data/sounds/icicles-shiny-bells.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN or a == 25:
                return
            elif event.type == MYEVENTTYPE:
                a += 1
                if a < 25:
                    screen.blit(pygame.transform.scale(load_image_intro(f'{a}.png'), size1), (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').play(loops=-1)
    fon = pygame.transform.scale(load_image('Newfon1.png'), size1)
    fon1 = pygame.transform.scale(load_image("Newfon2.png"), size1)
    screen.blit(fon, (0, 0))
    poss = False
    copyright_text = ["GS Production: 2021; Diamond Cave: New Adventures; vers 1.0.1; beta_version"]
    font = pygame.font.Font(None, 25)
    text_coord = 475
    string_rendered = None
    intro_rect = None
    for line in copyright_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 0
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 608 <= event.pos[0] <= 795 and 108 <= event.pos[1] <= 156:
                    pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').stop()
                    return
                else:
                    create_particles(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                create_arrow(pygame.mouse.get_pos())
                if 608 <= event.pos[0] <= 795 and 108 <= event.pos[1] <= 156:
                    if not poss:
                        pygame.mixer.Sound('D:/data/sounds/gunshot-dryfir.mp3').play()
                        poss = True
                    screen.blit(fon1, (0, 0))
                    create_arrow(pygame.mouse.get_pos())
                    screen.blit(string_rendered, intro_rect)
                else:
                    poss = False
                    screen.blit(fon, (0, 0))
                    screen.blit(string_rendered, intro_rect)
        arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
        arrow_group.draw(screen)
        if not poss:
            all_sprites.update()
            screen.blit(fon, (0, 0))
            arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
            arrow_group.draw(screen)
            all_sprites.draw(screen)
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


def defeat():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').play()
    fon = pygame.transform.scale(load_image('gameover.jpg'), (800, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').stop()
                return
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                create_arrow(pygame.mouse.get_pos())
        screen.blit(fon, (0, 0))
        arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
        arrow_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def finish():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    pygame.mixer.Sound('D:/data/sounds/trevor-morris-cappuccino-clouds.mp3').play()
    fon = pygame.transform.scale(load_image('308.jpg'), size1)
    screen.blit(fon, (0, 0))
    hero.get_points()
    intro_text = [f"Очки: {hero.points}", "",
                  "Нажмите кнопкой мыши для завершения игры!"]
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 100
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound('D:/data/sounds/trevor-morris-cappuccino-clouds.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound('D:/data/sounds/trevor-morris-cappuccino-clouds.mp3').stop()
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "D:/data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
            elif level[y][x] == 'd':
                Tile('diamond_wall', x, y)
            elif level[y][x] == 'n':
                Tile('fall', x, y)
            elif level[y][x] == 's':
                Tile('shadow_wall_1', x, y)
            elif level[y][x] == '+':
                Tile('shadow_wall_2', x, y)
            elif level[y][x] == 'p':
                Tile('axe', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Tile('diamond', x, y)
            elif level[y][x] == 'm':
                Tile('box', x, y)
            elif level[y][x] == 'g':
                Tile('box_with_pickaxe', x, y)
            elif level[y][x] == 'h':
                Tile('box_with_heath', x, y)
            elif level[y][x] == 't':
                Tile('box_with_time', x, y)
            elif level[y][x] == 'f':
                Tile('finish', x, y)
            elif level[y][x] == '1':
                Tile('heart', x, y)
            elif level[y][x] == '2':
                Tile('time', x, y)
            elif level[y][x] == '3':
                Tile('pickaxe', x, y)
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] not in special_list:
            hero.move(x, y - 1)
            if level_map[y - 1][x] == 's':
                Tile('shadow_wall_2', x, y - 1)
                level_map[y - 1][x] = '+'
            elif level_map[y - 1][x] == 'n':
                hero.get_damaged(101)
            elif level_map[y - 1][x] == '!':
                pygame.mixer.Sound('D:/data/sounds/fantasy_game_crafting_select_gem.mp3').play()
                hero.diamonds += 1
                Tile('empty', x, y - 1)
                level_map[y - 1][x] = '.'
            elif level_map[y - 1][x] == 'f':
                finish()
            elif level_map[y - 1][x] == 'p':
                hero.have_axe = True
                Tile('empty', x, y - 1)
                level_map[y - 1][x] = '.'
            elif level_map[y - 1][x] == '1':
                hero.heath += 125
                Tile('empty', x, y - 1)
                level_map[y - 1][x] = '.'
            elif level_map[y - 1][x] == '2':
                hero.time += 15
                Tile('empty', x, y - 1)
                level_map[y - 1][x] = '.'
            elif level_map[y - 1][x] == '3':
                hero.find_pickaxe()
                Tile('empty', x, y - 1)
                level_map[y - 1][x] = '.'
        else:
            if y > 0 and level_map[y - 1][x] == special_list[0]:
                pass
            elif y > 0 and level_map[y - 1][x] == special_list[1]:
                if hero.have_pickaxe:
                    pygame.mixer.Sound('D:/data/sounds/game_sound_gem_treasure_found_001_38372.mp3').play()
                    hero.use_pickaxe()
                    Tile('empty', x, y - 1)
                    Tile('diamond', x, y - 1)
                    level_map[y - 1][x] = '!'
                else:
                    pass
            elif y > 0 and level_map[y - 1][x] == special_list[2]:
                if hero.have_axe:
                    Tile('empty', x, y - 1)
                    level_map[y - 1][x] = '.'
                else:
                    pass
            elif y > 0 and level_map[y - 1][x] == special_list[3]:
                if hero.have_axe:
                    Tile('empty', x, y - 1)
                    Tile('pickaxe', x, y - 1)
                    level_map[y - 1][x] = '3'
                else:
                    pass
            elif y > 0 and level_map[y - 1][x] == special_list[4]:
                if hero.have_axe:
                    Tile('empty', x, y - 1)
                    Tile('heart', x, y - 1)
                    level_map[y - 1][x] = '1'
                else:
                    pass
            elif y > 0 and level_map[y - 1][x] == special_list[5]:
                if hero.have_axe:
                    Tile('empty', x, y - 1)
                    Tile('time', x, y - 1)
                    level_map[y - 1][x] = '2'
                else:
                    pass
    elif movement == "down":
        if y < max_y and level_map[y + 1][x] not in special_list:
            hero.move(x, y + 1)
            if level_map[y + 1][x] == 's':
                Tile('shadow_wall_2', x, y + 1)
                level_map[y + 1][x] = '+'
            elif level_map[y + 1][x] == 'n':
                hero.get_damaged(101)
            elif level_map[y + 1][x] == '!':
                pygame.mixer.Sound('D:/data/sounds/fantasy_game_crafting_select_gem.mp3').play()
                hero.diamonds += 1
                level_map[y + 1][x] = '.'
                Tile('empty', x, y + 1)
            elif level_map[y + 1][x] == 'f':
                finish()
            elif level_map[y + 1][x] == 'p':
                hero.have_axe = True
                Tile('empty', x, y + 1)
                level_map[y + 1][x] = '.'
            elif level_map[y + 1][x] == '1':
                hero.heath += 125
                Tile('empty', x, y + 1)
                level_map[y + 1][x] = '.'
            elif level_map[y + 1][x] == '2':
                hero.time += 15
                Tile('empty', x, y + 1)
                level_map[y + 1][x] = '.'
            elif level_map[y + 1][x] == '3':
                hero.find_pickaxe()
                Tile('empty', x, y + 1)
                level_map[y + 1][x] = '.'
        else:
            if y < max_y and level_map[y + 1][x] == special_list[0]:
                pass
            elif y < max_y and level_map[y + 1][x] == special_list[1]:
                if hero.have_pickaxe:
                    pygame.mixer.Sound('D:/data/sounds/game_sound_gem_treasure_found_001_38372.mp3').play()
                    hero.use_pickaxe()
                    Tile('empty', x, y + 1)
                    Tile('diamond', x, y + 1)
                    level_map[y + 1][x] = '!'
                else:
                    pass
            elif y < max_y and level_map[y + 1][x] == special_list[2]:
                if hero.have_axe:
                    Tile('empty', x, y + 1)
                    level_map[y + 1][x] = '.'
                else:
                    pass
            elif y < max_y and level_map[y + 1][x] == special_list[3]:
                if hero.have_axe:
                    Tile('empty', x, y + 1)
                    Tile('pickaxe', x, y + 1)
                    level_map[y + 1][x] = '3'
                else:
                    pass
            elif y < max_y and level_map[y + 1][x] == special_list[4]:
                if hero.have_axe:
                    Tile('empty', x, y + 1)
                    Tile('heart', x, y + 1)
                    level_map[y + 1][x] = '1'
                else:
                    pass
            elif y < max_y and level_map[y + 1][x] == special_list[5]:
                if hero.have_axe:
                    Tile('empty', x, y + 1)
                    Tile('time', x, y + 1)
                    level_map[y + 1][x] = '2'
                else:
                    pass
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] not in special_list:
            hero.move(x - 1, y)
            if level_map[y][x - 1] == 's':
                Tile('shadow_wall_2', x - 1, y)
                level_map[y][x - 1] = '+'
            elif level_map[y][x - 1] == 'n':
                hero.get_damaged(101)
            elif level_map[y][x - 1] == '!':
                pygame.mixer.Sound('D:/data/sounds/fantasy_game_crafting_select_gem.mp3').play()
                hero.diamonds += 1
                Tile('empty', x - 1, y)
                level_map[y][x - 1] = '.'
            elif level_map[y][x - 1] == 'f':
                finish()
            elif level_map[y][x - 1] == 'p':
                hero.have_axe = True
                Tile('empty', x - 1, y)
                level_map[y][x - 1] = '.'
            elif level_map[y][x - 1] == '1':
                hero.heath += 125
                Tile('empty', x - 1, y)
                level_map[y][x - 1] = '.'
            elif level_map[y][x - 1] == '2':
                hero.time += 15
                Tile('empty', x - 1, y)
                level_map[y][x - 1] = '.'
            elif level_map[y][x - 1] == '3':
                hero.find_pickaxe()
                Tile('empty', x - 1, y)
                level_map[y][x - 1] = '.'
        else:
            if x > 0 and level_map[y][x - 1] == special_list[0]:
                pass
            elif x > 0 and level_map[y][x - 1] == special_list[1]:
                if hero.have_pickaxe:
                    pygame.mixer.Sound('D:/data/sounds/game_sound_gem_treasure_found_001_38372.mp3').play()
                    hero.use_pickaxe()
                    Tile('empty', x - 1, y)
                    Tile('diamond', x - 1, y)
                    level_map[y][x - 1] = '!'
                else:
                    pass
            elif x > 0 and level_map[y][x - 1] == special_list[2]:
                if hero.have_axe:
                    Tile('empty', x - 1, y)
                    level_map[y][x - 1] = '.'
                else:
                    pass
            elif x > 0 and level_map[y][x - 1] == special_list[3]:
                if hero.have_axe:
                    Tile('empty', x - 1, y)
                    Tile('pickaxe', x - 1, y)
                    level_map[y][x - 1] = '3'
                else:
                    pass
            elif x > 0 and level_map[y][x - 1] == special_list[4]:
                if hero.have_axe:
                    Tile('empty', x - 1, y)
                    Tile('heart', x - 1, y)
                    level_map[y][x - 1] = '1'
                else:
                    pass
            elif x > 0 and level_map[y][x - 1] == special_list[5]:
                if hero.have_axe:
                    Tile('empty', x - 1, y)
                    Tile('time', x - 1, y)
                    level_map[y][x - 1] = '2'
                else:
                    pass
    elif movement == "right":
        if x < max_x and level_map[y][x + 1] not in special_list:
            hero.move(x + 1, y)
            if level_map[y][x + 1] == 's':
                Tile('shadow_wall_2', x + 1, y)
                level_map[y][x + 1] = '+'
            elif level_map[y][x + 1] == 'n':
                hero.get_damaged(101)
            elif level_map[y][x + 1] == '!':
                pygame.mixer.Sound('D:/data/sounds/fantasy_game_crafting_select_gem.mp3').play()
                hero.diamonds += 1
                Tile('empty', x + 1, y)
                level_map[y][x + 1] = '.'
            elif level_map[y][x + 1] == 'f':
                finish()
            elif level_map[y][x + 1] == 'p':
                hero.have_axe = True
                Tile('empty', x + 1, y)
                level_map[y][x + 1] = '.'
            elif level_map[y][x + 1] == '1':
                hero.heath += 125
                Tile('empty', x + 1, y)
                level_map[y][x + 1] = '.'
            elif level_map[y][x + 1] == '2':
                hero.time += 15
                Tile('empty', x + 1, y)
                level_map[y][x + 1] = '.'
            elif level_map[y][x + 1] == '3':
                hero.find_pickaxe()
                Tile('empty', x + 1, y)
                level_map[y][x + 1] = '.'
        else:
            if x < max_x and level_map[y][x + 1] == special_list[0]:
                pass
            elif x < max_x and level_map[y][x + 1] == special_list[1]:
                if hero.have_pickaxe:
                    pygame.mixer.Sound('D:/data/sounds/game_sound_gem_treasure_found_001_38372.mp3').play()
                    hero.use_pickaxe()
                    Tile('empty', x + 1, y)
                    Tile('diamond', x + 1, y)
                    level_map[y][x + 1] = '!'
                else:
                    pass
            elif x < max_x and level_map[y][x + 1] == special_list[2]:
                if hero.have_axe:
                    Tile('empty', x + 1, y)
                    level_map[y][x + 1] = '.'
                else:
                    pass
            elif x < max_x and level_map[y][x + 1] == special_list[3]:
                if hero.have_axe:
                    Tile('empty', x + 1, y)
                    Tile('pickaxe', x + 1, y)
                    level_map[y][x + 1] = '3'
                else:
                    pass
            elif x < max_x and level_map[y][x + 1] == special_list[4]:
                if hero.have_axe:
                    Tile('empty', x + 1, y)
                    Tile('heart', x + 1, y)
                    level_map[y][x + 1] = '1'
                else:
                    pass
            elif x < max_x and level_map[y][x + 1] == special_list[5]:
                if hero.have_axe:
                    Tile('empty', x + 1, y)
                    Tile('time', x + 1, y)
                    level_map[y][x + 1] = '1'
                else:
                    pass


def moved(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] not in special_list_1:
            return True
    elif movement == "down":
        if y < max_y and level_map[y + 1][x] not in special_list_1:
            return True
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] not in special_list_1:
            return True
    elif movement == "right":
        if x < max_x and level_map[y][x + 1] not in special_list_1:
            return True


intro()
start_screen()
pygame.mixer.quit()
pygame.mixer.init()


running = True
level_map = load_level("map1.txt")
hero, max_x, max_y = generate_level(level_map)
screen = pygame.display.set_mode((1300, 700))
pygame.display.set_caption("Алмазная пещера: Новые приключения")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or hero.heath <= 0:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                hero.image = player_image
                if moved(hero, "up"):
                    move(hero, "up")
            elif event.key == pygame.K_DOWN:
                hero.image = player_image1
                if moved(hero, "down"):
                    move(hero, "down")
            elif event.key == pygame.K_LEFT:
                hero.image = player_image2
                if moved(hero, "left"):
                    move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                hero.image = player_image3
                if moved(hero, "right"):
                    move(hero, "right")
        elif event.type == pygame.MOUSEMOTION:
            create_arrow(pygame.mouse.get_pos())
        elif event.type == TIME:
            if hero.time > 0:
                hero.time -= 1
            elif hero.time <= 0:
                hero.get_damaged(1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            create_particles(pygame.mouse.get_pos())
    screen.fill((0, 0, 0))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    all_sprites.draw(screen)
    all_sprites.update()
    arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
    arrow_group.draw(screen)
    intro_text = [f"Время: {hero.time}",
                  f"Здоровье: {hero.heath}",
                  f"Кирки: {hero.pickaxes}",
                  f'Алмазы: {hero.diamonds}']
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 1150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock.tick(FPS)
    pygame.display.flip()
pygame.mixer.quit()
pygame.quit()
