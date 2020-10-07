from pynput.mouse import Button, Controller
from time import time,sleep
from threading import Thread,Lock

mouse = Controller()

class RagnarokBot:
    stopped = True
    lock = None
    point = None  
    
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.lock = Lock()
    
    def update(self,point):
        self.lock.acquire()
        self.point = point
        self.lock.release()
    
    def start(self):
        self.stopped= False
        t = Thread(target=self.run)
        t.start()
        
    def stop(self):
        self.stopped= True
        
    def run(self):
        while not self.stopped:
            if not self.point is None:
                target_img = self.point[0]
                target_x = target_img[0]+0
                target_y = target_img[1]+self.y
                mouse.position = (target_x, target_y)
                mouse.press(Button.left)
                sleep(0.5)
                mouse.release(Button.left)
            sleep(2)