#Aqui temos a fonte de imagens
#No caso de jogos e utilizado a captura da tela

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import numpy as np
from threading import Thread, Lock
import cv2 as cv
from Xlib.display import Display

#Funcao que retorna 
def locate_app(stack,app):
    disp = Display()
    NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
    WM_NAME = disp.intern_atom('WM_NAME') 
    name= []
    for i, w in enumerate(stack):
        win_id =w.get_xid()
        window_obj = disp.create_resource_object('window', win_id)
        for atom in (NET_WM_NAME, WM_NAME):
            window_name=window_obj.get_full_property(atom, 0)
            name.append(window_name.value)
    for l in range(len(stack)):
        if(name[2*l]==app):
            return stack[l]

class Screen:
    #Propriedades
    stopped = True
    lock = None
    screenshot = None    
    
    def __init__(self,app):
        #Para trancar objeto
        self.lock = Lock()  
        #Captura tela de acordo com o screen_id 
        self.window = Gdk.get_default_root_window()
        self.screen = self.window.get_screen()
        self.active = self.screen.get_window_stack()
        self.app = locate_app(self.active,app)
    def capture(self): 
        #Captura a tela identificada em self.active
        p = Gdk.pixbuf_get_from_window(self.app,0,0,self.app.get_geometry()[2],self.app.get_geometry()[3])   
        #Converter a imagem pixbuf em array
        w,h,c,r=(p.get_width(), p.get_height(), p.get_n_channels(), p.get_rowstride())
        assert p.get_colorspace() == GdkPixbuf.Colorspace.RGB
        assert p.get_bits_per_sample() == 8
        if  p.get_has_alpha():
            assert c == 4
        else:
            assert c == 3
        assert r >= w * c
        a=np.frombuffer(p.get_pixels(),dtype=np.uint8)
        if a.shape[0] == w*c*h:
            return a.reshape( (h, w, c) )
        else:
            b=np.zeros((h,w*c),'uint8')
            for j in range(h):
                b[j,:]=a[r*j:r*j+w*c]
            return b.reshape( (h, w, c) )
    
    def position(self):
        #Retornar a posicao da janela identificada em self.active
        #Nao esta funcionando corretamente
        x,y,w,h = self.app.get_geometry()
        return 0,32,w,h
    
    def start(self):
        #Inicia thread
        self.stopped= False
        t = Thread(target=self.run)
        t.start()
        
    def stop(self):
        #Para thread
        self.stopped= True
        
    def run(self):
        while not self.stopped:
            #Tira screenshot da tela do jogo
            screenshot = self.capture()
            #Trata imagem 
            screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) 
            #Atualiza variavel screenshot
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()