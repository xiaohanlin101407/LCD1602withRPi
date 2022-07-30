# LCD1602withRPi
 This program provide a convenient way to use LCD1602 and lirc on Raspberry Pi.
## Usage:
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
> Q:Why (y,x),not (x,y)? A:Because y->line!(The author's weird idea!)   <br> 
&nbsp;&nbsp;&nbsp;&nbsp;`def submenu(self,LineEdit):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Just one LineEdit cannot meet the requirements of the real work.try submenu to create the submenu of the currect menu,and set its parent as the currect menu.    
&nbsp;&nbsp;&nbsp;&nbsp;`def Back(self):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;set the currect LineEdit as its parent.  
&nbsp;&nbsp;&nbsp;&nbsp;`def popen(self,LineEdit,time_):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show a popen(LineEdit),showing time=time_  
&nbsp;&nbsp;&nbsp;&nbsp;`def mainmenu(self):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Like the home button on your phone,it lets LCD1602 back to the mainmenu(the LineEdit sent in \_\_init\_\_).  
&nbsp;&nbsp;&nbsp;&nbsp;`def select(self,):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If,somehow,the LineEdit is "clicked"(selected),self.LineEdit will be set to LineEdit.cursor.select(),which means the top TextObject's LineEdit returned in its select function.  
> It can be seen as "show the submenu of the Text on the top"     
&nbsp;&nbsp;&nbsp;&nbsp;`def print(self,y,x,data):`    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print data,cursor on (x,y).Usually,it's only called in foreverprint.  
