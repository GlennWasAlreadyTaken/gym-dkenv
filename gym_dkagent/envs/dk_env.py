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
        
        # Starting the server
        self.server = DKServer()
        #self.server.start()
        
        self.server.resetClient()
        
        inputMsg = ""
        while True:
            print("Enter input:")
            inputMsg = input()
            if inputMsg == "bye":
                break;
            
            direction, aButton = inputMsg.split(":")
            
            self.server.sendAction(int(direction), int(aButton))
            
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

"""
    Class responsible of creating a server for the communication
    between Bizhawk and the DK environnement.
"""
class DKServer():
    
    def __init__(self, port = 36297, num_env=-1):
        super().__init__()
        
        self.port = port
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))
        
        # We wait until only 1 connection is made.
        self.sock.listen(1) 
        
        # We accept the connection and 
        self.connection, self.address = self.sock.accept()
        print('Network got a client at {}'.format(self.address))

    # Executed when the thread is started.
    #def run(self):
        
        

    
    """
        Gets the answer sent by the 
    """
    def getAnswer(self):
        msg = self.connection.recv(1024).decode()
        self.buffer = ""
        
        if msg.startswith("DKMSG"):
            parsedMsg = msg.split(":")
            
            print(parsedMsg)
            self.buffer = msg
            # Get every needed information
            # background, objects, reward, done
        
        
        return self.buffer
    
    """
        Sends an action to the client. 
        An action consists in a direction, and whether 
        the A button is pressed or not.
        
        The action parameter is as the following:
        left -> 1
        right -> 2
        up -> 3
        down -> 4
        nothing -> every other number
        
        
        This method returns the answer of the client.
    """
    def sendAction(self, action, buttonAPressed=False):
        self.send("{}:{}\n".format(action, 1 if buttonAPressed else 0))
        
        return self.getAnswer()


    """
        Resets the client and returns its answer.
    """
    def resetClient(self):
        self.send('RESET\n')
        
        return self.getAnswer()

    """
        Sends a given message to the client.
    """
    def send(self, msg):
        _ = self.connection.send(msg.encode())

    """
        Closes the connection and kills the server process.
    """
    def close(self):
        _ = self.connection.close()
        #self.process.kill()



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