import pygame
import random
import sys
import pdb
loadoutx = random.randint(0,380)
loadouty = -30
playercenter = 24
lo_collected = 0
playerstep = 5
enemyspawns = 2
enemyhealth = 2
playerhealth = 3
current_wave = 1
enemyimage = "images/enemy_green.png"
with open("highscore.txt", "r") as f:
    highscore = int(f.read())
loadout_inbound_sound = False
loadout_is_collected = False
hitboxx = 40 
game_status = "ongoing" 
spaceship_img = "images/spaceship.png" # player image
loadoutsrn = False # makes it only one loadout on the screen
player1_points = 0 # amount of enemys player1 has destroyed
hitboxy = 30 # hitbox (y) for enemy(s)
green = (0,255,0) # color code for green
white = (255,255,255) # color code for white
red = (255,0,0) # color code for red
x = 400 # width of the frame
y = 700 # height of the frame
last_shot_time = 0 # last time you shoot a bullet
cooldown = 400 # cooldown between bullets
boss_spawned = False # spawns boss once
sound_played = False # plays sound once
spawn_delay = 2000  # time in milliseconds between spawns
last_spawn_time = pygame.time.get_ticks()  # current time

def player_movement(x,y,playerstep):
    # Handle movement on key press inside event loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= playerstep 
    if keys[pygame.K_RIGHT]:
        x += playerstep
    if keys[pygame.K_d]:
        x += playerstep
    if keys[pygame.K_s]:
        y += 5
    if keys[pygame.K_w]:
        y += -5
    if keys[pygame.K_a]:
        x += -playerstep
    if keys[pygame.K_UP]:
        y += -5
    if keys[pygame.K_DOWN]:
        y += 5

    # Boundary checks
    if x > 350:
        x = 350
    if x < 0:
        x = 0
    if y > 650:
        y = 650
    if y < 100:
        y = 100
    return x,y

def update_highscore(player1_points):
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
    if player1_points > highscore:
        highscore = player1_points
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))

def loadout_rewards(playerstep):       
    spaceship_img = "images/spaceship_upg1.png"
    playerimage = pygame.image.load(spaceship_img).convert_alpha()
    playercenter = 48
    cooldown = 325
    if lo_collected >= 2:
        cooldown = 200
    if lo_collected == 3:
        playerstep = 7
        cooldown = 200
    if 5 > lo_collected >= 4:
        playerstep = 9
        cooldown = 0
    if lo_collected >= 5:
        playerstep = 10
        cooldown = 0
    return playerimage,playercenter,cooldown,playerstep  
    

class Enemy():
    def __init__(self,img_path,health,boss):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.x = random.randint(20,380)    
        self.y = random.randint(-2,0)
        self.steps = random.choice([2,2.2,2.3,2.4,2.5])
        self.enemyhealth = health
        health = 3
        self.boss = boss
        
    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))
    def movement(self):
        
        self.y += self.steps


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
# Create frame
screen = pygame.display.set_mode((x, y))
# Set caption
pygame.display.set_caption("SPACEWAR VER 1.0.0")
# Detect time
clock = pygame.time.Clock()
# Load text
font1 = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 20)
font3 = pygame.font.Font('freesansbold.ttf', 40)
playerhealth1 = pygame.font.Font('freesansbold.ttf', 20)
highscore1 = pygame.font.Font('freesansbold.ttf', 20)
waves_passed = pygame.font.Font('freesansbold.ttf', 20)
# Text and color for text
text1= font1.render('YOU WIN', True,green)
text3= font3.render('WARZONE DEFEAT', True,red)

highscore1 = highscore1.render('Highscore: ' + str(highscore), True,white)


# Set center for text
text1_rect = text1.get_rect(center=(x // 2, y // 2))
text3_rect = text3.get_rect(center=(x // 2, y // 2))
highscore_rect = highscore1.get_rect(center=(310,30))

# Load images

background = pygame.image.load("images/bg.jpg").convert()
bg_height = background.get_height()
scroll_y = 0
playerimage = pygame.image.load(spaceship_img).convert_alpha()

# Load sounds
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
win_sound = pygame.mixer.Sound("sounds/win_sound.wav")
loadout_collected = pygame.mixer.Sound("sounds/loadout_collect.wav")
loadout_inbound = pygame.mixer.Sound("sounds/loadoutinbound.wav")
# Initial positions
playerx = x // 2
playery = y - (y // 4)
bulletlist = []
enemylist = []

for i in range(2):
    enemylist.append(Enemy("images/enemy_green.png",2,False))

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

    if current_time - last_spawn_time > spawn_delay:
        for i in range(enemyspawns):
            enemylist.append(Enemy(enemyimage, enemyhealth,False))
        last_spawn_time = current_time
        current_wave += 1
    
    playerx,playery = player_movement(playerx,playery,playerstep)

    # Draw background
    scroll_y -= 1
    if scroll_y <= 0:
        scroll_y = bg_height
    screen.blit(background, (0, - scroll_y))
    screen.blit(background,(0,bg_height - scroll_y))
    
    text2 = font2.render("Points: " + str(player1_points),True,white)
    playerhealth1_text = playerhealth1.render( "Health: "+ str(playerhealth), True,white)
    text2_rect = text2.get_rect(center=(50,30))
    playerhealth1_text_rect = playerhealth1_text.get_rect(center=(50,80))
    waves_passed_text = waves_passed.render('Current wave: ' + str(current_wave), True,white)
      
    waves_passed_text_rect = waves_passed_text.get_rect(center=(82,130))

    screen.blit(waves_passed_text, waves_passed_text_rect)
    screen.blit(highscore1, highscore_rect)
    screen.blit(text2, text2_rect)
    screen.blit(playerhealth1_text, playerhealth1_text_rect)
    

    # Draw player (needed so it still shows when no keys pressed)
    #screen.blit(playerimage, (playerx, playery))
    for enemy in enemylist:
        if (enemy.x < playerx + 50 and
            enemy.x + 40 > playerx and  
            enemy.y < playery + 53 and  
            enemy.y + 29 > playery):  
            playerhealth -= 1
            enemylist.remove(enemy)  
            
    if playerhealth == 0:
        game_status = "loss"
        update_highscore(player1_points)

    if game_status == "loss":
        screen.blit(text3, text3_rect)
    
    if game_status == "ongoing":
        screen.blit(playerimage, (playerx, playery))        

    if game_status == "win":
        screen.blit(text1, text1_rect)
    # Update enemy
    for enemy in enemylist:
        enemy.image_blit(screen)
        enemy.movement()
        if enemy.y > 700:
            enemylist.remove(enemy)
            
        
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
                    if enemy.boss == True:
                        player1_points += 3
                        update_highscore(player1_points)       
                        win_sound.play()
                        game_status = "win"                        
                    else:
                        explosion_sound.play()
                        player1_points += 1
                        lo_spawn = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
                        #makes it 10 percent chance for loadout every time you kill an enemy
                        if lo_spawn == 7 and loadoutsrn == False:
                            loadoutsrn = True
                            loadout_inbound.play() 
                            loadout = pygame.image.load("images/loadout.png").convert_alpha()
                break

    if 100 > player1_points >= 25:
        enemyspawns = 3
        

    if 150 > player1_points >= 100:
        enemyspawns = 5
        enemyimage = "images/enemy_red.png"

    if 250 > player1_points > 150:
        spawn_delay = 1500
        enemyspawns = 8

    if 500 > player1_points > 250:
        spawn_delay = 1000
    
    if 750 > player1_points >= 300:
        enemyspawns = 10
        enemyimage = "images/red_final .png"

    if player1_points > 500:
        enemyhealth = 3
        spawn_delay = 500

    if loadoutsrn == True:      
        screen.blit(loadout, (loadoutx, loadouty))
        loadouty += 2
        if loadouty >= 700:  
            loadoutsrn = False
            loadoutx =random.randint(0,380)
            loadouty = -30
        
        if (loadoutx < playerx + 50 and 
            loadoutx + 40 > playerx and
            loadouty < playery + 53 and  
            loadouty + 29 > playery):
            loadout_collected.play() 
            loadoutsrn = False 
            lo_collected += 1
            playerhealth += 1  
            loadoutx =random.randint(0,380)
            loadouty = -30
            if lo_collected >= 1:  
                playerimage,playercenter,cooldown,playerstep = loadout_rewards(playerstep)
       
    if player1_points >= 10:
        if boss_spawned == False: 
            enemylist.append(Enemy("images/boss.png",5,True))
            boss_spawned = True
            hitboxx = 70
            hitboxy = 102

             
    pygame.display.flip()
    clock.tick(60)
   