import pygame
import random
import sys
import pdb
loadoutx = random.randint(0,800)
playercenter = 24
loadouty = 0
lo_collected = 0
with open("highscore.txt", "r") as f:
        highscore = int(f.read())
loadout_inbound_sound = False
loadout_is_collected = False
hitboxx = 40
player_alive = True
spaceship_img = "images/spaceship.png"
loadoutsrn = False
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
def player_movement(x,y):
    # Handle movement on key press inside event loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 5 
    if keys[pygame.K_RIGHT]:
        x += 5
    if keys[pygame.K_d]:
        x += 5
    if keys[pygame.K_s]:
        y += 5
    if keys[pygame.K_w]:
        y += -5
    if keys[pygame.K_a]:
        x += -5
    if keys[pygame.K_UP]:
        y += -5
    if keys[pygame.K_DOWN]:
        y += 5


    
    # Boundary checks
    if x > 750:
        x = 750
    if x < 0:
        x = 0
    if y > 550:
        y = 550
    if y < 400:
        y = 400
    return x,y

def update_highscore(player1_points):
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
    if player1_points > highscore:
        highscore = player1_points
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))

def loadout_rewards():       
    spaceship_img = "images/spaceship_upg1.png"
    playerimage = pygame.image.load(spaceship_img).convert_alpha()
    playercenter = 48
    cooldown = 325
    if lo_collected >= 2:
        cooldown = 0
    return playerimage,playercenter,cooldown   
    

class Enemy():
    def __init__(self,img_path,steps,health):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.x = random.randint(300,600)    
        self.y = random.randint(30, 100)
        self.steps = steps
        self.enemyhealth = health
        steps = random.choice([-4,-3,-2,-1,1,2,3,4,])
        health = 3
        
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
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.x = playerx+playercenter
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
highscore1 = pygame.font.Font('freesansbold.ttf', 30)
text1= font1.render('YOU WIN', True,green)
text3= font3.render('WARZONE DEFEAT', True,red)
highscore1 = highscore1.render('highscore: ' + str(highscore), True,white)

text1_rect = text1.get_rect(center=(x // 2, y // 2))
text3_rect = text3.get_rect(center=(x // 2, y // 2))
highscore_rect = highscore1.get_rect(center=(700,30))



# Load images

background = pygame.image.load("images/backround.jpg").convert_alpha()
playerimage = pygame.image.load(spaceship_img).convert_alpha()
# Load sounds
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
win_sound = pygame.mixer.Sound("sounds/win_sound.wav")
loadout_collected = pygame.mixer.Sound("sounds/loadout_collect.wav")
loadout_inbound = pygame.mixer.Sound("sounds/loadoutinbound.wav")
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
    
    playerx,playery = player_movement(playerx,playery)

    # Draw background
    screen.blit(background, (0, 0))
    text2 = font2.render("points: " + str(player1_points),True,white)
    text2_rect = text2.get_rect(center=(70,30))

    screen.blit(highscore1, highscore_rect)
    screen.blit(text2, text2_rect)

    # Draw player (needed so it still shows when no keys pressed)
    #screen.blit(playerimage, (playerx, playery))
    for enemy in enemylist:
        if (enemy.x < playerx + 50 and
            enemy.x + 40 > playerx and  
            enemy.y < playery + 53 and  
            enemy.y + 29 > playery):    
            player_alive = False
            
    if player_alive == False:
        screen.blit(text3, text3_rect)
        update_highscore(player1_points)
    
    if player_alive == True:
        screen.blit(playerimage, (playerx, playery))        
            # Update enemy
    for enemy in enemylist:
        enemy.image_blit(screen)
        enemy.movement()
        
    for bullet in bulletlist:
        bullet.image_blit(screen)
        bullet.movement()
        if bullet.y <0:
            bulletlist.remove(bullet)
            continue
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
                        lo_spawn = random.choice([7])
                        #makes it 10 percent chance for loadout every time you kill an enemy
                        if lo_spawn == 7 and loadoutsrn == False:
                            loadoutsrn = True
                            loadout_inbound.play() 
                            loadout = pygame.image.load("images/loadout.png").convert_alpha()
                break
   
    if loadoutsrn == True:      
        screen.blit(loadout, (loadoutx, loadouty))
        loadouty += 1 

                
        if loadouty >= 600:  
            loadoutsrn = False
            loadoutx =random.randint(0,800)
            loadouty = 0 
        
        if (loadoutx < playerx + 50 and 
            loadoutx + 40 > playerx and
            loadouty < playery + 53 and  
            loadouty + 29 > playery):
            loadout_collected.play() 
            loadoutsrn = False 
            lo_collected += 1  
            loadoutx =random.randint(0,800)
            loadouty = 0 
            if lo_collected >= 1:           
                playerimage,playercenter,cooldown = loadout_rewards()
       
    if enemylist == []:
        if boss_spawned == False: 
            enemylist.append(Enemy("images/boss.png",15,10))
            boss_spawned = True
            hitboxx = 70
            hitboxy = 102
        else:
            screen.blit(text1, text1_rect)
            if sound_played == False:
                sound_played = True
                update_highscore(player1_points)       
                win_sound.play()
         
    pygame.display.flip()
    clock.tick(60)
   