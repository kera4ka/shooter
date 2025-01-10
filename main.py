from pygame import *
from random import randint
from time import time as timer

# вынесем размер окна в константы для удобства
# W - width, ширина
# H - height, высота
WIN_W = 700
WIN_H = 500

FPS = 60

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)

SPEED1 = 5
SPEED2 = 1

x1,y1 = 0,WIN_H - 100
x2,y2 = 630,250
x3,y3 = WIN_W - 100,WIN_H - 100
size = 70

SCORE = 10
DEAD = 5
HEALTH = 2
BULLETIKI = 4
RECHARGE = 3

class GameSprite(sprite.Sprite):
    def __init__(self,img,x,y,width=65,height=65,speed=SPEED1):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            (width,height)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Bullet(GameSprite):
    def __init__(self,img,x,y,width=65,height=65,speed=SPEED2):
        super().__init__(img,x,y,width,height,speed)
    def update(self):       
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= (self.speed)

class Player(GameSprite):
    def __init__(self,img,x,y,width=65,height=65,speed=SPEED1,
            health = HEALTH,bulletiki = BULLETIKI,recharge = RECHARGE):
        super().__init__(img,x,y,width,height,speed)
        self.bullets = sprite.Group()
        self.score = 0
        self.lost = 0
        self.health = health
        self.totalbullets = bulletiki
        self.bulletiki = 0
        self.is_recharge = False
        self.recharge_time = recharge
        self.carenttimer = 0
        self.lasttimer = 0   
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x<WIN_W-self.rect.width:
            self.rect.x += self.speed
    def shoot(self,window,perezarad):
        if self.bulletiki <self.totalbullets and not self.is_recharge:
            bullet = Bullet('bullet.png',self.rect.x +(self.rect.width//2),self.rect.y,2,10 )
            self.bulletiki += 1
            self.bullets.add(bullet)

        if self.bulletiki >=self.totalbullets and not self.is_recharge:
            self.lasttimer = timer()
            self.is_recharge = True

        if self.is_recharge:
            self.carenttimer = timer()

            if self.carenttimer - self.lasttimer < self.recharge_time:
                window.blit(perezarad,(300,200))
                
            else:
                self.bulletiki = 0
                self.is_recharge = False

class Enemy(GameSprite):
    def __init__(self,img,x,y,width=65,height=65,speed=SPEED2):
        super().__init__(img,x,y,width,height,speed)
    def update(self,rocket):       
        if self.rect.y > WIN_H:
            self.rect.y = 0
            self.rect.x = randint(0,WIN_W - self.rect.width)
            rocket.lost += 1
        self.rect.y += (self.speed)


# создание окна размером 700 на 500
window = display.set_mode((WIN_W, WIN_H))

clock = time.Clock()

# mixer.init()
# mixer.music.load('1shaurma.wav')
# mixer.music.set_volume(0.5)
# mixer.music.play(-1)

# crash = mixer.Sound('3crash.wav')
# crash.set_volume(0.5)

font.init()
my_font = font.SysFont('verdana',70,)
my_font2 = font.SysFont('verdana',35,)
win = my_font.render('мировладелец', True, GREEN)
lose = my_font.render('шарики', True, RED)
schet_txt = my_font2.render('счет:',True,GREEN)
propusk_txt = my_font2.render('пропуск:',True,GREEN)
perezarad = my_font.render('перезарядка',True,RED)

schet = my_font2.render('0',True,GREEN)
propusk = my_font2.render('0',True,GREEN)

# название окна
display.set_caption("Догонялки")

# задать картинку фона такого же размера, как размер окна
background = transform.scale(
    image.load("galaxy.jpg"),
    # здесь - размеры картинки
    (WIN_W, WIN_H)
)
#чубрик 1
rocket = Player('rocket.png',x1,y1,width=35,height=65)

#чубрик 2

asteroids = sprite.Group()


for i in range(5):
    x = randint(0,WIN_W - 65)
    asteroid = Enemy('asteroid.png',x,0)
    asteroids.add(asteroid)

#чубрик 3

finish = False

# игровой цикл
game = True
while game:
    # слушать события и обрабатывать
    for e in event.get():
        # выйти, если нажат "крестик"
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:

            rocket.shoot(window,perezarad)                
    # отобразить картинку фона
    if not finish:
        window.blit(background,(0, 0))
        window.blit(schet_txt,(0,0))
        window.blit(propusk_txt,(0,40))
        schet = my_font2.render(str(rocket.score),True,GREEN)
        propusk = my_font2.render(str(rocket.lost),True,GREEN)
        window.blit(schet,(100,0))
        window.blit(propusk,(170,40))
        rocket.reset()
        rocket.update()
        asteroids.draw(window)
        asteroids.update(rocket)
        rocket.bullets.draw(window)
        rocket.bullets.update()

        rocket_vs_asteroids = sprite.spritecollide(
            rocket,asteroids,True
        )
        bullets_vs_asteroids = sprite.groupcollide(
            rocket.bullets,asteroids,True,True
        )

        if rocket_vs_asteroids or rocket.lost >= DEAD :
            if rocket.health == 0:
                window.blit(lose,(100,200)) 
                display.update()
                finish = True
            else:
                rocket.health -= 1
        if rocket.score >= SCORE:
            window.blit(win,(0,200))
            display.update()
            finish = True
        if bullets_vs_asteroids:
            x = randint(0,WIN_W - 65)
            asteroid = Enemy('asteroid.png',x,0)
            asteroids.add(asteroid)
            rocket.score += 1
        # if sprite.collide_rect(rocket, world):
        #     window.blit(win,(100,200))
        #     display.update()
        #     finish = True




    # обновить экран, чтобы отобрзить все изменения
    display.update()
    clock.tick(FPS)
