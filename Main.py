import pygame, sys
from pygame.locals import *

# from src.Game import Game
from src.Hero import Hero

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()  #this object will make sure our program runs at a certain maximum FPS

displayObj = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Game')

WHITE = (255, 255, 255)
heroImg = pygame.image.load('bloomy.png')
ourHero = Hero()
direction = 'right'
while True:  # the main game loop
    displayObj.fill(WHITE)

    displayObj.blit(heroImg, (ourHero.x, ourHero.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
        #handles if a key is pressed, and moves the hero
            if event.key in (K_LEFT, K_a) and ourHero.x >= 0:
                ourHero.move_x("n")
            if event.key in (K_RIGHT, K_d) and ourHero.x <= 940:
                ourHero.move_x("p")
            if event.key in (K_UP, K_w) and ourHero.y >= 0:
                ourHero.move_y("n")
            if event.key in (K_DOWN, K_s) and ourHero.y <= 540:
                ourHero.move_y("p")


    pygame.display.update()
    fpsClock.tick(FPS)

