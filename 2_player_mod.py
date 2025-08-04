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
playerhealth2 = 3
enemyimage = "images/enemy_green.png"
with open("highscore.txt", "r") as f:
    highscore = int(f.read())
loadout_inbound_sound = False
loadout_is_collected = False
active = False
hitboxx = 40 
game_status = "ongoing" 
spaceship_img = "images/panda.webp" # player image
spaceship_img2 = "images/spaceship2.png"
loadoutsrn = False # makes it only one loadout on the screen
player1_points = 0 # amount of enemys player1 has destroyed
hitboxy = 30 # hitbox (y) for enemy(s)
green = (0,255,0) # color code for green
white = (255,255,255) # color code for white
red = (255,0,0) # color code for red
x = 400 # width of the frame
y = 700 # height of the frame
last_shot_time = 0 # last
last_shot_time2 = 0
cooldown = 400 # cooldown between bullets
cooldown2 = 1000
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
def player_movement2(x2,y2):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x2 += 5
    if keys[pygame.K_s]:
        y2 += 5
    if keys[pygame.K_w]:
        y2 += -5
    if keys[pygame.K_a]:
        x2 += -5

    if x2 > 350:
        x2 = 350
    if x2 < 0:
        x2 = 0
    if y2 > 650:
        y2 = 650
    if y2 < 100:
        y2 = 100
    return x2,y2
# Function to save highscore

def update_highscore(player1_points):
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
    if player1_points > highscore:
        highscore = player1_points
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))
        username = input("what is your name? ")
        print(username)
# Function to give you rewards after you take loadout
def loadout_rewards(playerstep):       
    spaceship_img = "images/panda.webp"
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
    
# Enemy class, makes it possible to have multiple enemies.
class Enemy():
    def __init__(self,img_path,health,boss):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.x = random.randint(20,380)    
        self.y = random.randint(-2,0)
        self.steps = random.choice([2,2.2,2.3,2.4,2.5])
        self.enemyhealth = health
        health = 3
        self.boss = boss
    # Refreshes enemies image and position every frame    
    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))
    def movement(self):
        
        self.y += self.steps

    # Enemy loses one health every time it gets hit by a bullet
    def detection(self):

        for bullet in bulletlist:
            bullet.image_blit(screen)
            bullet.movement()
            for enemy in enemylist:
                if enemy.x <= bullet.x <= enemy.x+40 and enemy.y <= bullet.y <= enemy.y+30:
                    bulletlist.remove(bullet)
                    enemy.enemyhealth -= 1
                    if enemy.enemyhealth == 0:
                        enemylist.remove(enemy)
                        explosion_sound.play()
        for big_bullet in big_bulletlist:
            big_bullet.image_blit(screen)
            big_bullet.movement()
            for enemy in enemylist:
                if enemy.x-50 <= big_bullet.x <= enemy.x+90 and enemy.y-50 <= big_bullet.y <= enemy.y+80:
                    big_bulletlist.remove(bullet)
                    enemy.enemyhealth -= 5
                    if enemy.enemyhealth == 0:
                        enemylist.remove(enemy)
                        explosion_sound.play()
                
# Makes it possible to have multiple bullets at the same time                       
class Bullet():
    def __init__(self,playerx,playery):
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.speed = 7
        self.x = playerx+playercenter
        self.y = playery

    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))

    def movement(self):
        self.y -= self.speed

class Big_bullet():
    def __init__(self,playerx2,playery2):
        self.image = pygame.image.load("images/big_bullet1.png").convert_alpha()
        self.speed = 5
        self.x = playerx2+10
        self.y = playery2
      

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
font4 = pygame.font.Font('freesansbold.ttf', 20)
playerhealth1 = pygame.font.Font('freesansbold.ttf', 20)
highscore1 = pygame.font.Font('freesansbold.ttf', 20)
waves_passed = pygame.font.Font('freesansbold.ttf', 20)
# Color for input box
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
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
playerimage2 = pygame.image.load(spaceship_img2).convert_alpha()
# Load sounds
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
lose_sound = pygame.mixer.Sound("sounds/lose_sound.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
win_sound = pygame.mixer.Sound("sounds/win_sound.wav")
loadout_collected = pygame.mixer.Sound("sounds/loadout_collect.wav")
loadout_inbound = pygame.mixer.Sound("sounds/loadoutinbound.wav")
# Initial positions
playerx = x // 2
playery = y - (y // 4)
playerx2 = x // 2
playery2 = y - (y // 4)

# Lists
bulletlist = []
enemylist = []
big_bulletlist = []

# Main loop
while True:
    # Cooldown and track if window is closed
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        # print(pygame.event.event_name(event.type))
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if current_time - last_shot_time >= cooldown:

                if event.key == pygame.K_l or event.key == pygame.K_SPACE:
                    bullet = Bullet(playerx, playery)
                    bulletlist.append(bullet)
                    shoot_sound.play()
                    last_shot_time = current_time

        if event.type == pygame.KEYDOWN:
            if current_time - last_shot_time2 >= cooldown2:

                if event.key == pygame.K_e:
                    big_bullet = Big_bullet(playerx2,playery2)
                    big_bulletlist.append(big_bullet)
                    shoot_sound.play()
                    last_shot_time2 = current_time
    # Appends enemys every two seconds
    if current_time - last_spawn_time > spawn_delay:
        for i in range(enemyspawns):
            enemylist.append(Enemy(enemyimage, enemyhealth,False)) 
        last_spawn_time = current_time
        current_wave += 1
    
    playerx,playery = player_movement(playerx,playery,playerstep)
    playerx2,playery2 = player_movement2(playerx2,playery2)


    # Draw background
    scroll_y -= 1
    if scroll_y <= 0:
        scroll_y = bg_height
    screen.blit(background, (0, - scroll_y))
    screen.blit(background,(0,bg_height - scroll_y))
    
    text2 = font2.render("Points: " + str(player1_points),True,white)
    text4 = font4.render("PlayerTwo health: " + str(playerhealth2),True,white)
    playerhealth1_text = playerhealth1.render( "PlayerOne health: "+ str(playerhealth), True,white)
    text2_rect = text2.get_rect(center=(50,30))
    text4_rect = text4.get_rect(center=(300,80))
    playerhealth1_text_rect = playerhealth1_text.get_rect(center=(300,130))
    waves_passed_text = waves_passed.render('Current wave: ' + str(current_wave), True,white) 
    waves_passed_text_rect = waves_passed_text.get_rect(center=(82,130))
    # Blits text
    screen.blit(waves_passed_text, waves_passed_text_rect)
    screen.blit(highscore1, highscore_rect)
    screen.blit(text2, text2_rect)
    screen.blit(playerhealth1_text, playerhealth1_text_rect)
    screen.blit(text4, text4_rect)
    

    
    #screen.blit(playerimage, (playerx, playery))
    for enemy in enemylist:
        if (enemy.x < playerx + 50 and
            enemy.x + 40 > playerx and  
            enemy.y < playery + 53 and  
            enemy.y + 29 > playery):  
            playerhealth -= 1
            enemylist.remove(enemy) 
    for enemy in enemylist:
        if (enemy.x < playerx2 + 50 and
            enemy.x + 40 > playerx2 and  
            enemy.y < playery2 + 53 and  
            enemy.y + 29 > playery2):  
            playerhealth2 -= 1
            enemylist.remove(enemy) 
            
    if playerhealth == 0 or playerhealth2 == 0:
        game_status = "loss"
        update_highscore(player1_points)
        lose_sound.play()
        playerhealth -= 1
        playerhealth2 -= 1

    if game_status == "loss":
        # Shows "WARZONE DEFEAT" text
        screen.blit(text3, text3_rect)
    
    if game_status == "ongoing":
        # Draw player (needed so it still shows when no keys pressed)
        screen.blit(playerimage, (playerx, playery)) 
        screen.blit(playerimage2, (playerx2, playery2))


    if game_status == "win":
        # Refreshes "YOU WIN" text
        screen.blit(text1, text1_rect)

    # Update enemy
    for enemy in enemylist:
        enemy.image_blit(screen)
        enemy.movement()
        if enemy.y > 700:
            enemylist.remove(enemy)           
    # Deletes bullet after it is out of screen   
    for big_bullet in big_bulletlist:
        big_bullet.image_blit(screen)
        big_bullet.movement()
        if big_bullet.y <0:
            big_bulletlist.remove(big_bullet)
            continue
        for enemy in enemylist:
                if enemy.x-100 <= big_bullet.x <= enemy.x+150 and enemy.y <= big_bullet.y <= enemy.y+30:
                    big_bulletlist.remove(big_bullet)
                    enemy.enemyhealth -= 5
                
                    if enemy.enemyhealth <= 0:
                        enemylist.remove(enemy)
                        explosion_sound.play() 
                        player1_points += 1  
                    break 
    for bullet in bulletlist:
        bullet.image_blit(screen)
        bullet.movement()
        if bullet.y <0:
            bulletlist.remove(bullet)
            continue
        for enemy in enemylist:
        # Bullet detection
            if enemy.x <= bullet.x <= enemy.x+hitboxx and enemy.y <= bullet.y <= enemy.y+hitboxy:
                bulletlist.remove(bullet)
                enemy.enemyhealth -= 1
                if enemy.enemyhealth == 0:
                    enemylist.remove(enemy)
                    if enemy.boss == True:
                        # Gives extra points if you kill the boss
                        player1_points += 3
                        update_highscore(player1_points)       
                        win_sound.play()
                        game_status = "win"                        
                    else:
                        explosion_sound.play()
                        player1_points += 1
                        lo_spawn = random.randint(1,15)
                        #makes it a chance for loadout every time you kill an enemy
                        if lo_spawn == 7 and loadoutsrn == False:
                            loadoutsrn = True
                            loadout_inbound.play() 
                            loadout = pygame.image.load("images/loadout.png").convert_alpha()
                break
    # Difficulties depending on the players points
    if 100 > player1_points >= 25:
        enemyspawns = 3
        
    if 150 > player1_points >= 100:
        enemyspawns = 5
        

    if 250 > player1_points > 150:
        spawn_delay = 1750
        enemyspawns = 6
        enemyimage = "images/enemy_red.png"

    if 500 > player1_points > 250:
        spawn_delay = 1500
        enemyspawns = 8
    
    if 750 > player1_points >= 300:
        enemyspawns = 10
        enemyimage = "images/red_final .png"

    if 1000 > player1_points > 500:
        enemyhealth = 3
        spawn_delay = 1000

    if player1_points >= 1000:
        enemyspawns = 15
        spawn_delay = 500


    # Spawns loadout
    if loadoutsrn == True:      
        screen.blit(loadout, (loadoutx, loadouty))
        loadouty += 2
        # Detects if the loadout is out of screen
        if loadouty >= 700:  
            loadoutsrn = False
            loadoutx =random.randint(0,380)
            loadouty = -30
        # Detects if player have touched the loadout
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
                # Gives player more health if loadout collected is more than 5
                if lo_collected >= 5:
                    playerhealth += 1

        if (loadoutx < playerx2 + 50 and 
            loadoutx + 40 > playerx2 and
            loadouty < playery2 + 53 and  
            loadouty + 29 > playery2):
            loadout_collected.play() 
            loadoutsrn = False 
            lo_collected += 1
            playerhealth2 += 1  
            loadoutx =random.randint(0,380)
            loadouty = -30
            if lo_collected >= 1:  
                playerimage,playercenter,cooldown,playerstep = loadout_rewards(playerstep)
                # Gives player more health if loadout collected is more than 5
                if lo_collected >= 5:
                    playerhealth2 += 1

    if player1_points == 10:
        if boss_spawned == False: 
            enemylist.append(Enemy("images/boss.png",5,True))
            boss_spawned = True
            hitboxx = 70
            hitboxy = 102
         
    pygame.display.flip()
    clock.tick(60)
   