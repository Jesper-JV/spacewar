import pygame
import random
import json
import sys

class Enemy_bullet():
    def __init__(self,enemyx,enemyy):
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.speed = -7
        self.rect = self.image.get_rect()
        self.x = enemyx + 5
        self.y = enemyy + 5

    def image_blit(self,screen):
        self.rect.topleft = (self.x,self.y)
        screen.blit(self.image, (self.x,self.y))

    def movement(self):
        self.y -= self.speed

class Enemy():
    def __init__(self,img_path,health,bullet_enemy,steps,finalboss = False,zigzag = False,baby = False):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.bulletimage = pygame.image.load("images/bullet.png").convert_alpha()
        self.x = random.randint(20,380)    
        self.y = random.randint(-2,0)
        self.rect = self.image.get_rect()
        self.bulletx = self.x
        self.bullety = self.y
        self.steps = steps
        self.enemyhealth = health
        health = 3
        self.bulletenemy = bullet_enemy
        self.finalboss = finalboss
        self.zigzag = zigzag
        self.baby = baby
        if self.finalboss == True:
            self.x = 150
            self.y = -400
  
    # Refreshes enemies image and position every frame    
    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))
    def movement(self,screen):
        self.rect.topleft = (self.x,self.y)   
    
        self.y += self.steps
    def zigzag_movement(self):
        
        if self.x > 360:
            self.steps = self.steps *(-1)
            self.y += 40
        if self.x < 0:
            self.steps = self.steps *(-1)
            self.y += 40
        self.x += self.steps
        return self.x, self.y
    
class Bullet():
    def __init__(self,playerx,playery,playercenter,img = "images/bullet.png",speed = 7,big_bullet = False):
        self.image = pygame.image.load(img).convert_alpha()
        self.speed = speed
        self.x = playerx+playercenter
        self.y = playery
        self.big_bullet = big_bullet
        self.rect = self.image.get_rect()

    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))

    def movement(self,screen):
        self.rect.topleft = (self.x,self.y)
     
        self.y -= self.speed

class Loadout():
    def __init__(self,img_path = "images/loadout.png",gone = False,health = False,rapid_fire = False,launcher = False):
        
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
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

    def detection(self,player_rect,playerhealth,playerhealth2,player2_rect,health_lo_collected,rapid_fire_collected,loadout_collected,lo_collected):
        
        if self.rect.colliderect(player_rect):
             
            playerhealth += 1  
            self.x =random.randint(0,360)
            self.y = -30 
            self.gone = True
            self.collected = True
            if self.health == True:
                playerhealth += 2
                health_lo_collected.play()
            elif not self.health:
                lo_collected += 1
                if self.rapid_fire:
                    rapid_fire_collected.play()
                elif self.launcher:
                    pass
                    
                else:
                    loadout_collected.play()

        if self.rect.colliderect(player2_rect): 
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
                lo_collected += 1
            if self.rapid_fire:
                rapid_fire_collected.play()
            elif self.launcher:
                rapid_fire_collected.play()
                    
            else:
                loadout_collected.play()



 
            self.gone = True
            if self.collected_amount >= 5:
                playerhealth2 += 2
        return playerhealth,playerhealth2,lo_collected
    
    def loadout_rewards(self,big_bullet_speed,playerstep,cooldown,cooldown2,lo_collected):
        
        spaceship_img = "images/spaceship_upg1.png"
        playerimage = pygame.image.load(spaceship_img).convert_alpha()
        playercenter = 48
        cooldown = 325
        big_bullet_speed = 5
        if lo_collected >= 2:
            cooldown = 200
            big_bullet_speed = 6
        if lo_collected == 3:
            playerstep = 7
            cooldown = 200

        if 5 > lo_collected >= 4:
            playerstep = 9
            cooldown = 0
    
        if lo_collected >= 5:
            playerstep = 10
            cooldown = 0

            
            
            
    

        return playerimage,playercenter,cooldown,playerstep,big_bullet_speed,cooldown2
    def movement(self,screen):

        self.y += self.speed
        self.rect.topleft = (self.x,self.y)
 
        if self.y > 700:
            self.gone = True
            
class Buttons():
    def __init__(self,img,x,y,purchase_number = 9999):
        self.image = pygame.image.load(img).convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.purchase_number = purchase_number
    def screenblit(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    def detection(self,game_status):
        pos = pygame.mouse.get_pos()
        print(pos)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                game_status = "ongoing"

        return game_status
    def start_detection(self,game_status):
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):  
            if pygame.mouse.get_pressed()[0] == 1:
                game_status = "ongoing"   
        return game_status 
    def menu_detection(self,game_status):
        pos = pygame.mouse.get_pos() 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                game_status = "menu"   
        return game_status
    def shop_detection(self,game_status,shop_page):
        pos = pygame.mouse.get_pos() 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                game_status = "shop" 
                shop_page = 1  
        return game_status,shop_page

    def buy_items(self,spaceship_list,coins):
        pos = pygame.mouse.get_pos() 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if self.purchase_number == 1 and coins >= 50:
                    spaceship_list.append("images/spaceship_num1")
                    coins -= 50
                if self.purchase_number == 2 and coins >= 100:
                    spaceship_list.append("images/spaceship_num2")
                    coins -= 100
                if self.purchase_number == 3 and coins >= 150:
                    spaceship_list.append("images/spaceship_num3")
                    coins -= 150
    def change_page(self,page):
        
        pos = pygame.mouse.get_pos() 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: 
                if page == 1:  
                    page = 2
                elif page == 2:  
                    page = 3
                elif page == 3:  
                    page = 4
                elif page == 4:  
                    page = 1
                print(page)
            
        return page
                
class Text():
    def __init__(self,size,text,color,x,y,font='freesansbold.ttf'):
        self.font = pygame.font.SysFont(font,size)
        self.text = self.font.render(text, True,color)
        self.text_rect = self.text.get_rect(center=(x,y))
    def image_blit(self,screen):
        screen.blit(self.text,self.text_rect)
    def refresh_text(self,text,color):
        self.text = self.font.render(str(text), True,color)

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

def update_highscore(player1_points,coins,dictionary_highscore):  
    dictionary_highscore["coins"] += coins    
    if player1_points > dictionary_highscore["highscore"]:
        username = input("what is your name? ")
        print(username)  
        dictionary_highscore["username"] = username
        dictionary_highscore["highscore"] = player1_points
    with open("highscore.txt", "w") as f:
        json.dump(dictionary_highscore,f)
    return dictionary_highscore

def save_coins(dictionary_highscore):

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

def finalboss_spawn(hitboxx,hitboxy,final_boss_spawned,player1_points,enemylist):
    if player1_points == 100 and final_boss_spawned == False:
        enemylist.append(Enemy("images/Final_boss.png",300,False,0.2,True,False))
        final_boss_spawned = True        
      
        pygame.mixer.music.load("sounds/boss.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
    return hitboxx,hitboxy,final_boss_spawned


def shoot_bullets(last_shot_time,cooldown,current_time,current_fire_mod,shoot_sound,playercenter,playerx,playery,launcher,playerx2,playery2,big_bullet_speed,last_shot_time2,cooldown2,bullet_damage,event,bulletlist):
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

