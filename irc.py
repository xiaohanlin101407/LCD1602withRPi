import os
from threading import Thread
from PIL import Image
import pyqrcode


class Sensor:
    def __init__(self, event):
        self.event=event
        Thread(target=self.setup).start()
    def setup(self,):
        for i in self.mainloop():
            self.event(i)        
    def mainloop(self,):
        return


def QRCodeBytes(data: str) -> bin:
    pyqrcode.create(data).png('./code.png', scale=5, quiet_zone=0)
    im = Image.open("./code.png")
    assert im.width == im.height
    res = 0b00
    for j in range(im.height) :
        for i in range(im.width):
            res = res << 1 + im.getpixel((i, j))[0] & 0x01
    return res


import time
from lirc import LircdConnection as LC
from lirc import Client
import socket

class irC(Sensor):
    def mainloop(self):
        lastCode = None
        socket_=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client = Client(connection=LC(address="/var/run/lirc/lircd",socket=socket_,timeout = 9223372036.854775))
        r=client._connection.readline
        now_=float("-inf")
        
        while True:
            code = r().split(" ")[2]
            if lastCode == code and time.time()-now_ <= 0.2:
                continue
            else:
                lastCode = code
                now_ = time.time()
                yield code
