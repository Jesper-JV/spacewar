import pygame
import random



class Enemy_bullet():
    def __init__(self,enemyx,enemyy):
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.speed = -7
        
        self.x = enemyx + 5
        self.y = enemyy + 5

    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))

    def movement(self):
        self.y -= self.speed

class Enemy():
    def __init__(self,img_path,health,bullet_enemy,steps,finalboss = False,zigzag = False,baby = False):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.bulletimage = pygame.image.load("images/bullet.png").convert_alpha()
        self.x = random.randint(20,380)    
        self.y = random.randint(-2,0)
        self.bulletx = self.x
        self.bullety = self.y
        self.steps = steps
        self.enemyhealth = health
        health = 3
        self.bulletenemy = bullet_enemy
        self.finalboss = finalboss
        self.zigzag = zigzag
        self.baby = baby
  
    # Refreshes enemies image and position every frame    
    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))
    def movement(self):
        
        self.y += self.steps
    def zigzag_movement(self):
        
        if self.x > 360:
            self.y += 40
            self.steps = self.steps *(-1)
        if self.x < 0:
            self.y += 40
            self.steps = self.steps *(-1)
        self.x += self.steps
        return self.x, self.y

 

    
class Bullet():
    def __init__(self,playerx,playery,playercenter,img = "images/bullet.png",speed = 7,big_bullet = False):
        self.image = pygame.image.load(img).convert_alpha()
        self.speed = speed
        self.x = playerx+playercenter
        self.y = playery
        self.big_bullet = big_bullet

    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))

    def movement(self):
        self.y -= self.speed

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

    def detection(self,playerx,playery,playerhealth,playerhealth2,playerx2,playery2,health_lo_collected,rapid_fire_collected,loadout_collected):
        
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
        if self.collected_amount == 3:
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
            
   