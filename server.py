import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Will automatically find local ip address
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []


class playerclass():
    def __init__(self):
        self.x = 0
        self.y = 800 - 90 - 30
        self.disconnected = False


player1 = playerclass()
player2 = playerclass()
totalPlayers = 0


def handle_client(conn, addr):
    global player1, player2, totalPlayers
    player = 1
    thingToReturn = ""
    initialized = False
    connected = True
    print(f"[CONNECTION] {addr}")
    while connected:
        print(totalPlayers)
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode(FORMAT)
        if data == "pos":
            clientpos = eval(conn.recv(1024).decode())
            conn.send(f"{player}, {player1.x}, {player1.y}, {player2.x}, {player2.y}".encode(FORMAT))
            if player == 1:
                player1.x = clientpos[0]
                player1.y = clientpos[1]
            else:
                player2.x = clientpos[0]
                player2.y = clientpos[1]
        if data == "init":
            if player == 1 and totalPlayers == 0:
                player = totalPlayers + 1
                totalPlayers += 1
            else:
                player = totalPlayers + 1
                totalPlayers = 2

            conn.send(f"{player}, {player1.x}, {player1.y}, {player2.x}, {player2.y}".encode(FORMAT))
        if data == "DISCONNECT":
            connected = False
        print(f"Player1 : {player1.x}, {player1.y}\n"
              f"Player2 : {player2.x}, {player2.y}")
    totalPlayers -= 1
    print(f'[CONNECTION CLOSED] BY:{addr}')
    conn.close()


def start():
    server.listen(2)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()
