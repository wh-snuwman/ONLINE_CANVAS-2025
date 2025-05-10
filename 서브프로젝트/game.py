import socket
from json import *
import json
import pygame
from threading import *
from random import *
from Text import *
from time import *
import colorsys
pygame.init()



def SendToServer(type=str,msg=str):
    global sc 
    msg = type + msg + "/"
    sc.sendall(f"{msg}".encode())
def DataSplit(data=str,spliter=str):
    return data.split(spliter)
def DataChange(data=str):
    if not data[0:4] == '':
        return data[0:4],data[4:len(data)]
    else:
        return None #no data 
def DataCheck(data_,check_str=str):
    if data_[0] == check_str:
        return True
    else: 
        return False
def JsonToData(data=None) -> dict:
    return loads(data)
def DataToJson(data=dict):
    return dumps(data)

class game():
    class tile():
        def __init__(self,game,w,h):
            self.game = game
            self.text = Text(screen)
            self.x = w*self.game.tileSize[0]
            self.y = h*self.game.tileSize[1]
            self.rect = pygame.Rect(self.x,self.y,self.game.tileSize[0],self.game.tileSize[1])
            self.color = (255,255,255)
            self.tileN = h+(w*self.game.mapSize[1])
            self.wLine = w
            self.hLine = h
            self.delay = 0
            SendToServer('0003',f'{DataToJson({'tileN':self.tileN})}')

            
        def update(self):
            self.rect.x = self.game.cX + self.x
            self.rect.y = self.game.cY + self.y
            self.color = self.game.map[self.tileN]

            if time() > self.delay:
                SendToServer('0003',f'{DataToJson({'tileN':self.tileN})}')
                self.delay = time() + 0.1
            
                
            if self.wLine >= 0 and self.hLine >= 0 and self.wLine < self.game.mapSize[0] and self.hLine < self.game.mapSize[1]:
                if not mousepos[0] < self.game.bar.get_width()+20 or not mousepos[1] > self.game.bar.get_height()+120:

                    if pygame.Rect(self.rect.x+self.game.tileAdj[0],self.rect.y+self.game.tileAdj[1],self.rect.w,self.rect.h).collidepoint(mousepos) and press_l:
                        SendToServer('0004',f'{DataToJson({'tileN':self.tileN,'tile':self.game.setColor})}') # set tile color
                    
                    if pygame.Rect(self.rect.x+self.game.tileAdj[0],self.rect.y+self.game.tileAdj[1],self.rect.w,self.rect.h).collidepoint(mousepos) and press_r:
                        SendToServer('0004',f'{DataToJson({'tileN':self.tileN,'tile':(255,255,255)})}') # remove tile color
                    

                if not self.color == None: 
                    pygame.draw.rect(screen,self.color,pygame.Rect(self.rect.x+self.game.tileAdj[0],self.rect.y+self.game.tileAdj[1],self.rect.w,self.rect.h),0)
                    # self.text.Writing(f'{self.tileN}',(0,0,0),(self.rect.x+15+self.game.tileAdj[0],self.rect.y+15+self.game.tileAdj[1]))

            if self.rect.centerx < 0:
                self.wLine += self.game.tileInW
                self.x += self.game.tileSize[0]*self.game.tileInW
                self.tileN += self.game.tileInW * self.game.mapSize[0]
                SendToServer('0003',f'{DataToJson({'tileN':self.tileN})}')

            if self.rect.centerx > self.game.tileSize[0]*self.game.tileInW:
                self.wLine -= self.game.tileInW
                self.x -= self.game.tileSize[0]*self.game.tileInW
                self.tileN -= self.game.tileInW * self.game.mapSize[0]
                SendToServer('0003',f'{DataToJson({'tileN':self.tileN})}')

            
            if self.rect.centery < 0:
                self.hLine += self.game.tileInH
                self.y += self.game.tileSize[1]*self.game.tileInH
                self.tileN +=  self.game.tileInH
                SendToServer('0003',f'{DataToJson({'tileN':self.tileN})}')


            if self.rect.centery > self.game.tileSize[1]*self.game.tileInH:
                self.hLine -= self.game.tileInH
                self.y -= self.game.tileSize[1]*self.game.tileInH
                self.tileN -= self.game.tileInH
                SendToServer('0003',f'{DataToJson({'tileN':self.tileN})}')

    def __init__(self):
        self.tileSize = [40,40]
        self.mapSize = [1024,1024]
        self.tileInW = round(screenW / self.tileSize[0]) + 2
        self.tileInH = round(screenH / self.tileSize[1]) + 2
        self.tiles = []
        self.map = [None for i in range(1024*1024)]
        self.tileAdj = [-self.tileSize[0],-self.tileSize[1]]
        self.cX = -(self.tileSize[0] * self.mapSize[0]) / 2 + (screenW / 2)
        self.cY = -(self.tileSize[1] * self.mapSize[1]) / 2 + (screenH / 2)
        for w in range(self.tileInW):
            for h in range(self.tileInH):
                self.tiles.append(self.tile(self,w,h))

        self.recvTh = Thread(target=self.recv,args=())
        self.recvTh.start()
        self.setColor = (29, 45, 184)
        self.mouse = pygame.image.load('img/mouse.png').convert_alpha()
        self.bar = pygame.image.load('img/bar.png').convert_alpha()
        self.colors = []
        for ii in range(20):
            for i in range(20):
                hue = i / 20
                brightness = (ii + 1) / 20
                r, g, b = colorsys.hsv_to_rgb(hue,1, brightness)
                self.colors.append((int(r * 255), int(g * 255), int(b * 255)))

    def palette(self):
        screen.blit(self.bar,(20,screenH-self.bar.get_height()-20))
        self.rects = []
        for ii in range(20):
            for i in range(20):
                self.rect = pygame.Rect(i*18 + 70, ii*18 + (screenH-18*20)-70, 18, 18)
                self.rects.append((self.colors[ii * 20 + i], self.rect))
        for i in self.rects:
            pygame.draw.rect(screen,i[0],i[1],0)
            if i[1].collidepoint(mousepos) and click_l:
                self.setColor = i[0]

    def inGame(self):
        for i in self.tiles:
            i.update()
        self.palette()
        screen.blit(self.mouse,mousepos)

    def update(self):
        self.inGame()

    def recv(self):
        global sc,run,DataSplit,DataChange,SendToServer
        self.run = True
        self.recvdata_size = 2048
        SendToServer('0001','None')
        while self.run:
            try:
                self.data = sc.recv(self.recvdata_size).decode()
            except:
                self.run = False
                run = False
                break

            if self.data == '':
                self.run = False
                run = False
                break

            self.datas = DataSplit(self.data,'/')
            if not self.data == '':
                for data in self.datas:
                    data = DataChange(data)
                    if not data == None:

                        if DataCheck(data,'0001'):
                            data = loads(data[1])
                            self.Pn = data['pn']


                        elif DataCheck(data,'0003'):
                            try:
                                data = JsonToData(data[1])
                                self.map[data['tileN']] = data['tile']

                            except json.decoder.JSONDecodeError:
                                pass   

                            


if __name__ == '__main__':
    host,port = 'snuwfield.duckdns.org',47000
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect((host, port))
    screen_adj = 1
    screenH = 1080 * screen_adj
    screenW = 1920 * screen_adj
    screen = pygame.display.set_mode((screenW,screenH),pygame.HWSURFACE)

    click_r = False
    click_l = False
    press_r = False
    press_l = False
    run = True
    movetoL = False
    movetoR = False
    movetoU = False
    movetoD = False
    moveR = 0
    moveL = 0
    moveU = 0
    moveD = 0
    mousepos = ()
    dt = 0
    movementSmoothing = 0.8
    speedRatio = 0.54
    clock = pygame.time.Clock()
    main = game()
    pygame.mouse.set_visible(False)

    while run:
        dt = clock.tick(1000)
        # fps = clock.get_fps()
        click_r = False
        click_l = False
        
        mousepos = pygame.mouse.get_pos()
        screen.fill((15, 157, 218))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_l = True
                    press_l = True
                if event.button == 3:
                    click_r = True
                    press_r = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    press_l = False
                if event.button == 3:
                    press_r = False
                
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_a:
                    movetoR = True
                if event.key == pygame.K_d:
                    movetoL = True
                if event.key == pygame.K_w:
                    movetoD = True
                if event.key == pygame.K_s:
                    movetoU = True
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_a:
                    movetoR = False
                if event.key == pygame.K_d:
                    movetoL = False
                if event.key == pygame.K_w:
                    movetoD = False
                if event.key == pygame.K_s:
                    movetoU = False
       
       
       
        if movetoU:
            moveU = speedRatio*dt
        else:
            moveU = moveU*movementSmoothing

        if movetoD:
            moveD = speedRatio*dt
        else:
            moveD = moveD*movementSmoothing

        if movetoR:
            moveR = speedRatio*dt
        else:
            moveR = moveR*movementSmoothing

        if movetoL:
            moveL = speedRatio*dt
        else:
            moveL = moveL*movementSmoothing

        main.cX -= moveL
        main.cX += moveR
        main.cY -= moveU
        main.cY += moveD

        main.update()
        pygame.display.flip()
    pygame.quit()
    SendToServer('0002','None')