#створи гру "Лабіринт"!
from pygame import *
mixer.init()
FPS = 60
TILESIZE = 35
WIDTH, HEIGHT = 20*TILESIZE, 15*TILESIZE
window = display.set_mode((WIDTH, HEIGHT))
mixer.music.load('sounds/Damiano_Baldoni_-_Witch.mp3')
mixer.music.play()
mixer.music.set_volume(0.01)
count = 0
display.set_caption('Лабіринт')

sprites = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, sprite_img, x, y, width, height):
        super().__init__(sprite_img, x, y, width, height)
        self.speed = 4
        self.keys = 0
        self.hp = 1
        sprites.remove(self)

    def update(self):
        pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if pressed[K_s] and self.rect.y < HEIGHT - TILESIZE:
            self.rect.y += self.speed

        if pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        if pressed[K_d] and self.rect.x < WIDTH - TILESIZE:
            self.rect.x += self.speed
    
        for w in walls:
            if sprite.collide_rect(player, w):
                self.rect.x, self.rect.y = old_pos


class Enemy(GameSprite):
    def __init__(self, x , y , sprite_img = 'images/ettin_old.png', speed = 2):
        super().__init__(sprite_img, x, y, 30, 30)
        self.speed = speed
    def update(self, walls):
        for w in walls:
            if sprite.collide_rect(self, w):
                self.speed = self.speed * -1

        self.rect.x += self.speed 


class Wall(GameSprite):
    def __init__(self, x , y, ):
        super().__init__('images/brick_brown_0.png', x, y, 35, 35)



player = Player('images/witch right.png', 40 , 350, 28, 28)
gold = GameSprite('images/closed_door.png', WIDTH - 30 , 458, 30, 30)
ground = transform.scale(image.load('images/pebble_brown_1_old.png'), (TILESIZE, TILESIZE))

walls = []
enemys = []
coins = []
stairs =sprite.Group()
keys =sprite.Group()
potions = sprite.Group() 
floor = 1

def load_map(floor = 1):
    walls.clear()
    enemys.clear()
    coins.clear()
    stairs.empty()
    sprites.empty()

    with open(f'map{floor}.txt', 'r') as file:
        x, y = 0, 0
        map = file.readlines()
        for line in map:
            for symbol in line:
                if symbol == 'W':
                    walls.append(Wall(x, y))
                elif symbol == 'P':
                    player.rect.x = x
                    player.rect.y = y
                elif symbol == 'F':
                    gold.rect.x = x
                    gold.rect.y = y
                elif symbol == 'E':
                    enemys.append(Enemy(x, y))
                elif symbol == 'K':
                    keys.add(GameSprite('images/key.png', x, y, 30, 30))
                elif symbol == 'A':
                    GameSprite('images/celtic_red.png', x, y, 30, 30)
                elif symbol == 'S':
                    stairs.add(GameSprite('images/stone_stairs_down.png', x, y, 30, 30))
                elif symbol == 'C':
                    GameSprite('images/chest_2_closed.png', x, y, 30, 30)
                elif symbol == 'G':
                    GameSprite('images/gem_bronze_old.png', x, y, 30, 30)
                elif symbol == 'L':
                    walls.append(GameSprite('images/altar_xom_7.png', x, y, 30, 30))
                elif symbol == 'B':
                    GameSprite('images/brick_brown_6.png', x, y, 35, 35)
                elif symbol == 'L':
                    GameSprite('images/altar_xom_7.png', x, y, 30, 30)
                elif symbol == 'D':
                    stairs.add(GameSprite('images/stone_stairs_up.png', x, y, 30, 30))
                elif symbol == 'Z':
                    potions.add(GameSprite('images/potion_puce.png', x, y, 30, 30))
                    
                x += 35
            y += 35
            x = 0

run = True
finish = False
clock = time.Clock()

font.init()
font1 = font.SysFont('Impact', 70)
font2 = font.SysFont('Impact', 25)
hp_text = font2.render(f'♥ {player.hp}', True, (255,0,0))
keys_text = font2.render(f'keys: {player.keys}/5', True, (255,255,255))
result = font1.render('YOU LOSE' , True, (140, 100, 30))

load_map(floor)
player.rect.x = 70
player.rect.y = 40

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        player.update()
        window.fill((0, 0, 0))
        for x in range(20):
            for y in range(15):
                window.blit(ground, (x*TILESIZE, y *TILESIZE))
        sprites.draw(window)
        player.draw()
        
        gold.draw()
        for w in walls:
            w.draw()

        for e in enemys:
            e.update(walls)
            if sprite.collide_rect(player, e):
                player.hp -= 1
                hp_text = font2.render(f'♥ {player.hp}', True, (255,0,0))
                enemys.remove(e)
                e.kill()
                if player.hp <= 0:
                    finish = True  

        if sprite.spritecollide(player, stairs, False):
            if floor == 1:
                floor = 2
            elif floor == 2:
                floor = 1
            load_map(floor)

        if sprite.spritecollide(player, keys, True):
            player.keys += 1
            keys_text = font2.render(f'keys: {player.keys}/5', True, (255,255,255))

        if sprite.spritecollide(player, potions, True):
            player.hp += 1
            hp_text = font2.render(f'♥ {player.hp}', True, (255,0,0))


        if sprite.collide_rect(player, gold):
            if player.keys == 5:
                finish = True
                result = font1.render('YOU WIN'  , True, (210, 150, 100))
            
    else:
        window.blit(result, (250, 200))
    window.blit(hp_text, (10, 5))
    window.blit(keys_text, (80, 5))
    display.update()
    clock.tick(FPS)