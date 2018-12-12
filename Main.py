import pygame, sys
from pygame.locals import *
import random
from setting import *

import os
from os import path


from src.Hero import Hero
from src.Zombie import *
from src.Bullet import *
from src.Game import Game
from src.Walls import Walls
from src.Item import *
from src.Effects import *


"""----------------------PARAMETERS----------------------------"""


#dist_center_xmin = img_width / 2 + Tile_size / 2
#dist_center_ymin = img_height / 2 + Tile_size / 2
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGTH = HEIGHT / TILE_SIZE

LAST_HIT_TIME = 0.5
last_hit_t = LAST_HIT_TIME  #initializes the time variable that we are going to use to limit the collisions between the hero and the zombies
last_attack_time = 0.
frequency_Zombie = FREQUENCY_ZOMBIE



vel_x, vel_y = 0., 0.  # inicializes the x and y components of the velocity vector of the hero movement intention
zombie_vel = pygame.math.Vector2(0., 0.)
backpack_killed = 0
last_shot = 0
shotgun_ammo = 0
level = 1
weaponType = "Pistol"
first_time = True
second_time = False
final_screen = False
game_complete = False
maps = []
map_data = []
map2_data = []
map3_data = []
play_mode = False
menu_mode = False
new_zombie_delete = False
game_folder = path.dirname(__file__)

"""----------------------PYGAME INITIALIZING---------------------------"""
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('8-Bit Madness', 35)

Pistol_sound = pygame.mixer.Sound(PISTOL_SOUND)
Shotgun_sound = pygame.mixer.Sound(SHOTGUN_SOUND)
Gun_pickup = pygame.mixer.Sound(GUN_PICKUP_SOUND)


for sounds in range(len(Player_sound)):
    Player_sound[sounds] = pygame.mixer.Sound("snd/Player_Sound/" + Player_sound[sounds])
    Player_sound[sounds].set_volume(2.0)

for z in range(len(Zombie_sound)):
    Zombie_sound[z] = pygame.mixer.Sound("snd/Zombie_Sound/" + Zombie_sound[z])
    Zombie_sound[z].set_volume(2.0)

fpsClock = pygame.time.Clock()

"""----------------------SCREEN OBJECT----------------------------"""

displayObj = pygame.display.set_mode((WIDTH, HEIGHT))  # creates the object that display the screen
pygame.display.set_caption('Game')


"""----------------------GAME OBJECT: display start screen, intro, menu----------------------------"""

game = Game()
game.show_start_screen(displayObj)
game.show_intro(displayObj)
play_mode = game.menu(displayObj)

#initial music
level_1_sound = pygame.mixer.music.load("snd/Level_Sound/Level1.mp3")
pygame.mixer.music.play(2)

#to display the instruccions
game.instructions(displayObj)

"""----------------------INITIAL INSTANCES AND GROUPS CREATION----------------------------"""
ourHero = Hero()

# here we create a sprite group to make easier to manage our zombies instances
crewZombies = pygame.sprite.Group()
groupBullets = pygame.sprite.Group()
ourWall = pygame.sprite.Group()
ourItems = pygame.sprite.Group()
ourEffects = pygame.sprite.Group()
# pygame.key.set_repeat(1, 10) #to handle the "holding key" event


pygame.display.flip()

"""-----------------------------MAP CREATION----------------------------"""

with open(path.join(game_folder, 'map/FirstMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map_data.append(line)

with open(path.join(game_folder, 'map/SecondMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map2_data.append(line)

with open(path.join(game_folder, 'map/ThirdMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map3_data.append(line)

"""----------------------------------------------------------------------------"""
"""--------------------------------GAME LOOP-----------------------------------"""
"""----------------------------------------------------------------------------"""

while play_mode:  # the main game loop

    """------------------------MAP CREATION IN FUNCTION OF THE LEVEL---------------------------"""

    if level == 1:
        maps = map_data
    elif level == 2:
        maps = map2_data
    else:
        maps = map3_data

    ourWall.empty()
    for row, tiles in enumerate(maps):  # enumerate to get both index and value as row and column
        for col, tile in enumerate(tiles):
            if tile == "1":
                ourWall.add(Walls(col, row, TILE_SIZE))

    if level == 1:
        background_image = pygame.image.load("img/background/level1_1024.jpg").convert()
    elif level == 2:
        background_image = pygame.image.load("img/background/level2.jpg").convert()
    elif final_screen == False:
        background_image = pygame.image.load("img/background/level3_begin.jpg").convert()
    else:
        background_image = pygame.image.load("img/background/level3_final.jpg").convert()

    displayObj.blit(background_image, [0, 0])

    """------------------------INSTANCES CREATION---------------------------"""
    #·····························BACKPACKS································
    if first_time == True:
        for i in range(MAX_BACKPACKS):
            ourItems.add(Backpack(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT / 4 * 3)))
        first_time = False
    else:
        for i in range(backpack_killed):
            #it keeps creating backpacks if they've been destroyed because of the collisions with the wall
            ourItems.add(Backpack(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT / 4 * 3)))
        backpack_killed = 0

    # ·····························ZOMBIES································
    if random.randrange(0, 100) < frequency_Zombie:  # here, a probability of "frecuency zombie" is assigned to the appearance of a new zombie
        # if a new zombie instance is created, it is added to the sprite group
        if random.randrange(0, 100) < PROBABILITY_SUPERZOMBIE:
            zombie_new = SuperZombie(random.randrange(0, WIDTH - img_width), random.randrange(0, HEIGHT - img_height))
        else:
            zombie_new = Zombie(random.randrange(0, WIDTH - img_width), random.randrange(0, HEIGHT - img_height))
        newzombie_walls_collision = pygame.sprite.spritecollide(zombie_new, ourWall, False)
        for wall in ourWall:
            if(zombie_new.collision_wall_x(wall.rect.centerx, wall.rect.centery) != "none" or zombie_new.collision_wall_y(wall.rect.centery, wall.rect.centery) != "none") or zombie_new.hero_near(ourHero.rect):
                new_zombie_delete = True
        if len(newzombie_walls_collision)==0 and new_zombie_delete == False:
            crewZombies.add(zombie_new)

        else:
            new_zombie_delete = False



    # ·····························GUNS································
    if random.randrange(0, 1000) < FREQUENCY_GUN:
        ourItems.add(Shotgun(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT - TILE_SIZE)))

    # ·····························LIVES································
    if random.randrange(0, 1000) < FREQUENCY_LIVES:
        ourItems.add(Health(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT - TILE_SIZE)))






    """----------------------OBJECTS DISPLAY----------------------------"""

    # ·····························AMMU································
    if shotgun_ammo > 0:  # only display the text on screen when the player is using shotgun
        displayObj.blit(ourHero.ammo_img, (WIDTH - 110, 30))
        
    # ............................LIFEBAR...............................
    displayObj.blit(ourHero.lives_img, (WIDTH - 200, 0))

    # ·····························SCORE································
    score_counter = myfont.render(str(ourHero.score), False, (255, 255, 255))
    displayObj.blit(score_counter, (WIDTH - 170, 30))
    displayObj.blit(ourHero.score_icon, (WIDTH - 200, 30))
    
    # ..........................BACKPACKS......................................
    backpack_collected = myfont.render(str(ourHero.backpack_collected), False, (255, 255, 255))
    displayObj.blit(backpack_collected, (WIDTH - 170, 60))
    displayObj.blit(ourHero.backpack_icon, (WIDTH - 200, 60))

    # ·····························SPRITE GROUPS································
    groupBullets.draw(displayObj)
    ourEffects.draw(displayObj)
    ourItems.draw(displayObj)
    crewZombies.draw(displayObj)
    ourHero.display(displayObj)
    for zombie in crewZombies:
        if type(zombie) == SuperZombie:
            zombie.life_bar_display(displayObj)

    if (pygame.time.get_ticks() - last_attack_time) < MAX_TIME_DISPLAY:
        ourHero.under_attack_display(displayObj)



    """---------------------------------COLLISIONS : PART 1---------------------------------"""

    hero_zombies_collision = pygame.sprite.spritecollide(ourHero, crewZombies, False)
    hero_wall_collision = pygame.sprite.spritecollide(ourHero, ourWall, False)
    hero_item_collision = pygame.sprite.spritecollide(ourHero, ourItems, False)

    # ·····························ZOMBIE - HERO································
    for zombie in hero_zombies_collision:
        # for each zombie that has taken part in the collision, we check if it's been at least 2 seconds from the last collision that was counted
        last_hit_t += time_passed_s
        if last_hit_t >= LAST_HIT_TIME:
            rand_sound = random.randint(0, len(Player_sound) - 1)
            pygame.mixer.Sound.play(Player_sound[rand_sound])
            ourHero.lives -= 1  # here our hero loses one life per zombie in the collisions list
            last_attack_time = ourHero.get_time_hit()
            ourEffects.add(Red_screen())
            ourHero.update_livebar(ourHero.lives)
            last_hit_t = 0.0  # set the time from the last collision to hero
            if ourHero.lives == 0:  # If Hero dies show Game Over screen
                if game.show_over_screen(displayObj, ourHero.score) == True:
                    ourHero = Hero()
                    crewZombies.empty()
                    groupBullets.empty()
                    ourItems.empty()
                    ourWall.empty()
                    level = 1
                    vel_x, vel_y = 0., 0.  # initializes the x and y components of the velocity vector of the hero
                    backpack_killed = 0
                    last_shot = 0
                    shotgun_ammo = 0
                    first_time = True
                    second_time = False
                    frequency_Zombie = FREQUENCY_ZOMBIE

    # ·····························ITEMS - HERO································
    for hit in hero_item_collision:
        if type(hit) == Health and ourHero.lives < 5:
            hit.kill()
            ourHero.lives += 1
            ourHero.update_livebar(ourHero.lives)
        elif type(hit) == Shotgun:
            if shotgun_ammo < 6:
                hit.kill()
                pygame.mixer.Sound.play(Gun_pickup)
                weaponType = "Shotgun"
                shotgun_ammo = 6
            ourHero.update_ammo(shotgun_ammo)
            displayObj.blit(ourHero.ammo_img, (WIDTH - 110, 30))
        elif type(hit) == Backpack:
            ourHero.backpack_collected += 1
            hit.kill()

    # ·····························ITEMS - WALL································
    for wall in ourWall:
        item_wall_collision = pygame.sprite.spritecollide(wall,ourItems,False)
        for item in item_wall_collision:
            if type(item) == Backpack:
                backpack_killed += 1
            item.kill()

    # ·····························ZOMBIE - BULLETS································
    if len(groupBullets.sprites()) > 0:
        for bul in groupBullets:
            bullet_zombies_collision = pygame.sprite.spritecollide(bul, crewZombies, False)
            bullet_wall_collision = pygame.sprite.spritecollide(bul, ourWall, False)
            # if there is a collision the bullets is also deleted from the group
            if len(bullet_wall_collision) > 0:
                bul.kill()
            if len(bullet_zombies_collision) > 0:
                bul.kill()
                for z in bullet_zombies_collision:
                    ourEffects.add(Splash(bul.rect.x, bul.rect.y))
                    if z.updates_life() is True:
                        ourHero.score += 1




    hero_zombies_collision.clear()

    #sound of the roar of zombies randomized
    if len(crewZombies.sprites()) > 0:
        if random.randrange(0, 1000) < 3:
            pygame.mixer.Sound.play(Zombie_sound[random.randint(0, len(Zombie_sound) - 1)])

    """----------------------EVENTS HANDLING----------------------------"""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()  # ends pygame
            os._exit(0)
            sys.exit()  # ends the program

        if event.type == KEYUP:
            # handles if a key is released
            if event.key in (K_LEFT, K_a):
                vel_x = 0.
            if event.key in (K_RIGHT, K_d):
                vel_x = 0.
            if event.key in (K_UP, K_w):
                vel_y = 0.
            if event.key in (K_DOWN, K_s):
                vel_y = 0.
        if event.type == KEYDOWN:
            # handles if a key is pressed, and moves the hero
            if event.key in (K_LEFT, K_a):
                vel_x = -1.
            if event.key in (K_RIGHT, K_d):
                vel_x = 1.
            if event.key in (K_UP, K_w):
                vel_y = -1.
            if event.key in (K_DOWN, K_s):
                vel_y = 1.
            if event.key == K_n:
                level = 2
            if event.key == K_l:
                level = 3
            if event.key == K_o:
                game_complete = True


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                now = pygame.time.get_ticks()

                if weaponType == "Pistol":
                    Bullet_Rate = 350
                    if now - last_shot > Bullet_Rate:
                        last_shot = now
                        groupBullets.add(Pistol_bullet(ourHero.rect))
                        pygame.mixer.Sound.play(Pistol_sound)
                elif weaponType == "Shotgun":
                    Bullet_Rate = 1200
                    if now - last_shot > Bullet_Rate:
                        last_shot = now
                        if shotgun_ammo > 0:
                            shotgun_ammo -= 1

                            for x in range(10):
                                groupBullets.add(Shotgun_Bullet(ourHero.rect))
                                pygame.mixer.Sound.play(Shotgun_sound)
                            ourHero.update_ammo(shotgun_ammo)
                        else:
                            weaponType = "Pistol"

    """---------------------------------COLLISIONS : PART 2---------------------------------"""
    # ···································HERO - WALLS································

    for wall in ourWall:
        colx = ourHero.collision_wall_x(wall.rect.centerx,wall.rect.centery)
        coly = ourHero.collision_wall_y(wall.rect.centerx, wall.rect.centery)
        if colx == "left" and vel_x > 0:
            vel_x = 0.
        elif colx == "right" and vel_x < 0:
            vel_x = 0.
        if coly == "top" and vel_y > 0:
            vel_y = 0.
        elif coly == "bottom" and vel_y < 0:
            vel_y = 0.

    for zombie in crewZombies:
        zombie_vel = zombie.trajectory_intention(ourHero.rect)
        for wall in ourWall:
            colx_zombie = zombie.collision_wall_x(wall.rect.centerx, wall.rect.centery)
            if colx_zombie == "left" and zombie_vel.x > 0:
                zombie_vel.x = 0.
            elif colx_zombie == "right" and zombie_vel.x < 0:
                zombie_vel.x = 0.
        for wall in ourWall:
            coly_zombie = zombie.collision_wall_y(wall.rect.centerx, wall.rect.centery)
            if coly_zombie == "top" and zombie_vel.y > 0:
                zombie_vel.y = 0.
            elif coly_zombie == "bottom" and zombie_vel.y < 0:
                zombie_vel.y = 0.
        zombie.set_vel(zombie_vel)


    """---------------------------------UPDATES---------------------------------"""

    # sets the frames per second to our clock object and store the time passed from the last call in time_passed_ms
    ourHero.set_vel(pygame.math.Vector2(vel_x, vel_y))
    time_passed_ms = fpsClock.tick(FPS)

    # converts the time to seconds
    time_passed_s = time_passed_ms / 1000.0
    # call the hero method to update its position, based on the time passed and its velocity

    # the function update of the sprite group basically calls the update function of each sprite of the group
    # so the zombies update method changes its position, based on the position of the hero the time passed
    crewZombies.update(ourHero.rect, time_passed_s)
    groupBullets.update(time_passed_s)
    ourHero.update(time_passed_s)
    ourEffects.update()

    if ourHero.backpack_collected >= MAX_BACKPACKS:
        if ourHero.if_checkpoint(CHECKPOINT_X_MIN, WIDTH, CHECKPOINT_Y_MIN, CHECKPOINT_Y_MAX):
            if level == 1:
                level = 2
                first_time = True
                #reinitializes the position of the hero and delete the zombies
                ourHero.backpack_collected=0
                ourHero.set_pos2(48, 48)
                frequency_Zombie *=4
                crewZombies.empty()
                ourItems.empty()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("snd/Level_Sound/Level2.mp3")
                pygame.mixer.music.play(2)

            elif level == 2:
                level = 3
                frequency_Zombie /=4
                ourHero.set_pos2(48, 48)
                crewZombies.empty()
                ourItems.empty()
                ourHero.backpack_collected = 0
                first_time = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("snd/Level_Sound/Level3.mp3")
                pygame.mixer.music.play(2)
            elif final_screen == True:
                game_complete = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("snd/Level_Sound/GameComplete.mp3")
                pygame.mixer.music.play(2)

        elif level == 3 and ourHero.if_checkpoint(FINAL_XMIN, FINAL_XMAX, FINAL_YMIN, FINAL_YMAX):
            final_screen = True

    if game_complete == True:
        if game.game_complete_screen(displayObj, ourHero.score) == True:
            ourHero = Hero()
            crewZombies.empty()
            groupBullets.empty()
            ourItems.empty()
            ourWall.empty()
            level = 1
            vel_x, vel_y = 0., 0.  # inicializes the x and y components of the velocity vector of the hero
            backpack_killed = 0
            last_shot = 0
            shotgun_ammo = 0
            first_time = True
            second_time = False
            final_screen = False
            game_complete = False
            frequency_Zombie = FREQUENCY_ZOMBIE



    pygame.display.flip()  # DO WE NEED BOTH OS THESE?!!!! update the screen with what we've drawn
    pygame.display.update()  # updates the state of the game



