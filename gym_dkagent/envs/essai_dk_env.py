# -*- coding: utf-8 -*-
import gym
import threading
import random
from dk_server import DKServer

import numpy as np
import dqnSolver as dnq

import imageio

from ddqn import *

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
    
    def __init__(self, episode=10):
        
        # Starting the server
        self.server = DKServer()
        #self.server.start()
        
        self.server.resetClient()
        """
        inputMsg = ""
        while True:
            #print("Enter input:")
            inputMsg = input()
            #inputMsg = str(2) + ":" + str(random.randint(0,1))
            #if inputMsg == "bye":
            #    break
            
            #start dqn
            observation_space = 230 # ou 224 #size#env.observation_space.shape[0]
            action_space = 6
            dqn_solver = dnq.DQNSolver(observation_space, action_space)

            
            final = []
            for e in range(episode):
                
                state = self.server.resetClient()
                state = np.reshape(state, [1, observation_space])
                step = 0
                while True:
                    step += 1
                    #env.render()
                    action = dqn_solver.act(state)
                    # background, objects, reward, done
                    # state_next, reward, terminal, info = self.listToSendAction(action)
                    path, reward, terminal = self.listToSendAction(action)
                    
                    img = cv2.imread(path)

                    reward = reward if not terminal else -reward
                    state_next = np.reshape(state_next, [1, observation_space])
                    dqn_solver.remember(state, action, reward, state_next, terminal)
                    state = state_next
                    if terminal:
                        print("Run: " + str(e) + ", exploration: " + str(dqn_solver.exploration_rate) + ", score: " + str(step))
                        break
                    dqn_solver.experience_replay()
                final.append(step)

            #save results        
            dqn_solver.save("./dk_dqn.h5")
            
            #direction, aButton = inputMsg.split(":")
            
            #answer = self.server.sendAction(int(direction), int(aButton))
            answer = self.server.sendAction(int(direction), int(aButton))
            #print(answer)
            if int(answer[2]) == 1:
                print("MARIO IS DEAD")
                self.server.resetClient()
        """

        # ddqn

        self.server.sendAction(0,0)

        im = imageio.imread(path)
        im=np.dot(im[...,:3], [0.299, 0.587, 0.114])
        action_space = 6
        game_model = DDQNTrainer('dk', (224, 256,1), action_space)
        
        final = []
        run = 0
        total_step = 0
        while True:
            if run >= EPISODES:
                print("Finis les episodes")
                break

            run += 1
            self.server.resetClient()
            path, reward, terminal = self.server.sendAction(0,0) #env.reset()
            
            current_state = np.dot(imageio.imread(path)[...,:3], [0.299, 0.587, 0.114])

            step = 0
            score = 0

            while True:
                if total_step >= STEP_MAX:
                    print("Step maximum en tout atteint")
                    break #Je veux break de toutes les loops
                total_step += 1
                step += 1

                action = game_model.move(current_state)
                path, reward, terminal = self.listToSendAction(action) #env.step(action)
                
                
                next_state = np.dot(imageio.imread(path)[...,:3], [0.299, 0.587, 0.114])
                
                
                
                score += reward
                game_model.remember(current_state, action, reward, next_state, terminal)
                current_state = next_state

                game_model.step_update(total_step)

                if terminal:
                    final.append([score, step, run])
                    break
                    
            print("Run: " + str(run) + ", tot_step: " + str(total_step) + ", score: " + str(score))
        self.server.resetClient()
        self.server.close()
        
        return final
        

    def listToSendAction(self, listActions):
        return self.server.sendAction(listActions.index(max(listActions[:4]))+1, listActions.index(max(listActions[4:]))+4)
    
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