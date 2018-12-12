import pygame, sys
from pygame.locals import *
from src.Person import Person
from setting import *

import math


pygame.font.init()
font_lives = pygame.font.SysFont('8-Bit Madness', 15)


class Hero(Person):

    speed = 150  # set the module of velocity

    hero_IMG = pygame.image.load(HERO_IMG)
    backpack_icon = pygame.image.load(BACKPACK_ICON_IMG)
    score_icon = pygame.image.load(SCORE_ICON_IMG)

    for z in range(len(BULLETS_IMG)):
        BULLETS_IMG[z] = pygame.image.load("img/effects/shotgun_ammo/" + BULLETS_IMG[z])
    for b in range(len(LIFE_BAR_IMG)):
        LIFE_BAR_IMG[b] = pygame.image.load("img/effects/life_bar/player/" + LIFE_BAR_IMG[b])



    def __init__(self):
        super().__init__()
        self.image = Hero.hero_IMG
        self.rect = self.image.get_rect()
        self.rect.x = INI_HERO_X
        self.rect.y = INI_HERO_Y
        self.vel = pygame.math.Vector2(0.0, 0.0) #inicialize the velocity vector to 0,0
        self.pos = self.rect
        self.score = 0
        self.lives = LIVES_INI
        self.lives_img = LIFE_BAR_IMG[len(LIFE_BAR_IMG) - 1]
        self.ammo_img = BULLETS_IMG[len(BULLETS_IMG) - 1]
        self.backpack_icon = Hero.backpack_icon
        self.score_icon = Hero.score_icon
        self.img_width = 49
        self.img_height = 43
        self.pos_max_x = WIDTH - self.img_width
        self.pos_max_y = HEIGHT - self.img_height
        self.backpack_collected = 0

    def get_rot_mouse(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rotate(mouse_x, mouse_y)

    def set_pos2(self, x, y):

        self.rect.x = x
        self.rect.y = y

    def under_attack_display(self, screen):
        attack_effect = font_lives.render("-200", False, RED)
        screen.blit(attack_effect,(self.rect.centerx, self.rect.centery - self.img_height-5))

    def update_livebar(self, num_lives):
        """
            Method that update the life bar image when the hero gain or lose lives
            :param num_lives : number of lifes left
        """
        self.lives_img = LIFE_BAR_IMG[num_lives - 1]

    def update_ammo(self, num_bullets):

        self.ammo_img = BULLETS_IMG[(num_bullets - 1)]


    def update(self,t):
        self.get_rot_mouse()
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(Hero.hero_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.set_pos(t)

    def if_checkpoint(self, cp_xmin, cp_xmax, cp_ymin, cp_ymax):
        if self.rect.centerx > cp_xmin and self.rect.centerx < cp_xmax  and self.rect.centery > cp_ymin and self.rect.centery < cp_ymax:
            return True

