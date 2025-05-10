import socketserver
from Log import *
from json import *
import json
from time import *

HOST,PORT = '0.0.0.0',47000
User = {}
Pn = 0
Map = []
map_size = [1024,1024]

'''
유저는 아래의 데이터 형식에 따라서 저장된다.
Pn = Player Number

0001<msg>/ = player number recv/send
0002<msg>/ = player left recv/send
0003<msg>/ = map data send/recv
0004<msg>/ = map change
0005<msg>/ = 
0006<msg>/ = 
0007<msg>/ = 
0008<msg>/ = 

'''

def DataSplit(data=str,spliter=str) -> list:
    data = data.split(spliter)
    d_list = [] # data list
    for d in data:
        if not d == '':
            d_list.append(d)
    return d_list
def DataToJson(data=dict):
    return dumps(data)
def JsonToData(data=None) -> dict:
    return loads(data)
def SendToAll(type=str,msg=str,exep=None):
    try:
        for user in User:
            if not exep == None:
                if not exep == user:
                    User[user]['socket'].sendall(f'{type}{msg}/'.encode())
                else:pass
            else:
                User[user]['socket'].sendall(f'{type}{msg}/'.encode())
    except ConnectionResetError:
        pass
def Join(Pn_=int,socket=None):
    global Pn
    User[Pn_] = {'name':str,'pos':tuple,'motion':None,'socket':socket}
    printlog("INFO",f"someone is join(Join)")
    Pn += 1
def Left(Pn_=int):  
    SendToAll('0002',f'{DataToJson({'pn':Pn_})}')
    del User[Pn_]
    printlog("INFO",f"someone is left(Left)")
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
def SendToClient(type=str,msg=str,target=None) -> str:
    try:
        User[target]['socket'].sendall(f"{type}{msg}/".encode())
    except OSError:
        del User[target]
        printlog("INFO",f"someone is disconnect(SendToClient)")
    return f"{type}{msg}/"



class myTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global Pn
        self.Pn = Pn
        Join(self.Pn,self.request)
        self.run = True
        self.recvdata_size = 2048
        try:
            while self.run:
                data = self.request.recv(self.recvdata_size).decode()
                if data == '':
                    break
                datas = DataSplit(data,"/")
                if not data == '':
                    for data in datas:
                        data = DataChange(data)
                        if not data == None:
                            if DataCheck(data,'0001'):
                                SendToClient('0001',f'{DataToJson({'pn':self.Pn})}',self.Pn)
                            
                            elif DataCheck(data,'0002'):
                                self.run = False
                                break

                            elif DataCheck(data,'0003'):
                                try:
                                    data = JsonToData(data[1])
                                    SendToClient('0003',f'{DataToJson({'tile':Map[data['tileN']],'tileN':data['tileN']})}',self.Pn)
                                except json.decoder.JSONDecodeError:
                                    pass

                            elif DataCheck(data,'0004'):
                                try:
                                    data = JsonToData(data[1])
                                    Map[data['tileN']] = data['tile']
                                    SendToClient('0003',f'{DataToJson({'tile':Map[data['tileN']],'tileN':data['tileN']})}',self.Pn)
                                except json.decoder.JSONDecodeError:
                                    pass

        except ConnectionResetError:
            pass
        
        Left(self.Pn)



class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

if __name__ == '__main__':


    for i in range(map_size[0]*map_size[1]):
        Map.append((255,255,255))

    with ThreadedTCPServer((HOST,PORT),myTcpHandler) as server:
        printlog('INFO',f'server is runing on {HOST},{PORT}')
        server.serve_forever()