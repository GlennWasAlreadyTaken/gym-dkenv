# -*- coding: utf-8 -*-
import gym
import threading
import random
from dk_server import DKServer
import os
import subprocess
from gym import spaces



class DKEnv(gym.Env):
    """
    DonkeyKong Environment.
    
    Observation: 
        * Background of the level
        * Objects in the level
        
    Actions:
        Type: MultiDiscrete([ 4, 2])
        Num	Action
        0	Left
        1	Right
        2   Up
        3   Down
        0   A Button
        1   B Button
    Reward:
        ?
    Episode Termination:
        Level finished
    """
    
    
    def __init__(self):
        self.action_space=spaces.MultiDiscrete([ 4, 2])

        print(os.getcwd())
        print("emulator launch from env")
        subprocess.Popen([r""+os.getcwd()+"\Biz\EmuHawk.exe","--luaconsole"])
        #os.startfile(os.getcwd()+"\Biz\EmuHawk.exe",args="--luaconsole")
        #subprocess.call([os.getcwd()+"\Biz\EmuHawk.exe", "--luaconsole"])
        print("emulator launched from env")
        # Starting the server
        self.server = DKServer()
        #self.server.start()
        
        self.server.resetClient()
        print("bye")
        
       
        
    
    def reset(self):
        observation = self.server.resetClient()
        return observation
    
    def step(self, action):
        answer = self.server.sendAction(action[0], action[1])
        observation,reward,done=answer
        return str(observation), float(reward), int(done)
    
    def render(self, mode='human'):
        pass

    def bye(self):
        self.server.resetClient()
        self.server.close()
        print("close serv connection from env")

import numpy as np
import os
import random
import shutil
from statistics import mean
from datetime import datetime
from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense

GAMMA = 0.99
MEMORY_SIZE = 900000
BATCH_SIZE = 32
TRAINING_FREQUENCY = 4
TARGET_NETWORK_UPDATE_FREQUENCY = 40000
MODEL_PERSISTENCE_UPDATE_FREQUENCY = 50#10000
REPLAY_START_SIZE = 500#50000

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.1
EXPLORATION_TEST = 0.02 
EXPLORATION_STEPS = 850000
EXPLORATION_DECAY = (EXPLORATION_MAX-EXPLORATION_MIN)/EXPLORATION_STEPS


class DDQNGameModel():

    def __init__(self, game_name, mode_name, input_shape, action_space, logger_path, model_path):
        self.action_space = action_space
        self.input_shape = input_shape
        self.model_path = model_path
        
        #Section Modele neural network
        self.model = Sequential()
        self.model.add(Conv2D(32,
                              8,
                              strides=(4, 4),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.model.add(Conv2D(64,
                              4,
                              strides=(2, 2),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.model.add(Conv2D(64,
                              3,
                              strides=(1, 1),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.model.add(Flatten())
        self.model.add(Dense(512, activation="relu"))
        self.model.add(Dense(4*2))
        self.model.compile(loss="mean_squared_error",
                           optimizer=RMSprop(lr=0.00025,
                                             rho=0.95,
                                             epsilon=0.01),
                           metrics=["accuracy"])
        #self.model.summary()
        
        self.ddqn = self.model
        
        
        
        if os.path.isfile(self.model_path):
            self.ddqn.load_weights(self.model_path)

    def _save_model(self):
        self.ddqn.save_weights(self.model_path)

        
        
        
        
        

class DDQNSolver(DDQNGameModel):

    def __init__(self, game_name, input_shape, action_space):
        testing_model_path = "./output/neural_nets/" + game_name + "/ddqn/testing/model.h5"
        assert os.path.exists(os.path.dirname(testing_model_path)), "No testing model in: " + str(testing_model_path)
        DDQNGameModel.__init__(self,
                               game_name,
                               "DDQN testing",
                               input_shape,
                               action_space,
                               "./output/logs/" + game_name + "/ddqn/testing/" + str(datetime.now().strftime('%Y-%m-%d_%H-%M')) + "/",
                               testing_model_path)

    def move(self, state):
        if np.random.rand() < EXPLORATION_TEST:
            return self.action_space.sample()
        q_values = self.ddqn.predict(np.expand_dims(np.asarray(state).astype(np.float64), axis=0), batch_size=1)
        return np.argmax(q_values[0])


    
    

class DDQNTrainer(DDQNGameModel):

    def __init__(self, game_name, input_shape, action_space):
        DDQNGameModel.__init__(self,
                               game_name,
                               "DDQN training",
                               input_shape,
                               action_space,
                               "./output/logs/" + game_name + "/ddqn/training/" + str(datetime.now().strftime('%Y-%m-%d_%H-%M')) + "/",
                               "./output/neural_nets/" + game_name + "/ddqn/" + str(datetime.now().strftime('%Y-%m-%d_%H-%M')) + "/model.h5")

        if os.path.exists(os.path.dirname(self.model_path)):
            shutil.rmtree(os.path.dirname(self.model_path), ignore_errors=True)
        os.makedirs(os.path.dirname(self.model_path))

        #Section Modele neural network
        self.target_model = Sequential()
        self.target_model.add(Conv2D(32,
                              8,
                              strides=(4, 4),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.target_model.add(Conv2D(64,
                              4,
                              strides=(2, 2),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.target_model.add(Conv2D(64,
                              3,
                              strides=(1, 1),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.target_model.add(Flatten())
        self.target_model.add(Dense(512, activation="relu"))
        self.target_model.add(Dense(4*2))
        self.target_model.compile(loss="mean_squared_error",
                           optimizer=RMSprop(lr=0.00025,
                                             rho=0.95,
                                             epsilon=0.01),
                           metrics=["accuracy"])
        #self.model.summary()
        
        self.ddqn_target = self.target_model
        self._reset_target_network()
        self.epsilon = EXPLORATION_MAX
        self.memory = []

    def move(self, state):
        if np.random.rand() < self.epsilon or len(self.memory) < REPLAY_START_SIZE:
            return self.action_space.sample()
        q_values = self.ddqn.predict(np.expand_dims(np.asarray(state).astype(np.float64), axis=0), batch_size=1)
        return np.argmax(q_values[0])

    def remember(self, current_state, action, reward, next_state, terminal):
        
        #print("state "+str(current_state)+"\naction "+str(action)+"\nreward "+str(reward)+"\nnext state "+str(next_state)+str(terminal))
        self.memory.append({"current_state": current_state,
                            "action": action,
                            "reward": reward,
                            "next_state": next_state,
                            "terminal": terminal})
        if len(self.memory) > MEMORY_SIZE:
            self.memory.pop(0)

    def step_update(self, total_step):
        if len(self.memory) < REPLAY_START_SIZE:
            return

        if total_step % TRAINING_FREQUENCY == 0:
            loss, accuracy, average_max_q = self._train()
            #add comment les loggers
            #self.logger.add_loss(loss)
            #self.logger.add_accuracy(accuracy)
            #self.logger.add_q(average_max_q)

        self._update_epsilon()

        if total_step % MODEL_PERSISTENCE_UPDATE_FREQUENCY == 0:
            print("on save")
            self._save_model()

        if total_step % TARGET_NETWORK_UPDATE_FREQUENCY == 0:
            self._reset_target_network()
            print('{{"metric": "epsilon", "value": {}}}'.format(self.epsilon))
            print('{{"metric": "total_step", "value": {}}}'.format(total_step))

    def _train(self):
        batch = np.asarray(random.sample(self.memory, BATCH_SIZE))
        if len(batch) < BATCH_SIZE:
            return

        current_states = []
        q_values = []
        max_q_values = []

        for entry in batch:
            current_state = np.expand_dims(np.asarray(entry["current_state"]).astype(np.float64), axis=0)
            #added
            #current_state = np.expand_dims(current_state, axis=0)
            
            
            
            current_states.append(current_state)
            next_state = np.expand_dims(np.asarray(entry["next_state"]).astype(np.float64), axis=0)
            #added
            #next_state = np.expand_dims(next_state, axis=0)
            
            #added expand dims
            next_state_prediction = self.ddqn_target.predict(np.expand_dims(next_state,axis=0)).ravel()
            next_q_value = np.max(next_state_prediction)
            #added expand dims
            q = list(self.ddqn.predict(np.expand_dims(current_state,axis=0))[0])
            if entry["terminal"]:
                q[entry["action"]] = entry["reward"]
            else:
                q[entry["action"]] = entry["reward"] + GAMMA * next_q_value
            q_values.append(q)
            max_q_values.append(np.max(q))

        
        #add remove squeeze()
        fit = self.ddqn.fit(np.asarray(current_states),
                            np.asarray(q_values),
                            batch_size=BATCH_SIZE,
                            verbose=0)
        loss = fit.history["loss"][0]
        #add acc to accuracy
        accuracy = fit.history["accuracy"][0]
        return loss, accuracy, mean(max_q_values)

    def _update_epsilon(self):
        self.epsilon -= EXPLORATION_DECAY
        self.epsilon = max(EXPLORATION_MIN, self.epsilon)

    def _reset_target_network(self):
        self.ddqn_target.set_weights(self.ddqn.get_weights())

