# chrome dinosaur game
import pygame
import os
import random


pygame.init()

# Global variables-----------------------------------------------------------------
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GAME_SPEED = 14 
XBG = 0 # background x position
YBG = 380 # background y position

# Images
# Dinosaur
DINO_DEAD = [pygame.image.load("Images/Dino/DinoDead.png")]
DINO_RUN = [
    pygame.image.load("Images/Dino/DinoRun1.png"),
    pygame.image.load("Images/Dino/DinoRun2.png"),
]
DINO_JUMP = [pygame.image.load("Images/Dino/DinoJump.png")]
DINO_DUCK = [
    pygame.image.load("Images/Dino/DinoDuck1.png"),
    pygame.image.load("Images/Dino/DinoDuck2.png"),
]
DINO_START = [pygame.image.load("Images/Dino/DinoStart.png")]

# Bird
BIRD = [
    pygame.image.load("Images/Bird/Bird1.png"),
    pygame.image.load("Images/Bird/Bird2.png"),
]

# Cactus
CACTUS_LARGE = [
    pygame.image.load("Images/Cactus/LargeCactus1.png"),
    pygame.image.load("Images/Cactus/LargeCactus2.png"),
    pygame.image.load("Images/Cactus/LargeCactus3.png"),
]
CACTUS_SMALL = [
    pygame.image.load("Images/Cactus/SmallCactus1.png"),
    pygame.image.load("Images/Cactus/SmallCactus2.png"),
    pygame.image.load("Images/Cactus/SmallCactus3.png"),
]

# Other
OTHER = [
    pygame.image.load("Images/Other/Cloud.png"),
    pygame.image.load("Images/Other/GameOver.png"),
    pygame.image.load("Images/Other/Track.png"),
    pygame.image.load("Images/Other/Reset.png"),
]


# classes --------------------------------------------------------------------------


class Cloud:
    '''clouds are background objects for decoration'''
    def __init__(self):
        '''makes new clouds'''
        self.x = SCREEN_WIDTH + random.randint(800,1000)
        self.y = random.randint(50, 100)
        self.image = OTHER[0]
        self.width = self.image.get_width()

    def update(self):
        self.x -= GAME_SPEED
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Dinosaur:
    def __init__(self):
        '''Makes new Dinosaur object'''
        # self.dead_img = DINO_DEAD
        # self.duck_img = DINO_DUCK
        # self.jump_img = DINO_JUMP
        # self.run_img  = DINO_RUN
        # self.start_img = DINO_START

        # Dino States
        self.duck = False
        self.run = True
        self.jump = False
        self.X = 80  # default x position
        self.Y = 310  # default y position
        self.duck_height = 340
        self.jump_vel = 8.5

        self.step_index = 0
        self.image = DINO_RUN[0]
        self.rect = self.image.get_rect()

    def update(self, userInput):
        '''update the position of Dinosaur'''
        if self.duck:
            self.ducking()
        if self.run:
            self.running()
        if self.jump:
            self.jumping()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.jump: # if we arn't jumping
            self.jump = True
            self.run = False
            self.duck = False
        elif userInput[pygame.K_DOWN] and not self.jump:
            self.duck = True
            self.run = False
            self.jump = False
        elif not (self.jump or userInput[pygame.K_DOWN]):
            self.duck = False
            self.run = True
            self.jump = False

    def ducking(self):
        '''Helper for self.update()'''
        self.image = DINO_DUCK[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = 340
        self.step_index += 1

    def running(self):
        '''Helper for self.update()'''
        self.image = DINO_RUN[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.step_index += 1

    def jumping(self):
        '''Helper for self.update()'''
        self.image = DINO_JUMP[0]
        if self.jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -8.5:
            self.jump = False
            self.jump_vel = 8.5

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


# functions-----------------------------------------------------------------------------------------


def background():
    global XBG, YBG
    image_width = OTHER[2].get_width()
    SCREEN.blit(OTHER[2], (XBG, YBG))
    SCREEN.blit(OTHER[2], (image_width + XBG, YBG))
    if XBG <= -image_width:
        SCREEN.blit(OTHER[2], (image_width + XBG, YBG))
        XBG = 0 
    XBG -= GAME_SPEED


def main():
    runing = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()

    # Game loop
    while runing:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if we want to quit game
                runing = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        # draws player 
        player.draw(SCREEN)
        player.update(userInput)

        # draws player
        background()

        # draws cloud
        cloud.draw(SCREEN)
        cloud.update()

        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    main()
