# Simple pygame program
# https://pygame.readthedocs.io/en/latest/3_image/image.html#:~:text=Work%20with%20images%20%C2%B6%201%20Load%20an%20image,Transform%20the%20image%20with%20the%20mouse%20%C2%B6%20
# Import and initialize the pygame library
import time
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random
options = ["rock", "paper", "scissors"]
# Score tracker
AIwins = 0;
PlayerWins = 0;
#GRAY = (150, 150, 150)

# initialize pygame
pygame.init()

# load images
rock = pygame.image.load('rock.png')
paper = pygame.image.load('paper.png')
scissors = pygame.image.load('scissors.png')
choices = pygame.image.load('choices.png')
youWon = pygame.image.load('youWon.png')
youLost = pygame.image.load('youLost.png')
Tie = pygame.image.load('Tie.png')

# convert to optmize the image formate and make drawing faster
#rock.convert()
#rectRock = rock.get_rect()
#rectRock.center = w//2, h//2

# resize images

Rwidth = rock.get_rect().width
Rheight = rock.get_rect().height
Pwidth = paper.get_rect().width
Pheight = paper.get_rect().height
Swidth = scissors.get_rect().width
Sheight = scissors.get_rect().height
Cwidth = choices.get_rect().width
Cheight = choices.get_rect().height

rock = pygame.transform.scale(rock, (Rwidth*0.08, Rheight*0.08))
paper = pygame.transform.scale(paper, (Pwidth*0.38, Pheight*0.38))
scissors = pygame.transform.scale(scissors, (Swidth*0.2, Sheight*0.2))
choices = pygame.transform.scale(choices, (Cwidth*0.7, Cheight*0.7))

# Set up the drawing window
screen = pygame.display.set_mode([600, 600])

# function to determine winner (returns 1 if player won, 0 if tie, and -1 if AI won)
def determineWinner(str1, str2) -> int:
    if str1 == str2:
        print("It's a tie!")
        #global GRAY
        return 0
    elif (str1 == "rock" and str2 == "scissors") or (str1 == "paper" and str2 == "rock") or (str1 == "scissors" and str2 == "paper"):
        print("You win! Your choice is " + str1 + " and the computer's choice is " + str2)
        #global PlayerWins
        #PlayerWins += 1;
        #global GRAY
        # screen.fill(150, 150, 150)
        # screen.blit(youWon,(250,300))
        # pygame.display.flip()
        return 1

    else:
        print("You lose! Your choice is " + str1 + " and the computer's choice is " + str2)
        #global AIwins
        #AIwins += 1;
        #global GRAY
        # screen.fill(150, 150, 150)
        # screen.blit(youLost,(250,300))
        # pygame.display.flip()
        return -1

# Run until the user asks to quit
running = True
while running:
    # Fill the background with white
    #screen.fill((255, 255, 255))
    #global GRAY
    GRAY = (150, 150, 150)
    screen.fill(GRAY)

    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Draw pictures
    screen.blit(rock,(0,200))
    screen.blit(paper,(200,200))
    screen.blit(scissors,(400,200))
    screen.blit(choices,(200,400))

    # Flip the display
    pygame.display.flip()

    # Get AI choice
    computer_choice = random.choice(options)

    # Get player choice
    # Did the user click the window close button?
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == pygame.QUIT:
                running = False
            if event.key == pygame.K_UP:
                # User chose rock
                temp = determineWinner("rock",computer_choice)
                if (temp == 0):
                    screen.fill(GRAY)
                    screen.blit(Tie,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                if (temp == 1):
                    screen.fill(GRAY)
                    screen.blit(youWon,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                    #global PlayerWins
                    PlayerWins += 1;
                if (temp == -1):
                    screen.fill(GRAY)
                    screen.blit(youLost,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                    #global AIwins
                    AIwins += 1;
            if event.key == pygame.K_LEFT:
                # User chose paper
                temp = determineWinner("paper",computer_choice)
                if (temp == 0):
                    screen.fill(GRAY)
                    screen.blit(Tie,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                if (temp == 1):
                    screen.fill(GRAY)
                    screen.blit(youWon,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                    #global PlayerWins
                    PlayerWins += 1;
                if (temp == -1):
                    screen.fill(GRAY)
                    screen.blit(youLost,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                    #global AIwins
                    AIwins += 1;
            if event.key == pygame.K_RIGHT:
                # User chose scissors
                temp = determineWinner("scissors",computer_choice)
                if (temp == 0):
                    screen.fill(GRAY)
                    screen.blit(Tie,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                if (temp == 1):
                    screen.fill(GRAY)
                    screen.blit(youWon,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                    #global PlayerWins
                    PlayerWins += 1;
                if (temp == -1):
                    screen.fill(GRAY)
                    screen.blit(youLost,(250,300))
                    pygame.display.flip()
                    time.sleep(1)
                    #global AIwins
                    AIwins += 1;
            if event.key == pygame.K_DOWN:
                # User requested score
                print("Wins: " + str(PlayerWins) + " " + "Losses: " + str(AIwins))
            if event.key == pygame.K_ESCAPE:
                # Quit the game
                running = False

# Done! Time to quit.
pygame.quit()
