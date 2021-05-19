import threading
import socket
import sys

server = "192.168.0.104" #my local IP address
port = 1612

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
        str(e)

s.listen(2) #want only 2 pp to connect to this
print("waiting for a connection, Server Started")

def readPos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def makePos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0),(100,100)]

def threaded_client(conn,player):
    conn.send(str.encode(makePos(pos[player])))
    reply = ""
    while True:
        try:
            data = readPos(conn.recv(2048).decode()) #size of information in bits
            pos[player] = data
            #reply = data.decode("utf-8") whenever we sent data btwn client and server we have to encode and decode
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1: #if player1 send player0 position
                    reply = pos[0]
                else: #if player0 send player1 position
                    reply = pos[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(makePos(reply))) #send encode reply, encode into byte obj, for security things
        except:
            break
    print("Lost connection")
    conn.close()


currentPlayer = 0

while True: #continously look for connection
    conn, addr = s.accept() #accept connection, cnn store connection, addr store ip address
    print("Connected to:", addr)
    t = threading.Thread(target=threaded_client, args=(conn, currentPlayer))
    t.start()
    #_thread.start_new_thread(threaded_client, (conn, currentPlayer)) #let thread do the threaded_client
    currentPlayer += 1