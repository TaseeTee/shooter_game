from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('Шутер')
lost = 0
c = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class PlayerSprite(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 625:
            self.rect.x += 10
        if keys[K_a] and self.rect.x > 5:
            self.rect.x += - 10
    def fire(self):
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            mfire.play()
class ЕnemySprite(GameSprite):
    def update(self):
        self.rect.y += 2
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 420)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= 15
        if self.rect.y < 0:
            self.kill()
background = transform.scale(image.load('galaxy.jpg'),(700,500))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mfire = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 18)
font2 = font.SysFont('Arial', 75)



mc = PlayerSprite('rocket.png', 350, 425, 65, 65, 10)

enemies = sprite.Group()
for enemy in range(5):
    enemy = ЕnemySprite('ufo.png', randint(0,625), 0, 65, 65, 5)
    enemies.add(enemy)
bullets = sprite.Group()

game = True

while game:
    window.blit(background,(0,0))
    bullets.draw(window)
    bullets.update()
    mc.reset()
    enemies.draw(window)
    mc.update()
    enemies.update()


    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                mc.fire()

    sprites_list1 = sprite.groupcollide(enemies, bullets, True, True)
    sprites_list2 = sprite.spritecollide(mc, enemies, False)

    text_lose = font1.render("Пропущено: " + str(lost), 1, (255,255,255))
    text_win = font1.render("Сбито: " + str(c), 1, (255,255,255))

    for enemy in range(len(sprites_list1)):
        enemy = ЕnemySprite('ufo.png', randint(0,625), 0, 65, 65, 5)
        enemies.add(enemy)
        c += 1        

    if c == 3:
        win = font2.render("Победа!", 1, (255,255,255))
        window.blit(win, (150, 250))
        game = False
    if lost >= 3 or len(sprites_list2) >= 1:
        lose = font2.render("Поражение" , 1, (255,255,255))
        window.blit(lose, (80, 250))
        game = False

    window.blit(text_lose, (500, 40))
    window.blit(text_win, (500, 80))
    display.update()    
    clock.tick(FPS)

