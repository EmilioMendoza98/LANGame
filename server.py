import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Will automatically find local ip address
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []


class playerclass():
    def __init__(self):
        self.x = 0
        self.y = 0


player1 = playerclass()
player2 = playerclass()
players = 0


def handle_client(conn, addr):
    global player1, player2, players
    player = 0
    thingToReturn = ""
    connected = True
    print(f"[CONNECTION] {addr}")
    while connected:
        if players == 0:
            player = 1
            players = 1
        elif players == 1:
            player = 2
            players = 2
        # print("41: sending playernum", player, " end")
        conn.send(str(player).encode(FORMAT))
        print(players)
        data = conn.recv(1024)
        # print("44: recieved data from client", data, " end")
        if not data:
            break
        # print(f"[COMMAND] {addr}, Command: {str(data)}")
        """if player1 is not None:
            player = 2
            player2 = playerclass()
        else:
            player = 1
            player1 = playerclass()"""

        data = data.decode(FORMAT)
        if data == "getpos":
            thingToReturn = str([player1.x, player1.y, player2.x, player2.y])
            # print("57:sending", thingToReturn, "end")
            conn.send(thingToReturn.encode())
        if data == "setpos":
            getclientpos(conn, player)
    players -= 1
    conn.close()


def getclientpos(conn, playernum):
    # print("69: sending pos to client", "pos", " end")
    conn.send("pos".encode(FORMAT))
    pos = conn.recv(1024)
    # print("69:The data recieved from client is", pos, " end")
    pos = eval(pos)
    if playernum == 1:
        player1.x = pos[0]
        player1.y = pos[1]
    else:
        player2.x = pos[0]
        player2.y = pos[1]
    print(f"Player1: {player1.x}, {player1.y}")
    try:
        print(f"Player2: {player2.x}, {player2.y}")
    except:
        print("Player2 not initalized")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()
