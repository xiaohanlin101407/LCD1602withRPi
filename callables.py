from system import *
from string import *
import time
from typing import *
from loguru import logger
class Outputable:
    def now(self):
        return 
    def select(self):
        return 
class timer(Outputable):
    def select(): return None
    def now(): return time.strftime('%m%d %H%M%S', time.localtime(time.time()))

class StaticText(Outputable):
    class staticStr:
        def __init__(self,text):
            self.text=text
        def __getitem__(self,*args):
            return self.text
    def __init__(self,text):
        self.now=lambda:self.staticStr(text)

class Text(Outputable):
    def __init__(self, text, select=None, run=lambda: None):
        #TODO:fix it,this is too complex!
        logger.info(f"creating Text Obj with text:{text},select={select}")
        self.now = lambda: text
        self.select_ =  select         
        self.run = run


    def __call__(self):
        return LineEdit(self.now())

    def select(self):
        logger.info(f"text {self.now()} selected")
        self.run()
        return self.select_()


class LineEdit:
    # Basic Funcs
    def __init__(self, texts: List[Text], parent=None):
        if isinstance(texts, str):
            texts = [Text(i)for i in texts.splitlines()]#[Text(texts[i:i+16]) for i in range(0, len(texts), 16)]
        logger.info(f"creating LineEdit with texts:{texts}")
        self.VCursor = 0
        self.HCursor = 0
        self.parent = parent if parent else self
        self.texts = texts+EditSuffix

    def __call__(self): return self

    def setParent(self, parent):
        self.parent = parent
        return self
    def get(self,num=0):
        return self.texts[self.VCursor+num].now()[self.HCursor:self.HCursor+16]
    def select(self):
        return self.texts[self.VCursor].select()
    # action funcs
    def now(self): return self.get(), (self.get(1) if len(self.texts) >= self.VCursor+2 else Blank)

    def append(self, text) -> None:self.texts.insert(-1, text)

    # event funcs
    def moveUp(self): self.VCursor = max(self.VCursor-1, 0)  # [0,maxlen-1)
    def moveDown(self): self.VCursor = min(self.VCursor+1, len(self.texts)-2)
    def moveLeft(self): self.HCursor = max(self.HCursor-1, 0)
    def moveRight(self): self.HCursor = self.HCursor+1
    
    
def list2LineEdit(texts) -> LineEdit:
    return LineEdit([Text(i) if not isinstance(i, Text) else i for i in texts])


def FileEdit(filepath: str, baseDir="") -> Text:
    def Read(filepath_):
        try:
            res = open(filepath_, "r", encoding="ascii").read()
        except:
            res = "raspi cannot encode this file with ascii"
        return LineEdit(res)

    def BinaryRead(filepath_):
        res = ""
        for i in open(filepath_, "rb").read():
            res += hex(int(i))[2:]
        return LineEdit(res)

    file = baseDir+filepath
    if os.path.isfile(file):
        texts = [Text("Read", select=lambda:Read(file)), Text("Binary Read", select=lambda:BinaryRead(file))]

        if file.endswith(".py"):
            texts += [FuncText("Run...",lambda:run.python(file))]
        elif file.endswith(".sh"):
            texts += [FuncText("Run...",lambda:run.bash(file))]
        
        return Text(filepath, select=LineEdit(texts))

    elif os.path.isdir(file):
        if not file.endswith("/"):
            file += "/"
        return Text(filepath, select=LineEdit([FileEdit(i, file) for i in os.listdir(file)]))

    raise ValueError([filepath, baseDir])




Blank = Text(" "*16)
EditSuffix = [StaticText("---End Of Menu--")]
noMenuPopen = list2LineEdit(["No Sub Menu", "Sending back..."])
Inputable=LineEdit(texts=digits + ascii_letters + punctuation + " \\n")
FuncHasNoReturn = LineEdit("This Func Has NoReturn\nBut Executed")

def FuncText(text,run):
    return Text(text,select=FuncHasNoReturn,run=run)

SystemMenu = Text("System", select=LineEdit(
    texts=[FuncText("Shutdown", run=boot.shutdown),
           FuncText("Reboot",run=boot.reboot),
           FuncText("Exit",run=lambda:os._exit(0))]))

