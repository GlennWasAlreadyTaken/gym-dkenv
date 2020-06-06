import numpy as np
import os
import random
import shutil
import sys
from statistics import mean
from datetime import datetime
from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense

sys.path.append('./Biz')
from dk_env import DKEnv,DDQNTrainer,DDQNSolver
env = DKEnv()
import imageio


def dk(EPISODES,STEP_MAX,render):
    action_space=env.action_space

    game_model = DDQNTrainer('donkey_kong', (1,224, 256), action_space)
    
    final = []
    run = 0
    total_step = 0
    while True:
        if run >= EPISODES:
            print("Finis les episodes")
            break

        run += 1
        current_state = env.reset()
        #im = imageio.imread(current_state[0])
        im = imageio.imread("./frame.png")
        next_state=np.dot(im[...,:3], [0.299, 0.587, 0.114])
        step = 0
        score = 0
        while True:
            if total_step >= STEP_MAX:
                print("Step maximum en tout atteint")
                return final #Je veux break de toutes les loops
            total_step += 1
            step += 1

            if render:
                env.render()

            action = game_model.move(current_state)
            #print(action)

            action =(0,1)


            next_state, reward, terminal= env.step(action)
            #im = imageio.imread(next_state)
            im = imageio.imread("./frame.png")
            next_state=np.dot(im[...,:3], [0.299, 0.587, 0.114])
            
            
            score += reward
            game_model.remember(current_state, action, reward, next_state, terminal)
            current_state = next_state

            game_model.step_update(total_step)

            if terminal:
                final.append([score, run])
                break
                
        print("Run: " + str(run) + ", tot_step: " + str(total_step) + ", score: " + str(score))
    env.bye()
    return final

results = dk(2000,400000,render=False)
import matplotlib.pyplot as plt
plt.plot(results)
plt.savefig('score_ddqn.png', bbox_inches='tight')