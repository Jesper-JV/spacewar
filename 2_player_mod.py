import pygame
import random
import sys
import pdb
from library import Enemy_bullet, Enemy, Bullet, Loadout
import json

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
# Lists
bulletlist = []
enemylist = []
enemy_bullets = []
loadout_list = []
fire_mods = ["single_fire"]
mod = 0
current_fire_mod = fire_mods[mod]

def player_movement(x,y,playerstep):
    # Handle movement on key press inside event loop
    keys = pygame.key.get_pressed()
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
    
        
       

    if player1_points > dictionary_highscore["highscore"]:
        username = input("what is your name? ")
        print(username)  
        dictionary_highscore["username"] = username
        dictionary_highscore["highscore"] = player1_points
        with open("highscore.txt", "w") as f:
            json.dump(dictionary_highscore,f)
        
def enemy_difficulty(player1_points,enemyspawns,enemyimage,spawn_delay,enemyhealth):

            
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
    return enemyspawns,spawn_delay,enemyimage,enemyhealth 

def finalboss_spawn(hitboxx,hitboxy,final_boss_spawned):
    if player1_points == 100 and not final_boss_spawned:
        enemylist.append(Enemy("images/Final_boss.png",300,False,1,True,False))
        final_boss_spawned = True        
        for enemy in enemylist:
            if enemy.finalboss == True:
                hitboxx = 90
                hitboxy = 200
            elif enemy.finalboss == False:
                hitboxx = 50
                hitboxy = 40
    return hitboxx,hitboxy   

def shoot_bullets(last_shot_time,cooldown,current_time,current_fire_mod,shoot_sound,playercenter,playerx,playery,launcher,playerx2,playery2,big_bullet_speed,last_shot_time2,cooldown2,bullet_damage):
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
                
                bulletlist.append(Bullet(playerx2,playery2,10, "images/missile.png",big_bullet_speed,True))
                shoot_sound.play()
                last_shot_time2 = current_time
    return bullet_damage,current_fire_mod,cooldown,cooldown2,playerx,playerx2,playery,playery2,bulletlist,current_time,last_shot_time,last_shot_time2

class Buttons():
    def __init__(self,replay,x,y):
        self.image = pygame.image.load(replay).convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def screenblit(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    def detection(self,game_status, current_wave, player1_points, playerx,playerx2,playery,playery2,lo_collected,current_fire_mod,playerhealth,playerhealth2,spaceship_img,playerimage):
        pos = pygame.mouse.get_pos()
        print(pos)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                game_status = "ongoing"
                current_wave = 0
                player1_points = 0 
                playerx = x // 2
                playery = y - (y // 4)
                playerx2 = x // 2
                playery2 = y - (y // 4)
                lo_collected = 0
                playerhealth2 = 5
                playerhealth = 5
                spaceship_img = "images/spaceship.png"
                if "rapid_fire" in fire_mods:
                    fire_mods.remove("rapid_fire")
                if "launcher" in fire_mods:
                    fire_mods.remove("launcher")
                current_fire_mod = "single_fire"
                for enemy in enemylist:
                    enemylist.remove(enemy)
                playerimage = pygame.image.load(spaceship_img).convert_alpha()
        return game_status, current_wave, player1_points, playerx,playerx2,playery,playery2,lo_collected,current_fire_mod,playerhealth,playerhealth2,spaceship_img,enemylist,playerimage







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
dictionary_highscore = {"username":"none","highscore":0}
with open("highscore.txt", "r") as f:
    dictionary_highscore = json.load(f)
print(type(dictionary_highscore["highscore"]))

highscore1 = highscore1.render(dictionary_highscore["username"] + " : " + str(dictionary_highscore["highscore"]), True,white)

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


# Main loop
while True:
    # Cooldown and track if window is closed
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        # print(pygame.event.event_name(event.type))
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        bullet_damage,current_fire_mod,cooldown,cooldown2,playerx,playerx2,playery,playery2,bulletlist,current_time,last_shot_time,last_shot_time2 = shoot_bullets(last_shot_time,
        cooldown,current_time,current_fire_mod,shoot_sound,playercenter,playerx,playery,launcher,playerx2,playery2,big_bullet_speed,last_shot_time2,cooldown2,bullet_damage)
        
        
    
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
        replay = Buttons("images/try_again.png",x // 2 -150, 500)   
        replay.screenblit(screen)
        game_status,current_wave,player1_points,playerx,playerx2,playery,playery2,lo_collected,current_fire_mod,playerhealth,playerhealth2,spaceship_img,enemylist,playerimage = replay.detection(game_status, current_wave, player1_points
        , playerx,playerx2,playery,playery2,lo_collected,current_fire_mod,playerhealth,playerhealth2,spaceship_img,playerimage)
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
                if bullet.big_bullet == True:
                    enemy.enemyhealth -= 5
                else:
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
    
    hitboxx,hitboxy = finalboss_spawn(hitboxx,hitboxy,final_boss_spawned)
 
    if final_boss_killed == True:
        game_status = "win"
    enemyspawns,spawn_delay,enemyimage,enemyhealth = enemy_difficulty(player1_points,enemyspawns,enemyimage,spawn_delay,enemyhealth)

    for loadouts in loadout_list:    
        loadouts.image_blit(screen)
        playerhealth,playerhealth2,lo_collected = loadouts.detection(playerx,playery,playerhealth,playerhealth2,playerx2,playery2,health_lo_collected,rapid_fire_collected,loadout_collected,lo_collected)
        loadoutsrn = loadouts.movement()
        if loadouts.gone == True:
            loadout_list.remove(loadouts)
            if loadouts.collected:
                if lo_collected >= 1:
                    playerimage,playercenter,cooldown,playerstep,big_bullet_speed,cooldown2 = loadouts.loadout_rewards(big_bullet_speed,playerstep,cooldown,cooldown2,lo_collected)
                if loadouts.rapid_fire:
                    if not "rapid_fire" in fire_mods:
                        fire_mods.append("rapid_fire")
                if loadouts.launcher:
                    if not "launcher" in fire_mods:
                        fire_mods.append("launcher")         


    pygame.display.flip()
    clock.tick(60)  