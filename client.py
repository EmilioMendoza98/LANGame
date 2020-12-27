import sys
import pygame
import socket
pygame.init()

"""
My idea for this is just a space invaders game sort of thing
"""


HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

WIDTH, HEIGHT = (1500, 800)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space invaders LAN game")


class player(object):
    def __init__(self):
        self.groundPadding = 30
        self.x = 0
        self.y = HEIGHT - 90 - self.groundPadding
        self.serverx = 0
        self.servery = 0
        self.vel = 12
        self.width = 120
        self.height = 90
        self.image = pygame.transform.scale(pygame.image.load("photos/player/player.png"), (self.width, self.height))
        self.bullets = []
        self.playernum = 0

    def getPosFromServer(self):
        playernum = client.recv(1024).decode(FORMAT)
        self.playernum = playernum
        message = "getpos".encode(FORMAT)
        client.send(message)
        pos = client.recv(4096).decode(FORMAT)
        
        pos = eval(pos)
        if self.playernum == 1:
            self.serverx = pos[0]
            self.servery = pos[1]
        else:
            self.serverx = pos[2]
            self.servery = pos[3]

    def setglobalpos(self):
        pos = ""
        playernum = client.recv(1024).decode(FORMAT)
        self.playernum = playernum
        client.send("setpos".encode(FORMAT))
        tmp = client.recv(1024).decode(FORMAT)
        
        pos = eval(tmp)
        client.send(str((self.x, self.y)).encode(FORMAT))
        #print(pos)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def shoot(self):
        self.bullets.append(bullet(self.x, self.y, self, len(self.bullets) - 1))

    def controls(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            self.x += self.vel
        elif pressed[pygame.K_a]:
            self.x -= self.vel

        if pressed[pygame.K_w]:
            self.shoot()


class bullet(object):
    def __init__(self, xpPosition, ypPosition, p, indexPos):
        self.xcurrentPosition = xpPosition + p.width / 2  # Set x to be in the middle of the player at all times
        self.ycurrentPosition = ypPosition
        self.vel = 1
        self.player = p
        self.indexPos = indexPos

    def shoot(self):
        if self.ycurrentPosition >= 0:
            self.ycurrentPosition -= self.vel
        else:
            self.player.bullets.pop(0)

    def draw(self):
        pygame.draw.circle(win, (255, 255, 255), (self.xcurrentPosition, self.ycurrentPosition), 10)


def redrawGameWindow(win):
    win.fill((0, 0, 0))
    for bullet in p.bullets:
        bullet.shoot()
        bullet.draw()
    p.draw(win)
    pygame.display.update()


p = player()

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(6000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #p.getPosFromServer()
    p.controls()
    p.getPosFromServer()
    p.setglobalpos()
    redrawGameWindow(win)

pygame.quit()