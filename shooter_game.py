from random import randint
from pygame import *

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

background_image = r'C:\Users\rudic\Downloads\catherine\personal\python\algorithmics\pictures\a1.jpg'
hero_image = 'rocket.png'
bullet_image = 'bullet.png'

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
score = 0
lost = 0
goal = 10
losing_amt = 3
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   #method to control the sprite with arrow keys
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
   def fire(self):
       bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

class Enemies(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width, win_height = 700, 500

display.set_caption('shooter game by Catherine Nathania Chandra')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(background_image), (win_width, win_height))



rocket = Player(hero_image, 5, win_height - 150, 80 ,100, 10)
finish = False
run = True
score = 0
lost = 0

monsters = sprite.Group()
bullets = sprite.Group()
enemy_image = 'ufo.png'
for i in range(1, 6):
    monster = Enemies(enemy_image, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()






    if not finish:
        window.blit(background, (0, 0))
        
        score_text = font2.render('Score:' + str(score), 1, (255, 255, 255))
        window.blit(score_text, (10, 20))
        lose_text = font2.render('Missed:' + str(lost), 1, (255, 255, 255)) 
        window.blit(lose_text, (10, 50))

        rocket.update()
        monsters.update()
        bullets.update()
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemies(enemy_image, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(rocket, monsters, True):
            lost += 1
            monster = Enemies(enemy_image, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(rocket, monsters, False) or lost >= losing_amt:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        score_text = font2.render("Score:" + str(score), 1, (255, 255, 255))
        window.blit(score_text, (10, 20))
        lose_text = font2.render("Missed:" + str(lost), 1, (255, 255, 255))
        window.blit(lose_text, (10, 50))
        display.update()
    else:
        finish = False
        run = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemies(enemy_image, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    time.delay(60)




