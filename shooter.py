from pygame import *
from random import randint
mixer.init()
mixer.music.load('assets/musictheme.ogg') #фонова музика
fire_sound = mixer.Sound("assets/laser.wav")
mixer.music.set_volume(0.2) #задаємо гучність
fire_sound.set_volume(0.4)
#mixer.music.play(-1)
TEXT_COLOR = (221, 245, 66)
BTN_COLOR = (46, 89, 61)
WIDTH, HEIGHT = 900, 600
FPS = 60

window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("space invaders")
clock = time.Clock() 


class GameSprite(sprite.Sprite):
    def __init__(self,name,image,x,y,width,height):
        super().__init__()
        self.name = name
        self.image = transform.scale(image,(width,height)) 
        self.rect = self.image.get_rect() # промокутна область картинки (хітбокс)
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)

    def draw(self):
        # відрисовуємо картинку self.image в кооординатах self.rect
        window.blit(self.image,self.rect)


class Player(GameSprite):
    def __init__(self, name, image, x, y, width, height, hp=3):
        super().__init__(name, image, x, y, width, height)
        self.hp =  hp

    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y >0:
            self.rect.y -= 7
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += 7
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 7
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 7
    
    def shoot(self):
        new_bullet = Bullet(self.rect.centerx - 5, self.rect.top)
        bullets.add(new_bullet)
        fire_sound.play()
        
class Alien(GameSprite):
    def __init__(self):
        super().__init__("pro alien",alien_image,randint(0,WIDTH - 100),randint(-300,-100),100,80)
        self.speed = randint(3,7)
    def update(self):
        global lost,Lost_text
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            lost += 1
            Lost_text = font1.render("Lost:"+ str(lost),True,TEXT_COLOR)

            self.rect.x = randint(0,WIDTH - 100)
            self.rect.y = randint(-300,-100)
            self.speed = randint(3,7)

class Meteor(GameSprite):
    def __init__(self):
        super().__init__("pro alien",meteor_image,randint(0,WIDTH - 100),randint(-300,-100),60,50)
        self.speed = randint(3,5)
    def update(self):

        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0,WIDTH - 100)
            self.rect.y = randint(-300,-100)
            self.speed = randint(3,5)



class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__("bullet",bullet_image,x,y,10,20)
        self.speed = 9
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -30:
           self.kill()
           

class Button(sprite.Sprite):
    def __init__(self, text, color,x,y ):
        super().__init__()
        self.font = font.Font("assets/Boxy-Bold.ttf",35)
        self.image = self.font.render(text,True,BTN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.color = color
        
    def draw(self):
        draw.rect(window, self.color, self.rect)
        window.blit(self.image,self.rect)

# завантажуємо картинки
bg_image = image.load("assets/infinite_starts.jpg")
player_image = image.load("assets/spaceship.png")
alien_image = image.load("assets/alien.png")    
bullet_image = image.load("assets/fire.png")
meteor_image = image.load("assets/Meteor1.png")

# створюємо написи
font.init()

font1 = font.Font("assets/Boxy-Bold.ttf",25)
font2 = font.Font("assets/Boxy-Bold.ttf",50)
restart_btn = Button(text="Restart", color = (33, 196, 90), x = WIDTH/2, y = 350)
game_over = font2.render("Game Over",True,TEXT_COLOR)

# створення фону
bg = transform.scale(bg_image,(WIDTH,HEIGHT))

y1 = 0
y2 = -HEIGHT

def start():
    global lost,score,score_text,Lost_text,hp_text,player,aliens,bullets,finish,game,meteors
    
    lost = 0
    score = 0
    score_text = font1.render("Score: 0",True,TEXT_COLOR)
    Lost_text = font1.render("Lost: 0",True,TEXT_COLOR)
    hp_text = font1.render("Lives: 3",True,TEXT_COLOR)

    
    # створення спрайтів
    player = Player("boneless",player_image,WIDTH / 2,HEIGHT - 200,120,100)
    aliens = sprite.Group()
    bullets = sprite.Group()
    meteors = sprite.Group()
    for i in range(5):
        alien = Alien()
        aliens.add(alien)
    
    for i in range(2):   
        meteor = Meteor() 
        meteors.add(meteor)
    finish = False
    game = True

start()

while game: # основний ігровий цикл
    window.blit(bg,(0,y1)) 
    window.blit(bg,(0,y2)) 
    y1+=1 
    y2+=1

    if y1 > HEIGHT:
        y1 = -HEIGHT
    
    if y2 > HEIGHT:
        y2 = -HEIGHT

    for e in event.get(): # перевіряємо кожну подію
        if e.type == QUIT: # якщо ми натиснули на хрестик
            game = False # гра завершується
        if e.type == KEYDOWN and e.key == K_SPACE:
            player.shoot()

        if finish == True and  e.type == MOUSEBUTTONDOWN: 
            left, middle, right = mouse.get_pressed()
            x, y = mouse.get_pos()
            if left == True and restart_btn.rect.collidepoint(x,y):
                start()                
                    
    if finish != True:
        
        player.update()
        aliens.update()
        bullets.update()
        meteors.update()
        
        collide_list = sprite.groupcollide(aliens,bullets,False,True, sprite.collide_mask)
        for collide in collide_list:
            score += 1
            score_text = font1.render("Score:"+ str(score),True,TEXT_COLOR)
            collide.rect.x = randint(0,WIDTH - 100)
            collide.rect.y = randint(-300,-100)
            collide.speed = randint(3,7)
        
        collide_list = sprite.spritecollide(player,aliens,True, sprite.collide_mask)
        for collide in collide_list:
            player.hp = player.hp -1
            hp_text = font1.render("Lives:" + str(player.hp),True,TEXT_COLOR)
            if player.hp <= 0:
                finish = True
                game_over = font2.render("Game Over",True,TEXT_COLOR)
        
        collide_list = sprite.spritecollide(player,meteors,True, sprite.collide_mask)
        for collide in collide_list:
            finish = True
            game_over = font2.render("Game Over",True,TEXT_COLOR)
        if score >= 25:
            finish = True
            game_over = font2.render("You win!!",True,TEXT_COLOR)
        if lost >= 25:
            finish = True
            game_over = font2.render("Game Over",True,TEXT_COLOR)
    aliens.draw(window)
    meteors.draw(window)
    player.draw()
    bullets.draw(window)

    window.blit(hp_text,(WIDTH - 150,50))
    window.blit(score_text,(WIDTH - 150,20))
    window.blit(Lost_text,(20,20))
    if finish == True:
        window.blit(game_over,(290,250))
        restart_btn.draw()
    display.update() # оновлення екрану
    clock.tick(FPS) # контроль FPS