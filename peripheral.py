#Controle dos perifericos 
from pynput.mouse import Button, Controller as Controller_Mouse
from pynput.keyboard import Controller as Controller_Keyboard
from time import sleep


#Mouse
class Mouse:
    def __init__(self):
        self.mouse = Controller_Mouse()
    def click_left(self):
        self.mouse.press(Button.left)
        sleep(0.25)
        self.mouse.release(Button.left)        
    def click_right(self):
        self.mouse.press(Button.right)
        sleep(0.25)
        self.mouse.release(Button.right)        
    def move_instant(self,x):
        self.mouse.position= x #x =(coord x, coord y)


#Teclado
class Keyboard:
    def __init__(self):
        self.keyboard = Controller_Keyboard()
    def press(self,key):
        self.keyboard.press(key)
        sleep(0.25)
        self.keyboard.release(key)
        
        
       