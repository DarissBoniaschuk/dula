
from pygame import *
from random import randint
#звук


class GameSprite(sprite.Sprite):

    def __init__(self, player_image , player_x , player_y, size_x, syze_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, syze_y)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset (self):
        window.blit(self.image,(self.rect.x , self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed [K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed  

            keys_pressed = key.get_pressed()
        if keys_pressed [K_RIGHT] and self.rect.x < win_width - 80 :
            self.rect.x += self.speed


    def fire(self):
        bullett = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullett)
#лічильник збитих і пропущених кораблів
    
score = 0
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



#ігрова сцена
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
#шрифти ы написи
font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)


txt_lose_game = font1.render("YOU LOSE", True, [255, 0, 0])
txt_win_game = font1.render("YOU WIN", True, [0, 255, 0])
#зображення
asteroid = 'gitler.png'
fon = 'galaxy.jpg'
rocket = 'lok.png'
bullets = 'bullet.png'

#спайти
bullets = sprite.Group()


rocket = Player(rocket, 5, win_height - 100, 80, 100, 20)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(asteroid, randint(80, win_width - 80), -40, 800, 500, randint(1, 5))
    monsters.add(monster) 

#змінна гра закінчилась

finish = False


#Основний цикл гри
run = True

while run:

    #подія натискання на кнопку закрити
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
        



    if not finish:

        window.blit(background, (0, 0))
        
        #пишемо текст на екрані

        text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #рухи спрайтів

        rocket.update()
        monsters.update()

        rocket.reset()
        
        monsters.draw(window)

        bullets.draw(window)
        bullets.update()

        if sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(txt_lose_game, (200, 200))
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy(asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster) 
            score += 1
        if score == 11:
            window.blit(txt_win_game, (200, 200))
            finish = True
        if lost >= 6:
            window.blit(txt_lose_game, (200, 200))
            finish = True
    else:
        score = 0
        lost = 0
        finish = False

        for m in monsters:
            m.kill()
        
        for m in bullets:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)




    display.update()

    time.delay(50)
