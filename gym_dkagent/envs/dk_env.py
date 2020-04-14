# -*- coding: utf-8 -*-
import socket
import gym


class DKEnv(gym.Env):
    """
    DonkeyKong Environment.
    """
    
    def reset():
        observation = 0
        return observation
    
    def step(action):
        observation, reward, done, info = 0
        
        return observation, reward, done, info
    
    def render(mode='human'):
        pass



class Network:
    def __init__(self, host = '127.0.0.1', port = 36297):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.connection, self.address = self.sock.accept()
        print('Network got a client at {}'.format(self.address))

    def recv(self):
        self.buffer = self.connection.recv(1024).decode()
        return self.buffer

    def send(self, msg):
        _ = self.connection.send(msg.encode())

    def close(self):
        _ = self.connection.close()
        
net = Network()
msg = ""
while msg != "exit":
    
    # We get the message from the Bizhawk client
    msg = net.recv()
    print(msg)
    
net.close()