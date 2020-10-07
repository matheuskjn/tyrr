#Essa classe � responsavel por tratar a imagem
#Usar os metodos da classe vision para detectar objetos em uma imagem
#Retornando as coordenadas x,y do objeto (point)

from threading import Thread, Lock
from vision import Vision
from hsvfilter import HsvFilter

class Detection:
    #Propriedades
    stopped = True
    lock = None
    point = []
    screenshot = None
    
    def __init__(self,object_img_path):
        #Para trancar objeto
        self.lock = Lock()
        #Cria Classe
        self.vision = Vision(object_img_path,threshold=0.15)
        #Cria filtro
        self.filter = HsvFilter(0,73,0,0,223,255,0,0,0,0)
        
    def update(self,screenshot):
        #Atualiza a imagem
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()
    
    def start(self):
        #Inicia thread
        self.stopped= False
        t = Thread(target=self.run)
        t.start()
        
    def stop(self):
        #Para thread
        self.stopped= True
        
    def run(self):
        #Enquanto stop não é chamado é para rodar
        while not self.stopped:
            #apenas continua se tiver carregado uma imagem
            if not self.screenshot is None:
                #Processa imagem com o filtro HSV
                screenshot_processed = self.vision.apply_hsv_filter(self.screenshot,self.filter)
                #Identifica os retangulos na imagem
                rect = self.vision.find(screenshot_processed) 
                #Traz as coordenadas x,y do centro dos retangulos e coloca em point
                point = self.vision.points(rect)
                #Atualiza variavel point
                self.lock.acquire()
                self.point = point
                self.lock.release()