import pygame
import random

playercenter = 24

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
    def __init__(self,playerx,playery,playercenter,img = "images/bullet.png",speed = 7):
        self.image = pygame.image.load(img).convert_alpha()
        self.speed = speed
        self.x = playerx+playercenter
        self.y = playery

    def image_blit(self,screen):
        screen.blit(self.image, (self.x,self.y))

    def movement(self):
        self.y -= self.speed

   