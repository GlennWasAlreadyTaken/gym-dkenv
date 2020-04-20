# -*- coding: utf-8 -*-
import socket

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
            parsedMsg = msg.split(":.:")
            
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