# LCD1602 with RPi
 This program provide a convenient way to use LCD1602 and lirc on Raspberry Pi.
## Usage:
### ___def newThread___
> Decorator,used if you would like to run the function by starting a new thread.
### ___class BOARD___  
&nbsp;&nbsp;&nbsp;&nbsp;`def get(self,num:int)->byte(0|1):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return the value of a pin,coded as GPIO.BOARD.  
&nbsp;&nbsp;&nbsp;&nbsp;`def put(self,num:int,val):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;put the value of a pin,coded as GPIO.BOARD.  
&nbsp;&nbsp;&nbsp;&nbsp;`def PWM(self,num:int,freq):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;set PWM for a pin(freq=freq),coded as GPIO.BOARD.  
&nbsp;&nbsp;&nbsp;&nbsp;`def mainloop(self):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;the main code of a program.If you analyze the source code of BOARD.\_\_init\_\_,you can see "self.mainloop()" at the end of it.  
  
  
### ___class LCD1602___
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self,LineEdit):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;create a LCD1602 Object.LineEdit is a class from callable,which will be mentioned later in this document.Once LCD1602 is started,its __foreverprint__ function will be called and run as a new thread.So,__DO NOT__ re-write the function,unless you know what you're doing.  
&nbsp;&nbsp;&nbsp;&nbsp;`def foreverprint(self):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;forever print self on the LCDScreen.  
&nbsp;&nbsp;&nbsp;&nbsp;`def print(self,y,x,data):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print data,cursor on (x,y).Usually,it's only called in foreverprint.  

> Q:Why (y,x),not (x,y)? A:Because y->line!(The author's weird idea!)   

&nbsp;&nbsp;&nbsp;&nbsp;`def submenu(self,LineEdit):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Just one LineEdit cannot meet the requirements of the real work.try submenu to create the submenu of the current menu,and set its parent as the current menu.    
&nbsp;&nbsp;&nbsp;&nbsp;`def Back(self):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;set the current LineEdit as its parent.  
&nbsp;&nbsp;&nbsp;&nbsp;`def popen(self,LineEdit,time_):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show a popen(LineEdit),showing time=time_  
&nbsp;&nbsp;&nbsp;&nbsp;`def mainmenu(self):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Like the home button on your phone,it lets LCD1602 back to the mainmenu(the LineEdit sent in \_\_init\_\_).  
&nbsp;&nbsp;&nbsp;&nbsp;`def Select(self,):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If,somehow,the LineEdit is "clicked"(selected),self.LineEdit will be set to LineEdit.cursor.select(),which means the top TextObject's LineEdit returned in its select function.  

> It can be seen as "show the submenu of the Text on the top"     


### ___class Outputable___
> This class is a void class,as it has no useful things.The only use of it is that every class whose objects can print on the LCD1602 should be a subclass of Outputable.Outputable lets every Outputable Class realize that `select` and `now` should be re-writed.
> However,the normal uses for `select` and `now` are as follows.
> NOTE:`run`is not neccessary for Outputable.

&nbsp;&nbsp;&nbsp;&nbsp;`def select(self) -> LineEdit:`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Usually,it's only called when it's on the top of the screen.  
&nbsp;&nbsp;&nbsp;&nbsp;`def now(self) -> str:`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return the current string.
> As the string may change(timer),the now method is neccessary.
### ___class StaticText___
> This class's object has static text.That means no matter what your HCursor is,Its `now` returns the same string,which is the one you let it to be in the \_\_init\_\_ method.
> It's so hard to change it.However,you can try obj.now=lambda :StaticText.StaticStr(yourNewString).As you can see,it's complex.

### ___class timer___
> Create an `outputable` whose `now` is the current time.

### ___class Text___
&nbsp;&nbsp;&nbsp;&nbsp;`def run(self):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It runs after `select`,but before `select` returns.

### ___class LineEdit___
&nbsp;&nbsp;&nbsp;&nbsp;`def __call__(self)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return self.  
&nbsp;&nbsp;&nbsp;&nbsp;`def setParent(self,parent)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return self,whose parent is parent.  
&nbsp;&nbsp;&nbsp;&nbsp;`def get(self,num)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return the text with the index of self.Vcursor+num viewing by the self.Hcursor  
&nbsp;&nbsp;&nbsp;&nbsp;`def now(self)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return strings which should be printed now on LCD1602.    
&nbsp;&nbsp;&nbsp;&nbsp;`def append(self,text:Text)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;add Text to be printed.   
&nbsp;&nbsp;&nbsp;&nbsp;`def moveUp(self)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;move self.VCursor up(no less than 0).   
&nbsp;&nbsp;&nbsp;&nbsp;`def moveDown(self)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;move self.VCursor down(no more than len(self.texts-1)).   
&nbsp;&nbsp;&nbsp;&nbsp;`def moveLeft(self)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;move self.HCursor left(no less than 0).   
&nbsp;&nbsp;&nbsp;&nbsp;`def moveRight(self)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;move self.HCursor right.   

### ___def FileEdit___
> Return a Text with the string of its name
> If it's a file,its `select` is a LineEdit with `Read` and `Binary Read`.If it ends with .py/.sh,`Run...` will in the list.
> If it's a folder,its `select` is a LineEdit with all of its files (and subfolders) in it.  

### Blank: a 16-space Text.
### EditSuffix: a list,its only content is StaticText("---End Of Menu--").
### noMenuPopen: usually it's a popen to tell users there's no submenu of the selected.
### Inputable: show all inputable ascii chars.
### FuncHasNoReturn: for those which do not show anything,but have functions to run,their submenus are this.
### ___def FuncText___
> return a Text that described in `FuncHasNoReturn`.

### SystemMenu: show system options.
> contains: Shutdown, Reboot, Exit.

### These are the usage of callables.py.The following classes are from system.py.This contains system interfaces that can be called by python programs.
### run: run your scripts(*.py/*.sh)
### boot: shutdown or reboot your system.
### ___def addWIFIoption___
> add the default wifi(s).

### ___def hash___
> a very strong hash function.cannot beat it.
