import pygame
import random
import sys
import pdb
from library import Enemy_bullet, Enemy, Bullet

loadoutx = random.randint(0,380)
loadouty = -30
playercenter = 24
lo_collected = 0
playerstep = 5
enemyspawns = 2
enemyhealth = 2
playerhealth = 5
current_wave = 1
big_bullet_speed = 2
final_boss_spawned = False
final_boss_killed = False
zigzag_enemy = False
playerhealth2 = 5
bosses_killed = 0
bullet_damage = 1
enemyimage = "images/enemy_green.png"
with open("highscore.txt", "r") as f:
    highscore = int(f.read())
loadout_inbound_sound = False
active = False
hitboxx = 40 
game_status = "ongoing" 
spaceship_img = "images/spaceship.png" # player image
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
cooldown2 = 1500
boss_spawned = False # spawns boss once
sound_played = False # plays sound once
spawn_delay = 2000  # time in milliseconds between spawns
last_spawn_time = pygame.time.get_ticks()  # current time

def player_movement(x,y,playerstep):
    # Handle movement on key press inside event loop
    
    if keys[pygame.K_LEFT]:
        x -= playerstep 
    if keys[pygame.K_RIGHT]:
        x += playerstep
    if keys[pygame.K_UP]:
        y += -playerstep
    if keys[pygame.K_DOWN]:
        y += playerstep

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



class Loadout():
    def __init__(self,img_path = "images/loadout.png",gone = False,health = False,rapid_fire = False,launcher = False):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.speed = 2
        self.x = random.randint(0,360)
        self.y = -30
        self.collected_amount = 0
        self.health = health
        self.collected = False
        self.gone = gone
        self.rapid_fire = rapid_fire
        self.launcher = launcher
  


    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))

    def detection(self,playerx,playery,playerhealth,playerhealth2,playerx2,playery2):
        
        if (self.x < playerx + 50 and 
            self.x + 40 > playerx and
            self.y < playery + 53 and  
            self.y + 29 > playery):
             
            playerhealth += 1  
            self.x =random.randint(0,360)
            self.y = -30 
            self.gone = True
            self.collected = True
            if self.health == True:
                playerhealth += 2
                health_lo_collected.play()
            elif not self.health:
                self.collected_amount += 1
                if self.rapid_fire:
                    rapid_fire_collected.play()
                elif self.launcher:
                    pass
                    
                else:
                    loadout_collected.play()

        if (self.x < playerx2 + 50 and 
            self.x + 40 > playerx2 and
            self.y < playery2 + 53 and  
            self.y + 29 > playery2): 
            playerhealth2 += 1  
            self.x =random.randint(0,360)
            self.y = -30
            self.gone = True
            self.collected = True
            if self.health == True:
                playerhealth2 += 2
                health_lo_collected.play()
            elif not self.health:
                loadout_collected.play()
                self.collected_amount += 1
            if self.rapid_fire:
                rapid_fire_collected.play()
            elif self.launcher:
                rapid_fire_collected.play()
                    
            else:
                loadout_collected.play()



 
            self.gone = True
            if self.collected_amount >= 5:
                playerhealth2 += 2
        return playerhealth,playerhealth2
    
    def loadout_rewards(self,big_bullet_speed,playerstep,cooldown,cooldown2):
        
        spaceship_img = "images/spaceship_upg1.png"
        playerimage = pygame.image.load(spaceship_img).convert_alpha()
        playercenter = 48
        cooldown = 325
        big_bullet_speed = 5
        if self.collected_amount >= 2:
            cooldown = 200
            big_bullet_speed = 6
        if lo_collected == 3:
            playerstep = 7
            cooldown = 200

        if 5 > self.collected_amount >= 4:
            playerstep = 9
            cooldown = 0
    
        if self.collected_amount >= 5:
            playerstep = 10
            cooldown = 0
        
        if self.rapid_fire == True:
            
            cooldown2 -= 200
            if cooldown < 0:
                cooldown = 0
            if cooldown2 < 100: 
                cooldown2 = 100
            
            
            
    

        return playerimage,playercenter,cooldown,playerstep,big_bullet_speed,cooldown2
    def movement(self):
        self.y += self.speed
        if self.y > 700:
            self.gone = True
            

        

            
    
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
health_lo_collected = pygame.mixer.Sound("sounds/healing_lo.wav")
rapid_fire_collected = pygame.mixer.Sound("sounds/fire_mods.wav")
fire_mod_change = pygame.mixer.Sound("sounds/fire_mod_change.wav")
launcher = pygame.mixer.Sound("sounds/launcher.wav")
# Initial positions
playerx = x // 2
playery = y - (y // 4)
playerx2 = x // 2
playery2 = y - (y // 4)
# Lists
bulletlist = []
enemylist = []
big_bulletlist = []
enemy_bullets = []
loadout_list = []
fire_mods = ["single_fire"]
mod = 0
current_fire_mod = fire_mods[mod]
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
                if current_fire_mod == "single_fire":
                    bullet_damage = 1
                    cooldown = 400
                    if event.key == pygame.K_l or event.key == pygame.K_SPACE:
                    
                        bullet = Bullet(playerx, playery,playercenter)
                        bulletlist.append(bullet)
                        shoot_sound.play()
                        last_shot_time = current_time
        if event.type == pygame.KEYDOWN:
            if current_time - last_shot_time >= cooldown:
                if current_fire_mod == "launcher":
                    bullet_damage = 2
                    cooldown = 700
                    if event.key == pygame.K_l or event.key == pygame.K_SPACE:
                    
                        bullet = Bullet(playerx, playery,playercenter,"images/launcher_bullet.png")
                        bulletlist.append(bullet)
                        launcher.play()
                        last_shot_time = current_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if current_fire_mod == "rapid_fire":
                bullet_damage = 1
                cooldown = 200
                if current_time - last_shot_time >= cooldown:
                    shoot_sound.play()
                    bullet = Bullet(playerx, playery,playercenter)
                    bulletlist.append(bullet)
                    last_shot_time = current_time


        
        if event.type == pygame.KEYDOWN:
            if current_time - last_shot_time2 >= cooldown2:
                if event.key == pygame.K_e:
                    
                    bulletlist.append(Bullet(playerx2,playery2,10, "images/missile.png",big_bullet_speed))
                    shoot_sound.play()
                    last_shot_time2 = current_time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                fire_mod_change.play()
                mod += 1
               
                if mod >= len(fire_mods):
                    mod = 0
                current_fire_mod = fire_mods[mod]
                print(current_fire_mod)

        
    # Appends enemys every two seconds
    if current_time - last_spawn_time > spawn_delay:
        for i in range(enemyspawns):
            enemy = (Enemy(enemyimage, enemyhealth,False,random.choice([2,2.2,2.3,2.4,2.5]),False,False)) 
            enemyx = enemy.x
            enemyy = enemy.y
            enemylist.append(enemy)
        last_spawn_time = current_time
        current_wave += 1
        if current_wave % 10 == 0:
            enemylist.append(Enemy("images/tmp.png", 5,True,0.5,False,False))
        if current_wave % 7 == 0 and zigzag_enemy == False:
            enemylist.append(Enemy("images/enemy_blue.png", 10,False,2,False,True))
            zigzag_enemy = True

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
            if enemy.finalboss == False:
                enemylist.remove(enemy)
            if enemy.zigzag:
                playerhealth -= 2
            if enemy.bulletenemy:
                playerhealth -= 1
           
    for enemy in enemylist:
        if (enemy.x < playerx2 + 50 and
            enemy.x + 40 > playerx2 and  
            enemy.y < playery2 + 53 and  
            enemy.y + 29 > playery2):  
            playerhealth2 -= 1
            if enemy.finalboss == False:
                enemylist.remove(enemy)
            if enemy.zigzag:
                playerhealth -= 2
            if enemy.bulletenemy:
                playerhealth -= 1
            
            
    if playerhealth == 0 or playerhealth2 == 0 and not game_status == "loss":
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
        if enemy.zigzag == False:
            enemy.movement()
        if enemy.zigzag == True:
            zigzagx,zigzagy = enemy.zigzag_movement()   
        if enemy.y > 700:
            enemylist.remove(enemy)  
        if enemy.bulletenemy :
            if enemy.bulletenemy and enemy.y > 0:
                bullet_chance = random.randint(1,100)
                if bullet_chance == 2: 
                    bullet = Enemy_bullet(enemy.x + 15, enemy.y + 15)
                    enemy_bullets.append(bullet)
        
    for enemy_bullet in enemy_bullets:
        enemy_bullet.movement()
        enemy_bullet.image_blit(screen)
        if enemy_bullet.y > 700:
            enemy_bullets.remove(enemy_bullet)
    
    for enemy_bullet in enemy_bullets:
        if playerx <= enemy_bullet.x <= playerx+50 and playery <= enemy_bullet.y <= playery+50:
            playerhealth -= 1
            enemy_bullets.remove(enemy_bullet)

    for enemy_bullet in enemy_bullets:
        if playerx2 <= enemy_bullet.x <= playerx2+50 and playery2 <= enemy_bullet.y <= playery2+50:
            playerhealth2 -= 1
            enemy_bullets.remove(enemy_bullet)
    # Deletes bullet after it is out of screen     
    for bullet in bulletlist:
        bullet.image_blit(screen)
        bullet.movement()
        if bullet.y <0:
            bulletlist.remove(bullet)
            continue
        for enemy in enemylist:
            if enemy.finalboss == False:
                hitboxx = 40
                hitboxy = 40
            else:
                hitboxx = 200
                hitboxy =432
            if enemy.x <= bullet.x <= enemy.x+hitboxx and enemy.y <= bullet.y <= enemy.y+hitboxy:
                bulletlist.remove(bullet)
                enemy.enemyhealth -= bullet_damage
                if enemy.enemyhealth <= 0:
                    enemylist.remove(enemy)                    
                    if enemy.finalboss == True:
                        game_status = "win"
                        player1_points += 100
                        update_highscore(player1_points)
                        win_sound.play() 
                        final_boss_killed = True 
                        hitboxx = 200
                        hitboxy = 432   
                    if enemy.zigzag == True:
                        zigzag_enemy = False                 
                    else:
                        explosion_sound.play()
                        player1_points += 1
                        lo_spawn = random.choice([7,5,10,12])
                        #makes it a chance for loadout every time you kill an enemy
                        if lo_spawn == 7 and len(loadout_list) == 0:
                            loadout = Loadout("images/loadout.png")
                            loadout_list.append(loadout)
                            loadout_inbound.play()
                                    
                            lo_spawn = 8
                        if lo_spawn == 10 and len(loadout_list) == 0:
                            loadout_list.append(Loadout("images/loadout_heart.png",False,True))
                            loadout_inbound.play()
                        if lo_spawn == 5 and not loadout_list:
                            loadout_list.append(Loadout("images/fire_mods.png",False,False,True))
                            loadout_inbound.play()
                            
                        if lo_spawn == 12 and not loadout_list:
                            loadout_list.append(Loadout("images/launcher.png",False,False,False,True))
                            loadout_inbound.play()
                           
                            
                break
    for big_bullet in big_bulletlist:
        big_bullet.image_blit(screen)
        big_bullet.movement()
        if big_bullet.y <0:
            big_bulletlist.remove(big_bullet)
            continue
        for enemy in enemylist:
            if enemy.finalboss == False:
                hitboxx = 50
                hitboxy = 40
            else:
                hitboxx = 200
                hitboxy =370   
        # Bullet detection
            if enemy.x <= big_bullet.x <= enemy.x+hitboxx and enemy.y <= big_bullet.y <= enemy.y+hitboxy:
                big_bulletlist.remove(big_bullet)
                enemy.enemyhealth -= 5
                if enemy.enemyhealth <= 0:
                    enemylist.remove(enemy)         
                    if enemy.finalboss == True:
                        game_status = "win"
                        player1_points += 100
                        update_highscore(player1_points)
                        win_sound.play() 
                        final_boss_killed = True 
                        hitboxx = 200
                        hitboxy = 432 
                    if enemy.zigzag == True and not enemy.baby:
                        zigzag_enemy = False
                        for i in range(random.randint(2,4)):
                            enemylist.append(Enemy("images/enemy_blue_baby.png", 3,False,4,False,True,True)) 
                            for enemy in enemylist:
                                if enemy.baby == True:
                                    enemy.x = random.randint(zigzagx,zigzagx + 120)
                                    enemy.y = zigzagy 
                                    hitboxx = 20
                                    hitboxy = 15 
                                     
                    else:
                        explosion_sound.play()
                        player1_points += 1
                        lo_spawn = random.choice([5])
                        #makes it a chance for loadout every time you kill an enemy
                        if lo_spawn == 7 and len(loadout_list) == 0:
                            loadout = Loadout("images/loadout.png")
                            loadout_list.append(loadout)
                            loadout_inbound.play()
                                    
                            lo_spawn = 8
                        if lo_spawn == 10 and len(loadout_list) == 0:
                            loadout_list.append(Loadout("images/loadout_heart.png",False,True))
                            loadout_inbound.play()
                        if lo_spawn == 5 and not loadout_list:
                            loadout_list.append(Loadout("images/fire_mods.png",False,False,True))
                            loadout_inbound.play()
                        if lo_spawn == 12 and not loadout_list:
                            loadout_list.append(Loadout("images/launcher.png",False,False,False,True))
                            loadout_inbound.play()
                            
                break
  
    if player1_points > 1000 and not final_boss_spawned:
        enemylist.append(Enemy("images/Final_boss.png",300,False,0.2,True,False))
        hitboxx = 90
        hitboxy = 200
        for enemy in enemylist:
            if enemy.finalboss == True:
                enemy.x = 150
                enemy.y = -200
                hitboxx = 90
                hitboxy = 200
                current_wave += 1
                final_boss_spawned = True
            elif enemy.finalboss == False:
                hitboxx = 50
                hitboxy = 40
 
    if final_boss_killed == True:
        game_status = "win"        
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

    for loadouts in loadout_list:
        
        loadouts.image_blit(screen)
        playerhealth,playerhealth2 = loadouts.detection(playerx,playery,playerhealth,playerhealth2,playerx2,playery2)
        loadoutsrn = loadouts.movement()
        if loadouts.gone == True:
            loadout_list.remove(loadouts)
            if loadouts.collected:
                if loadouts.collected_amount >= 1:
                    playerimage,playercenter,cooldown,playerstep,big_bullet_speed,cooldown2 = loadouts.loadout_rewards(big_bullet_speed,playerstep,cooldown,cooldown2)
                if loadouts.rapid_fire:
                    if not "rapid_fire" in fire_mods:
                        fire_mods.append("rapid_fire")
                if loadouts.launcher:
                    if not "launcher" in fire_mods:
                        fire_mods.append("launcher")         


    pygame.display.flip()
    clock.tick(60)  