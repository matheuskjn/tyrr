#Deteccao de objetos dentro da imagem obtida no vision
#retornando as coordenadas x,y do objeto (point)

import cv2 as cv
import numpy as np
from threading import Thread, Lock

class Detection:
    #Propriedades
    stopped = True
    lock = None
    rectangle = []
    point = []
    screenshot = None
    
    #Construtor
    def __init__(self,object_img_path,method=cv.TM_CCOEFF_NORMED,threshold=0.5,EPS=0.1,output='point'):
        #Para trancar objeto
        self.lock = Lock()
        #Carrega imagem
        self.obj_img = cv.cvtColor(cv.imread(object_img_path),cv.COLOR_RGB2BGR)        
        # Salva dimensoes
        self.obj_w = self.obj_img.shape[1]
        self.obj_h = self.obj_img.shape[0]
        # Define metodo
        self.method = method
        self.threshold=threshold
        self.EPS =EPS
        #Define tipo de saida
        self.output = output
    
    #Localiza na imagem os templates e retorna os retangulos
    def find(self,screen_img):
        result = cv.matchTemplate(screen_img, self.obj_img, self.method)
        locations = np.where(result >= self.threshold)
        locations = list(zip(*locations[::-1]))
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]),int(loc[1]),self.obj_w,self.obj_h]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, 1,self.EPS)
        return rectangles
    
    #Lista de pontos no centro dos retangulos
    def points(self,rectangles):
        points= []
        for (x, y, w, h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x,center_y))      
        return points     
       
    #Atualiza screenshot
    def update(self,screenshot):
        #Atualiza a imagem
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()
    
    #Inicia thread
    def start(self):
        #Inicia thread
        self.stopped= False
        t = Thread(target=self.run)
        t.start()
    
    #Para thread
    def stop(self):
        #Para thread
        self.stopped= True
    
    #Funcoes principais da thread
    def run(self):
        #Enquanto stop não é chamado é para rodar
        while not self.stopped:
            #apenas continua se tiver carregado uma imagem
            if not self.screenshot is None:
                #Identifica os retangulos na imagem
                rectangle = self.find(self.screenshot) 
                #Traz as coordenadas x,y do centro dos retangulos e coloca em point
                if self.output == 'rectangle':
                    #Atualiza variavel retangulo
                    self.lock.acquire()
                    self.rectangle = rectangle
                    self.lock.release()
                else:    
                    point = self.points(rectangle)
                    #Atualiza variavel point
                    self.lock.acquire()
                    self.point = point
                    self.lock.release()

#Fazer desenhos na imagem
class Draw:
    #Desenha retangulo
    def rectangle(screen_img,rectangles):
         line_color = (0, 255, 0)
         line_type = cv.LINE_4
         for (x, y, w, h) in rectangles:
             top_left = (x, y)
             bottom_right = (x + w, y + h)
             cv.rectangle(screen_img, top_left, bottom_right, line_color, lineType=line_type)
         return screen_img
    
    #Desenha mira
    def marker(screen_img,points):
        marker_color = (0,255,0) 
        marker_type = cv.MARKER_CROSS   
        for (x,y) in points:
            cv.drawMarker(screen_img, (x, y), marker_color, marker_type)
        return screen_img 