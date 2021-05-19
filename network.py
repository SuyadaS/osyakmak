import socket

class Network: #class responsible for connecting the server
    def __init__(self): #define initialization function
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.104"
        self.port = 1612
        self.addr = (self.server, self.port)
        self.pos = self.connect() 
        print(self.pos)

    def connect(self):
        try:
            self.client.connect(self.addr) #connect to server
            return self.client.recv(2048).decode() #when connected server will send "Connected" back, so we receive here
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def getPos(self):
        return self.pos
    
n = Network()

print(n.send("hello"))
print(n.send("working"))