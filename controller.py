import time
from threading import *
from typing import *
import RPi.GPIO as g
import smbus
import callables

BUS = smbus.SMBus(1)
LCD_ADDR = 0x27
BLEN = 1 #turn on/off background light

def send(buf,f=0x05):
    buf |= f              # RS = 1, RW = 0, EN = 1
    write_word(buf)
    time.sleep(0.002)  
    write_word(buf & 0xFB)# Make EN = 0

def turn_light(key):
    global BLEN
    BLEN = key
    write_word(0x08)
 
def write_word(data):
    BUS.write_byte(LCD_ADDR,data | 0x08 if BLEN == 1 else data & 0xF7)
 
def send_commands(*comm):
    for i in comm:
        send(i&0xF0,0x04)
        send((i&0x0F)<<4,0x04)
 
def newThread(func):
    return lambda *args, **kwargs: Thread(target=func, args=args, kwargs=kwargs).start()


class LCD1602:
    def __init__(self, LineEdit: callables.LineEdit):
        self.Lines = self.mainMenu = LineEdit  # Real definenation
        self.foreverPrint()

    def print(self, y, x, data):
        if len(data) < 16:
            data += " "*(16-len(data))
        assert 0<=x<=15 and 0<=y<=1
        send_commands(0x80 + 0x40 * y + x)# Move cursor

        for chr in data:
            data=ord(chr)
            send(data & 0xF0)
            send((data & 0x0F) << 4)


    @newThread
    def foreverPrint(self) -> NoReturn:
        send_commands(0x33, 0x32, 0x28, 0x0C, 0x01)  # init the LCD device
        BUS.write_byte(LCD_ADDR,0x08)

        while True:  # foreverPrint
            time.sleep(0.1)
            lines = self.Lines.now()
            self.print(0, 0, lines[0])
            self.print(1, 0, lines[1])

    def popen(self, LineEdit, time_=1):
        self.subMenu(LineEdit)
        time.sleep(time_)
        self.Back()

    def Back(self): 
        self.Lines.VCursor=0
        self.Lines = self.Lines.parent

    def subMenu(self,subMenu:callables.LineEdit):
        self.Lines=subMenu.setParent(self.Lines)
 
    def mainmenu(self): self.Lines = self.mainMenu

    def Select(self):
        try:
            self.subMenu(self.Lines.select())
        except Exception as err:
            callables.logger.warning(err)
            self.popen(callables.noMenuPopen)

    def AskForInput(self, irc, callback):
        res = 0

        def event(KEY):
            nonlocal irc, res  
            if len(KEY)==5:res = res * 10+int(KEY[-1])
            elif KEY == "KEY_UP":self.Lines.moveUp()
            elif KEY == "KEY_DOWN":self.Lines.moveDown()
            elif KEY == "KEY_PROG2":self.Back()
            elif KEY == "KEY_PROG1":self.Lines = self.mainMenu                
            elif KEY == "KEY_OK":
                self.Back()
                irc.event = oldEvent
                callback(res)

        oldEvent = irc.event
        irc.event = event
        return callables.Inputable


class BOARD:
    def __init__(self):
        g.setmode(g.BOARD)
        self.canInputs = self.canOutput = [3, 5, 7, 29, 31, 26, 24, 21, 19, 23, 32, 33, 8, 10, 36, 11, 12, 35, 38, 40, 15, 16, 18, 22, 37, 13]  # 28 items
        self.GNDs = [6, 9, 14, 20, 25, 30, 34, 39]  # 7 items
        self.fileVolts, self.threepointthreeVolts = [2, 4], [1, 17]

    def __enter__(self,): return self
    def __exit__(self, *args): g.cleanup()

    def num(self, num, val):
        g.setup(num, val)
        return num

    def get(self, num): return g.input(self.num(num, g.IN))
    def put(self, num, val): return g.output(self.num(num, g.OUT), val)
    def PWM(self, num, freq): return g.PWM(self.num(num, g.OUT), freq)

def Input(lcd:LCD1602,irc)->str:
    Signal=True
    ans=None
    def change(res):
        nonlocal Signal,ans
        ans=res
        Signal=False
    lcd.subMenu(Text(text="Input...",select=lcd.AskForInput(irc,callback=change))())
    while Signal:
        time.sleep(0.1)
    lcd.Back()
    return ans