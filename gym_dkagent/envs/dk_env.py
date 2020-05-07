# -*- coding: utf-8 -*-
import gym
import threading
import random
from dk_server import DKServer

class DKEnv(gym.Env):
    """
    DonkeyKong Environment.
    
    Observation: 
        * Background of the level
        * Objects in the level
        
    Actions:
        Type: Discrete(2)
        Num	Action
        0	Left
        1	Right
        2   Up
        3   Down
        4   A Button
        5   B Button

    Reward:
        ?

    Episode Termination:
        Level finished
    """
    
    def __init__(self):
        
        # Starting the server
        self.server = DKServer()
        #self.server.start()
        
        self.server.resetClient()
        
        inputMsg = ""
        while True:
            #print("Enter input:")
            #inputMsg = input()
            inputMsg = str(2) + ":" + str(random.randint(0,1))
            if inputMsg == "bye":
                break;
                
            
            
            direction, aButton = inputMsg.split(":")
            
            answer = self.server.sendAction(int(direction), int(aButton))
            #print(answer)
            if int(answer[2]) == 1:
                print("MARIO IS DEAD")
                self.server.resetClient()
            
        self.server.resetClient()
        self.server.close()
        
        pass
    
    def reset(self):
        observation = 0
        return observation
    
    def step(self, action):
        observation, reward, done, info = 0
        
        return observation, reward, done, info
    
    def render(self, mode='human'):
        pass


DKEnv()
"""
net = Network()
msg = ""
while msg != "exit":
    
    # We get the message from the Bizhawk client
    msg = net.recv()
    print(msg)
    
net.close()
"""