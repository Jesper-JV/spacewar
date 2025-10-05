import pygame
import random
import sys
import pdb
from library import Enemy_bullet, Enemy, Loadout, Buttons, Text, Shop_items
from library import player_movement2, player_movement, update_highscore, save_coins, enemy_difficulty, finalboss_spawn, shoot_bullets, fire_mod_change, shop_item_blit
import json
pygame.init()
loadoutx = random.randint(0,380)
loadouty = -30
playercenter = 24
lo_collected = 0
coins = 0
playerstep = 5
enemyspawns = 2
enemyhealth = 2
playerhealth = 5
current_wave = 0
shop_page = 1
equipped_ship = 0
final_boss_spawned = False
final_boss_killed = False
icon = pygame.image.load("images/icon.png")
zigzag_enemy = False
playerhealth2 = 5
bullet_damage = 1
enemyimage = "images/enemy_green.png"
loadout_inbound_sound = False
hitboxx = 40 
game_status = "menu" 
spaceship_img = "images/spaceship.png" # player image
spaceship_img2 = "images/spaceship2.png"
loadoutsrn = False # makes it only one loadout on the screen
player1_points = 0 # amount of enemys player1 has destroyed
hitboxy = 30 # hitbox (y) for enemy(s)
green = (0,255,0) # color code for green
white = (255,255,255) # color code for white
red = (255,0,0) # color code for red
yellow = (255,215,0)
x = 400 # width of the frame
y = 700 # height of the frame
last_shot_time = 0 
last_shot_time2 = 0
cooldown = 400 # cooldown between bullets
cooldown2 = 1500
sound_played = False # plays sound once
spawn_delay = 2000  # time in milliseconds between spawns
last_spawn_time = pygame.time.get_ticks()  # current time
last_change_time = pygame.time.get_ticks()
page_cooldown = 400
# Lists
bulletlist = []
enemylist = []
enemy_bullets = []
loadout_list = []
spaceships = ["images/spaceship.png"]
fire_mods = ["single_fire"]
spaceship_img = spaceships[equipped_ship]
mod = 0
current_fire_mod = fire_mods[mod]
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
pygame.display.set_icon(icon)
# Color for input box
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
# Text and color for text
text1= font1.render('YOU WIN', True,green)
text3= font3.render('WARZONE DEFEAT', True,red)
dictionary_highscore = {"username":"none","highscore":0,"coins":0}
with open("highscore.txt", "r") as f:
    dictionary_highscore = json.load(f)
highscore1 = highscore1.render(dictionary_highscore["username"] + " : " + str(dictionary_highscore["highscore"]), True,white)

# Set center for text
text1_rect = text1.get_rect(center=(x // 2, y // 2))
text3_rect = text3.get_rect(center=(x // 2, y // 2))
highscore_rect = highscore1.get_rect(center=(310,30))
# Load images
space = Text(100,"SPACE",green,200,100,'comicsansms')
war = Text(65,"WAR",green,200,180,'comicsansms')
total_coins = Text(30,"Coins: "+str(dictionary_highscore["coins"]),yellow,340,30)
background = pygame.image.load("images/bg.jpg").convert()
bg_height = background.get_height()
scroll_y = 0
playerimage = pygame.image.load(spaceship_img).convert_alpha()
playerimage2 = pygame.image.load(spaceship_img2).convert_alpha()
shop = pygame.image.load("images/shop.jpg").convert_alpha()
# Load sounds
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
lose_sound = pygame.mixer.Sound("sounds/lose_sound.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
win_sound = pygame.mixer.Sound("sounds/win_sound.wav")
loadout_collected = pygame.mixer.Sound("sounds/loadout_collect.wav")
loadout_inbound = pygame.mixer.Sound("sounds/loadoutinbound.wav")
health_lo_collected = pygame.mixer.Sound("sounds/healing_lo.wav")
rapid_fire_collected = pygame.mixer.Sound("sounds/fire_mods.wav")
launcher = pygame.mixer.Sound("sounds/launcher.wav")
pygame.mixer.music.load("sounds/menu_sound.mp3")
pygame.mixer.music.set_volume(0.4)
# Append objects
start_game = Buttons("images/play.png",x // 2 -100, 300)
enter_shop = Buttons("images/shop.png",200, 300)
customize = Buttons("images/customize.png",100,400)
quit_shop = Buttons("images/quit_button.png",10, 10)
change_page = Buttons("images/change_page.png",180,665)
buy_stuff = Buttons("images/buy.png",113,430)
plane1 = Shop_items("images/panda.webp",200,200)
plane2 = Shop_items("images/panda.webp",170,170)
plane3 = Shop_items("images/spaceship3_display.png",205,350)
plane4 = Shop_items("images/panda.webp",150,150)
# Initial positions
playerx = x // 2
playery = y - (y // 4)
playerx2 = x // 2
playery2 = y - (y // 4)
# Main loop
while True:
    # Cooldown and track if window is closed
    current_time = pygame.time.get_ticks()
    current_time_page = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_status == "ongoing":
            bullet_damage,current_fire_mod,cooldown,cooldown2,playerx,playerx2,playery,playery2,bulletlist,current_time,last_shot_time,last_shot_time2 = shoot_bullets(last_shot_time,cooldown,current_time,current_fire_mod,shoot_sound,playercenter,playerx,playery,launcher,playerx2,playery2,last_shot_time2,cooldown2,bullet_damage,event,bulletlist)
            mod,fire_mods,current_fire_mod = fire_mod_change(event,mod,fire_mods,current_fire_mod)



    # Draw background
    scroll_y -= 1
    if scroll_y <= 0:
        scroll_y = bg_height
    screen.blit(background, (0, - scroll_y))
    screen.blit(background,(0,bg_height - scroll_y))
    player_rect = playerimage.get_rect()
    player2_rect = playerimage2.get_rect()
    player_rect.topleft = (playerx,playery)
    player2_rect.topleft = (playerx2,playery2)
    

    text2 = font2.render("Points: " + str(player1_points),True,white)
    text4 = font4.render("PlayerTwo health: " + str(playerhealth2),True,white)
    playerhealth1_text = playerhealth1.render( "PlayerOne health: "+ str(playerhealth), True,white)
    text2_rect = text2.get_rect(center=(50,30))
    text4_rect = text4.get_rect(center=(300,80))
    playerhealth1_text_rect = playerhealth1_text.get_rect(center=(300,130))
    waves_passed_text = waves_passed.render('Current wave: ' + str(current_wave), True,white) 
    waves_passed_text_rect = waves_passed_text.get_rect(center=(82,130))


    # Loss
    if game_status == "loss":
        current_wave = 0
        player1_points = 0 
        playerx = 400 // 2
        playery = 700 - (700 // 4)
        playerx2 = 400 // 2
        playery2 = 700 - (700 // 4)
        lo_collected = 0
        playerhealth2 = 5
        playerhealth = 5
        playerstep = 5
        spaceship_img = spaceships[0]
        if "rapid_fire" in fire_mods:
            fire_mods.remove("rapid_fire")
        if "launcher" in fire_mods:
            fire_mods.remove("launcher")
        current_fire_mod = "single_fire"
        for enemy in enemylist:
            enemylist.remove(enemy)
        playerimage = pygame.image.load(spaceship_img).convert_alpha()
        # Shows "WARZONE DEFEAT" text
        screen.blit(text3, text3_rect) 
        replay = Buttons("images/try_again.png",x // 2 -150, 400)  
        enter_menu = Buttons("images/menu.png", 5, 10) 
        replay.screenblit(screen)
        game_status = replay.change_game_status(game_status,"ongoing")
        game_status = enter_menu.change_game_status(game_status,"menu")
        enter_menu.screenblit(screen)
    # Win
    elif game_status == "win":
        pygame.mixer.music.stop()
        screen.blit(text1, text1_rect)
        save_coins(dictionary_highscore)
    
    # Menu
    elif game_status == "menu":
        space.image_blit(screen)
        war.image_blit(screen)
        game_status,spaceship_img,player_image = start_game.start_detection(game_status,spaceships,spaceship_img,equipped_ship,playerimage)
        game_status = enter_shop.change_game_status(game_status,"shop")
        game_status = customize.change_game_status(game_status,"customize")
        start_game.screenblit(screen)
        enter_shop.screenblit(screen)
        customize.screenblit(screen)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    elif game_status == "customize":
        screen.blit(shop,(0,0))
        screen.blit(pygame.image.load(spaceships[equipped_ship]).convert_alpha(),(100,100))


    # Shop  
    elif game_status == "shop": 
        dictionary_highscore["coins"] = buy_stuff.buy_stuff(shop_page,dictionary_highscore["coins"],spaceships)
        screen.blit(shop,(0,0))
        shop_item_blit(shop_page,plane1,plane2,plane3,plane4,screen)
        buy_stuff.screenblit(screen)
        change_page.screenblit(screen)
        shop_page = change_page.shop_change_detection(shop_page)
        game_status = quit_shop.menu_detection(game_status)
        quit_shop.screenblit(screen)
        total_coins.image_blit(screen)
        total_coins.refresh_text("Coins: "+str(dictionary_highscore["coins"]),yellow)
        save_coins(dictionary_highscore)
    # Ongoing
    elif game_status == "ongoing":
        playerx,playery = player_movement(playerx,playery,playerstep)
        playerx2,playery2 = player_movement2(playerx2,playery2)
        if playerhealth == 0 or playerhealth2 == 0:
            game_status = "loss"
            dictionary_highscore = update_highscore(player1_points,coins,dictionary_highscore)
            lose_sound.play()
            playerhealth -= 1
            playerhealth2 -= 1
        # Draw player (needed so it still shows when no keys pressed)
        screen.blit(playerimage, (playerx, playery)) 
        screen.blit(playerimage2, (playerx2, playery2))
        # Blit text
        screen.blit(waves_passed_text, waves_passed_text_rect)
        screen.blit(highscore1, highscore_rect)
        screen.blit(text2, text2_rect)
        screen.blit(playerhealth1_text, playerhealth1_text_rect)
        screen.blit(text4, text4_rect)
        if not final_boss_spawned:
            pygame.mixer.music.fadeout(3000)
        #Append enemies
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
        for enemy_bullet in enemy_bullets:
            enemy_bullet.movement()
            enemy_bullet.image_blit(screen)
            if enemy_bullet.y > 700:
                enemy_bullets.remove(enemy_bullet)
            if enemy_bullet.rect.colliderect(player_rect):
                playerhealth -= 1
                enemy_bullets.remove(enemy_bullet)
            if enemy_bullet.rect.colliderect(player2_rect):
                playerhealth2 -= 1
                enemy_bullets.remove(enemy_bullet)   
        for enemy in enemylist:
            if enemy.rect.colliderect(player_rect):  
                playerhealth -= 1
                if enemy.finalboss == False:
                    enemylist.remove(enemy)
                    continue
                if enemy.zigzag:
                    playerhealth -= 2
                if enemy.bulletenemy:
                    playerhealth -= 1
            if enemy.rect.colliderect(player2_rect):  
                playerhealth2 -= 1
                if enemy.finalboss == False:
                    enemylist.remove(enemy)
                    continue
                if enemy.zigzag:
                    playerhealth -= 2
                if enemy.bulletenemy:
                    playerhealth -= 1  
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
                if bullet.rect.colliderect(enemy.rect):
                    bulletlist.remove(bullet)
                    if bullet.big_bullet == True:
                        enemy.enemyhealth -= 5
                    else:
                        enemy.enemyhealth -= bullet_damage

                    if enemy.enemyhealth <= 0:
                        enemylist.remove(enemy) 
                        coins += 1  
                                      
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
                            #make sure to add baby enemys here!!!                
                        else:
                            explosion_sound.play()
                            player1_points += 1
                            lo_spawn = random.choice([7,5,10,12])
                            #makes it a chance for loadout every time you kill an enemy
                            if lo_spawn == 7 and len(loadout_list) == 0:
                                loadout = Loadout("images/loadout.png")
                                loadout_list.append(loadout)
                                loadout_inbound.play()
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
    
        hitboxx,hitboxy,final_boss_spawned = finalboss_spawn(hitboxx,hitboxy,final_boss_spawned,player1_points,enemylist)
 
        if final_boss_killed == True:
            game_status = "win"
        enemyspawns,spawn_delay,enemyimage,enemyhealth = enemy_difficulty(player1_points,enemyspawns,enemyimage,spawn_delay,enemyhealth)

        for loadouts in loadout_list:    
            loadouts.image_blit(screen)
            playerhealth,playerhealth2,lo_collected = loadouts.detection(player_rect,playerhealth,playerhealth2,player2_rect,health_lo_collected,rapid_fire_collected,loadout_collected,lo_collected)
            loadouts.movement(screen)
            if loadouts.gone == True:
                loadout_list.remove(loadouts)
                if loadouts.collected:
                    if lo_collected >= 1:
                        playerimage,playercenter,cooldown,playerstep,cooldown2 = loadouts.loadout_rewards(playerstep,cooldown,cooldown2,lo_collected)
                    if loadouts.rapid_fire:
                        if not "rapid_fire" in fire_mods:
                            fire_mods.append("rapid_fire")
                    if loadouts.launcher:
                        if not "launcher" in fire_mods:
                            fire_mods.append("launcher")         


    pygame.display.flip()
    clock.tick(60)  