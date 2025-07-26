import pygame
import random
import sys
import pdb
highscore = 0
hitboxx = 40
player_alive = True
player1_points = 0
hitboxy = 30
green = (0,255,0)
white = (255,255,255)
red = (255,0,0)
x = 800
y = 600
last_shot_time = 0
cooldown = 400
boss_spawned = False
sound_played = False

def update_highscore(player1_points,highscore):
    if player1_points > highscore:
        highscore = player1_points
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))

class Enemy():
    def __init__(self,img_path,steps,health):
        self.image = pygame.image.load(img_path)
        self.x = random.randint(300,600)    
        self.y = random.randint(30, 100)
        self.steps = steps
        self.enemyhealth = health
        steps = random.choice([-4,-3,-2,-1,1,2,3,4,])
        health = 2
        
    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))
    def movement(self):
        # Moves right when touched left border, moves left when touched right border.
        if self.x >= 760:
            self.steps = self.steps*-1
            self.y += random.choice([20,30])
        elif self.x  <= 0:
            self.steps = self.steps*-1
            self.y += random.choice([20,30])
        self.x += self.steps 
    def detection(self):

        for bullet in bulletlist:
            bullet.image_blit(screen)
            bullet.movement()
            for enemy in enemylist:
        #add bullet detection here
                if enemy.x <= bullet.x <= enemy.x+40 and enemy.y <= bullet.y <= enemy.y+30:
                    bulletlist.remove(bullet)
                    enemy.enemyhealth -= 1
                    if enemy.enemyhealth == 0:
                        enemylist.remove(enemy)
                        explosion_sound.play()
class Bullet():
    def __init__(self,playerx,playery):
        self.image = pygame.image.load("images/bullet.png")
        self.x = playerx+24
        self.y = playery
        self.speed = 7
    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))
    def movement(self):
        self.y -= self.speed

pygame.init()
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("SPACEWAR VER 1.0.0")
clock = pygame.time.Clock()
font1 = pygame.font.Font('freesansbold.ttf', 100)
font2 = pygame.font.Font('freesansbold.ttf', 30)
font3 = pygame.font.Font('freesansbold.ttf', 80)
text1= font1.render('YOU WIN', True,green)
text3= font3.render('WARZONE DEFEAT', True,red)

text1_rect = text1.get_rect(center=(x // 2, y // 2))
text3_rect = text3.get_rect(center=(x // 2, y // 2))



# Load images
background = pygame.image.load("images/backround.jpg")
playerimage = pygame.image.load("images/spaceship.png")
# Load sounds
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
win_sound = pygame.mixer.Sound("sounds/win_sound.wav")
# Initial positions
playerx = 380
playery = 450
bulletlist = []
enemylist = []
playerx += 5
for i in range(10):
    enemylist.append(Enemy("images/enemy_green.png",random.choice([-4,-3,-2,-1,1,2,3,4,]),2))

while True:
    
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        print(pygame.event.event_name(event.type))
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if current_time - last_shot_time >= cooldown:

                if event.key == pygame.K_SPACE:
                    bullet = Bullet(playerx, playery)
                    bulletlist.append(bullet)
                    shoot_sound.play()
                    last_shot_time = current_time
    # Handle movement on key press inside event loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerx -= 5 
    if keys[pygame.K_RIGHT]:
        playerx += 5
    if keys[pygame.K_d]:
        playerx += 5
    if keys[pygame.K_s]:
        playery += 5
    if keys[pygame.K_w]:
        playery += -5
    if keys[pygame.K_a]:
        playerx += -5
    if keys[pygame.K_UP]:
        playery += -5
    if keys[pygame.K_DOWN]:
        playery += 5
    
    # Boundary checks
    if playerx > 750:
        playerx = 750
    if playerx < 0:
        playerx = 0
    if playery > 550:
        playery = 550
    if playery < 400:
        playery = 400
    # Draw background
    screen.blit(background, (0, 0))
    text2 = font2.render("points: " + str(player1_points),True,white)
    text2_rect = text2.get_rect(center=(70,30))

    
    screen.blit(text2, text2_rect)
    

    # Draw player (needed so it still shows when no keys pressed)
    #screen.blit(playerimage, (playerx, playery))
    for enemy in enemylist:
        if (enemy.x < playerx + 50 and  # enemy's left is left of player's right
            enemy.x + 40 > playerx and  # enemy's right is right of player's left
            enemy.y < playery + 53 and  # enemy's top is above player's bottom
            enemy.y + 29 > playery):    # enemy's bottom is below player's top
            player_alive = False
            
    if player_alive == False:
        screen.blit(text3, text3_rect)
        update_highscore(player1_points,highscore)
    
    if player_alive == True:
        screen.blit(playerimage, (playerx, playery))        
            # Update enemy
    for enemy in enemylist:
        enemy.image_blit(screen)
        enemy.movement()
        
    for bullet in bulletlist:
        bullet.image_blit(screen)
        bullet.movement()
        for enemy in enemylist:
        #add bullet detection here
            if enemy.x <= bullet.x <= enemy.x+hitboxx and enemy.y <= bullet.y <= enemy.y+hitboxy:
                bulletlist.remove(bullet)
                enemy.enemyhealth -= 1
                if enemy.enemyhealth == 0:
                    enemylist.remove(enemy)
                    if boss_spawned == False:
                        explosion_sound.play()
                        player1_points += 1
                
                   
        if bullet.y <0:
             bulletlist.remove(bullet)
    if enemylist == []:
        if boss_spawned == False: 
            enemylist.append(Enemy("images/boss.png",2,2))
            boss_spawned = True
            hitboxx = 70
            hitboxy = 102
        else:
            screen.blit(text1, text1_rect)
            if sound_played == False:
                sound_played = True
                update_highscore(player1_points,highscore)
        
                win_sound.play()
    # update_highscore(player1_points,highscore)
    # if player1_points > highscore:
    #     highscore = player1_points
    #     with open("highscore.txt", "w") as f:
    #         f.write(str(highscore))
         
    pygame.display.flip()
    clock.tick(60)
   