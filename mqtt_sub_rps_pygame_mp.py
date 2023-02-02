import paho.mqtt.client as mqtt
import pygame
#import numpy as np
import time

pubPygameInput = ""
subPygameInput = ""

own_data_received = False
opp_data_received = False

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/sub")

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')

def on_message(client, userdata, message):
    publisherInput = str(message.payload)[2:-1]
    inputOptions = ["rock", "paper", "scissors", "quit", "score"]
    global PlayerWins
    global AIwins
    global pubPygameInput
    global opp_data_received
    #res = 2
    if publisherInput not in inputOptions:
        print("subscriber input invalid.")
    elif not opp_data_received:
        pubPygameInput = str(message.payload)[2:-1]
        opp_data_received = True

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

options = ["rock", "paper", "scissors"]
# Score tracker
AIwins = 0;
PlayerWins = 0;

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
        return 0
    elif (str1 == "rock" and str2 == "scissors") or (str1 == "paper" and str2 == "rock") or (str1 == "scissors" and str2 == "paper"):
        print("You win! Your choice is " + str1 + " and your opponents choice is " + str2)
        return 1

    else:
        print("You lose! Your choice is " + str1 + " and your opponents choice is " + str2)
        return -1

def updateScreen():
    # Fill the background with Gray
    GRAY = (150, 150, 150)
    screen.fill(GRAY)

    # Draw pictures
    screen.blit(rock,(0,200))
    screen.blit(paper,(200,200))
    screen.blit(scissors,(400,200))
    screen.blit(choices,(200,400))

    # Flip the display
    pygame.display.flip()


# Run until the user asks to quit
running = True
while running:

    updateScreen()

    #print("Enter your choice: up/down/left/right/esc")
    # Get player choice
    # Did the user click the window close button?
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key in [pygame.QUIT, pygame.K_ESCAPE]:
                running = False
            elif event.key == pygame.K_DOWN:
                # User requested score
                # PlayerWins is opponents and AIwins is publisher's wins
                print("Wins: " + str(PlayerWins) + " " + "Losses: " + str(AIwins))
            elif not own_data_received:
                if event.key == pygame.K_UP:
                    # User chose rock
                    subPygameInput = "rock"
                    own_data_received = True
                    client.publish("ece180d/testk", "rock", qos=1)
                if event.key == pygame.K_LEFT:
                    # User chose paper
                    subPygameInput = "paper"
                    own_data_received = True
                    client.publish("ece180d/testk", "paper", qos=1)
                if event.key == pygame.K_RIGHT:
                    # User chose scissors
                    subPygameInput = "scissors"
                    own_data_received = True
                    client.publish("ece180d/testk", "scissors", qos=1)
            #if own_data_received:
                #print(subPygameInput)

    if own_data_received and opp_data_received:
        temp = determineWinner(subPygameInput,pubPygameInput)
        if (temp == 0):
            GRAY = (150,150,150)
            screen.fill(GRAY)
            screen.blit(Tie,(250,300))
            pygame.display.flip()
            time.sleep(1)
            pubPygameInput = ""
            own_data_received = False
            opp_data_received = False
            updateScreen()
        if (temp == 1):
            GRAY = (150,150,150)
            screen.fill(GRAY)
            screen.blit(youWon,(250,300))
            pygame.display.flip()
            time.sleep(1)
            #global PlayerWins
            PlayerWins += 1;
            pubPygameInput = ""
            own_data_received = False
            opp_data_received = False
            updateScreen()
        if (temp == -1):
            GRAY = (150,150,150)
            screen.fill(GRAY)
            screen.blit(youLost,(250,300))
            pygame.display.flip()
            time.sleep(1)
            #global AIwins
            AIwins += 1;
            pubPygameInput = ""
            own_data_received = False
            opp_data_received = False
            updateScreen()

# Done! Time to quit.
pygame.quit()


while True:
    # print(PlayerWins, AIwins)
    pass # what will happen here is other non-communication things.

# 6. use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
