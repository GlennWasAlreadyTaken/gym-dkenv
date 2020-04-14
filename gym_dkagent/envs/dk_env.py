# -*- coding: utf-8 -*-
import socket
import gym
import threading

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
        pass
    
    def reset(self):
        observation = 0
        return observation
    
    def step(self, action):
        observation, reward, done, info = 0
        
        return observation, reward, done, info
    
    def render(self, mode='human'):
        pass

"""
    Class responsible of creating a server for the communication
    between Bizhawk and the DK environnement.
"""
class DKServer(threading.Thread):
    
    def __init__(self, port = 36297, num_env=-1):
        super().__init__()
        
        self.port = port + num_env
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))

    # Executed when the thread is started.
    def run(self):
        # We wait until only 1 connection is made.
        self.sock.listen(1) 
        
        # We accept the connection and 
        self.connection, self.address = self.sock.accept()
        print('Network got a client at {}'.format(self.address))

    def recv(self):
        self.buffer = self.connection.recv(1024).decode()
        return self.buffer

    def send(self, msg):
        _ = self.connection.send(msg.encode())

    def close(self):
        _ = self.connection.close()

"""
net = Network()
msg = ""
while msg != "exit":
    
    # We get the message from the Bizhawk client
    msg = net.recv()
    print(msg)
    
net.close()
"""