import paho.mqtt.client as mqtt
import numpy as np

import time


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

# Variable for rps game
import random

#list of user inputs
inputOptions = ["rock", "paper", "scissors", "quit", "score"]
# list of options
options = ["rock", "paper", "scissors"]

# Score tracker
# global AIwins
# global PlayerWins

AIwins = 0
PlayerWins = 0

gettingMsg = True;



  #print('Received message: "' + str(message.payload)[2:-1] + '" on topic "' +
        #message.topic + '" with QoS ' + str(message.qos))
  #client.publish("ece180d/testk", int(str(message.payload)[2:-1]) + 1, qos=1)


    # time.sleep(10)


# Do what you want...
def rps(input, publisherInput):
    user_choice = input


# get user choice
        #client.publish("ece180d/testk", "Enter your choice (rock/paper/scissors/quit/score: ", qos=1)
    #while gettingMsg:
        #continue

    if publisherInput not in inputOptions:
        print("Invalid choice. Please enter rock, paper, scissors, quit, or score.")
# check if user input is valid
    if user_choice not in inputOptions:
        print("Invalid choice. Please enter rock, paper, scissors, quit, or score.")
    else:
        #if user_choice == "quit":
            #global playing = False
            #continue;
        if user_choice == "score":
            print("Wins: " + str(AIwins) + '\n' + "Your wins: " + str(PlayerWins))
            #continue;
    # get computer choice (ONLY IN SINGLE PLAYER VERSION)
        #computer_choice = random.choice(options)

    # compare choices and determine winner
        if user_choice == publisherInput:
            print("It's a tie!")
            return 0
        elif (user_choice == "rock" and publisherInput == "scissors") or (user_choice == "paper" and publisherInput == "rock") or (user_choice == "scissors" and publisherInput == "paper"):
            #print("You win! Your choice is " + user_choice + " and the publisher's choice is " + publisherInput)
            return 1
        else:
            # global AIwins
            #print("You lose! Your choice is " + user_choice + " and the publisher's choice is " + publisherInput)
            return -1
            #gettingMsg = True;

# The default message callback.
# (won't be used if only publishing, but can still exist)
# For multiplayer version... publisher takes over the role of the AI
def on_message(client, userdata, message):
    subscriberInput = str(message.payload)[2:-1]
    # Check that the subscriber sent a valid message
    global inputOptions
    global PlayerWins
    global AIwins
    res = 2
    if subscriberInput not in inputOptions:
        client.publish("ece180d/testk", "Invalid message.", qos=1)

    if subscriberInput == "score":
        client.publish("ece180d/testk", "Wins: " + str(PlayerWins) + " Losses: " + str(AIwins) + ". Enter your choice (rock/paper/scissors/quit/score): ", qos=1)
    elif subscriberInput == "quit":
        exit(1)
    else:
        pubInput = input("Enter your choice (rock/paper/scissors/quit/score): ").lower()
        res = rps(subscriberInput, pubInput)

    if res == 1:
        PlayerWins += 1
        print("You lose! Your choice is " + pubInput + " and the other player's choice is " + subscriberInput)
        print(PlayerWins, AIwins)
        client.publish("ece180d/testk", "You win! Your choice is " + subscriberInput + " and the other player's choice is " + pubInput + ". Enter your choice (rock/paper/scissors/quit/score): ", qos=1)
    elif res == -1:
        AIwins += 1
        print("You win! Your choice is " + pubInput + " and the other player's choice is " + subscriberInput)
        client.publish("ece180d/testk", "You lose! Your choice is " + subscriberInput + " and the other player's choice is " + pubInput + ". Enter your choice (rock/paper/scissors/quit/score): ", qos=1)
    elif res == 0:
        client.publish("ece180d/testk", "You tie! Your choice is " + subscriberInput + " and the other player's choice is " + pubInput + ". Enter your choice (rock/paper/scissors/quit/score): ", qos=1)
    #print(PlayerWins, AIwins)
    #client.publish("ece180d/testk", "Enter your choice (rock/paper/scissors/quit/score: ", qos=1)
    #gettingMsg = False;

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

# 4. use subscribe() to subscribe to a topic and receive messages.

# 5. use publish() to publish messages to the broker.
# payload must be a string, bytearray, int, float or None.
print('Publishing...')

# playing = True
# while playing:
#     client.publish("ece180d/testk", "Enter your choice (rock/paper/scissors/quit/score: ", qos=1)

client.publish("ece180d/testk", "Enter your choice (rock/paper/scissors/quit/score: ", qos=1)
while True:
    # print(PlayerWins, AIwins)
    pass # what will happen here is other non-communication things.
#Replace float(np.random.random(1)) with a message in client.publish above

# 6. use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
