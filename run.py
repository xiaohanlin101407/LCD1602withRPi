from controller import *
from irc import irC


class myBOARD(BOARD):
    def mainloop(self):
        mainMenu=callables.LineEdit(texts=[
            callables.FileEdit("/home/pi/New/"),
            callables.timer,
            callables.SystemMenu,
            ])
        self.lcd = LCD1602(mainMenu)

        def event(code):
            callables.logger.info(f"code {code} pressed")
            if code == "KEY_UP":
                self.lcd.Lines.moveUp()
            elif code == "KEY_DOWN":
                self.lcd.Lines.moveDown()
            elif code == "KEY_OK":
                self.lcd.Select()
            elif code == "KEY_PROG2":
                self.lcd.Back()
            elif code == "KEY_PROG1":
                self.lcd.mainmenu()
            elif code == "KEY_LEFT":
                self.lcd.Lines.moveLeft()
            elif code=="KEY_RIGHT":
                self.lcd.Lines.moveRight()
        irc = irC(event)
        self.lcd.Lines.append(callables.Text("Input...",select=lambda:self.lcd.AskForInput(irc,lambda sth:print(sth))))

myBOARD().mainloop()
