import sys
import pygame
import socket
import time
import threading
pygame.init()

"""
My idea for this is just a space invaders game sort of thing
"""


HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = "192.168.2.100"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

WIDTH, HEIGHT = (1500, 800)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space invaders LAN game")

globalBullets = []
canshootbullets = True

class player(object):
    def __init__(self):
        self.groundPadding = 30
        self.x = 100
        self.y = HEIGHT - 90 - self.groundPadding
        self.serverx = 0
        self.servery = self.y
        self.vel = 12
        self.width = 120
        self.height = 90
        self.image = pygame.transform.scale(pygame.image.load("photos/player/player.png"), (self.width, self.height))
        self.bullets = globalBullets
        self.playernum = 0
        self.terminate = False
        self.initalized = False

    def iowithserver(self):
        client.send("pos".encode(FORMAT))
        client.send(f"{self.x}, {self.y}".encode(FORMAT))
        positions = eval(client.recv(1024).decode())
        #self.x, self.y = self.getcorrectpositions(positions=positions, offset=1) # code makes game bug out a lot because of disagreement with server
        print(self.x)

    def getcorrectpositions(self, positions, offset):
        return int(positions[self.playernum * 2 - 2 + offset]), int(positions[self.playernum * 2 - 1 + offset])

    def initWithServer(self):
        if not self.initalized:
            client.send("init".encode(FORMAT))
            info = eval(client.recv(1024).decode())
            self.playernum = info[0]
            self.x, self.y = self.getcorrectpositions(info, 1)
            self.initalized = True

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def shoot(self):
        self.bullets.append(bullet(self.x, self.y, self))

    def controls(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            self.x += self.vel
        elif pressed[pygame.K_a]:
            self.x -= self.vel

        if pressed[pygame.K_w]:
            self.shoot()


class bullet(object):
    def __init__(self, xpPosition, ypPosition, p):
        self.xcurrentPosition = xpPosition + p.width / 2  # Set x to be in the middle of the player at all times
        self.ycurrentPosition = ypPosition
        self.vel = 1
        self.player = p
        self.DELAY = 1
        self.shootable = True
        self.alreadystarted = False

    def shoot(self):
        if self.shootable:
            if self.ycurrentPosition >= 0:
                self.ycurrentPosition -= self.vel
            else:
                self.player.bullets.pop(0)

    def draw(self):
        if self.shootable:
            pygame.draw.circle(win, (255, 255, 255), (self.xcurrentPosition, self.ycurrentPosition), 10)


def redrawGameWindow(win):
    win.fill((0, 0, 0))
    for bullet in globalBullets:
        bullet.shoot()
        bullet.draw()
    p.draw(win)
    pygame.display.update()


p = player()

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            p.terminate = True
            run = False
    #p.getPosFromServer()
    p.initWithServer()

    p.iowithserver()
    p.controls()
    redrawGameWindow(win)


pygame.quit()
