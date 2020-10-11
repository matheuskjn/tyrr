from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as Controller2
from time import time,sleep
from threading import Thread,Lock
from math import sqrt
import cv2 as cv

class BotState:
    INITIALIZING = 0    #Inicializando bot
    SEARCHING = 1       #Movimentacao para procurar monstros
    ATTACKING = 2       #Caso tenha monstros então clica
    COLLECTING = 3      #Coletando drop
    

class RagnarokBot:
    #Parametros
    INITIALIZING_SECONDS = 3
    IGNORE_RADIUS = 130
    SWORD_MATCH_THRESHOLD = 0.65
    HAND_MATCH_THRESHOLD = 0.8
    MOVEMENT_STOPPED_THRESHOLD = 0.975
    LOCATION_PIXEL_SPACE = 40
    stopped = True
    lock = None

    #Propriedades
    state = None
    targets = []
    screenshot = None
    timestamp = None
    movement_screenshot = None
    x = 0
    y = 0
    w = 0
    h = 0
    sword = None
    click_history = []    

    def __init__(self,x,y,w,h):
        #Informações da tela
        self.x = x
        self.y = y
        self.w = w
        self.h = h  
        self.my_pos_x = (x+w)/2
        self.my_pos_y = (y+h)/2
        #Lista com os 5 lugares para procurar item
        self.location_item = [(self.my_pos_x,self.my_pos_y),
                              (self.my_pos_x+self.LOCATION_PIXEL_SPACE,self.my_pos_y+self.LOCATION_PIXEL_SPACE),
                              (self.my_pos_x-self.LOCATION_PIXEL_SPACE,self.my_pos_y+self.LOCATION_PIXEL_SPACE),
                              (self.my_pos_x+self.LOCATION_PIXEL_SPACE,self.my_pos_y-self.LOCATION_PIXEL_SPACE),
                              (self.my_pos_x-self.LOCATION_PIXEL_SPACE,self.my_pos_y-self.LOCATION_PIXEL_SPACE)] 
        #Mouse e Teclado
        self.mouse = Controller()
        self.keyboard = Controller2()
        #Thread
        self.lock = Lock()
        #Imagem para confirmar monstro,item
        self.sword = cv.cvtColor(cv.imread('imagens/sword.png'),cv.COLOR_RGB2BGR)
        self.hand = cv.cvtColor(cv.imread('imagens/hand.png'),cv.COLOR_RGB2BGR)
        #Estado bot inicial
        self.state = BotState.INITIALIZING
        self.info = 1
        #Tempo inicial
        self.timestamp = time()

    def have_stopped_moving(self):
        #Caso a screenshot de movimento estiver nula, atualizar
        if self.movement_screenshot is None:
            self.movement_screenshot = self.screenshot.copy()
            return False

        #Compara screenshot de movimento com atual
        result = cv.matchTemplate(self.screenshot, self.movement_screenshot, cv.TM_CCOEFF_NORMED)
        #Verifica similaridade
        similarity = result[0][0]
        #Se for maior que o limite retorna true
        if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
            return True
        #Se for menor, atualiza screenshot de movimento e retorna falso
        self.movement_screenshot = self.screenshot.copy()
        return False
        
    def targets_ordered_by_distance(self, targets):
        my_pos = (self.my_pos_x,self.my_pos_y)
        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)
        targets = [t for t in targets if pythagorean_distance(t) > self.IGNORE_RADIUS]
        return targets        
    
    def confirm_sword(self, target_position):
        #Verifica se na tela temos o icone de ataque
        result = cv.matchTemplate(self.screenshot, self.sword, cv.TM_CCOEFF_NORMED)
        #Pega as informacoes 
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        #Se temos o icone na tela retorna true
        if max_val >= self.SWORD_MATCH_THRESHOLD:
            return True
        return False
   
    def pick_up_item(self):
        for i in self.location_item:
            self.mouse.position= i
            sleep(0.25)
            result = cv.matchTemplate(self.screenshot, self.hand, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val >= self.HAND_MATCH_THRESHOLD:
                self.mouse.press(Button.left)
                sleep(0.5)
                self.mouse.release(Button.left)
                print('Item pego')
                return
        print('Sem item')
        return
        
    def click_next_target(self):
        targets = self.targets_ordered_by_distance(self.targets)

        target_i = 0
        found_sword = False
        while not found_sword and target_i < len(targets):
            
            #Parar esse loop caso a thread seja parada
            if self.stopped:
                break

            # Carrega trajetos e adiciona coordenadas na tela
            target_pos = targets[target_i]
            screen_x, screen_y = self.get_screen_position(target_pos)
            print('Provavel monstro na coordenada x:{} y:{}'.format(screen_x, screen_y))
            self.mouse.position= (screen_x,screen_y) 

            #Espera um tempo
            sleep(2)
            #confirma icone de ataque no monstro
            if self.confirm_sword(target_pos):
                print('Monstro confirmado')
                print('Atacando')
                #Define que localizou monstro
                found_sword = True
                #Seleciona Skill
                self.keyboard.press('u')
                sleep(0.25)
                self.keyboard.release('u')
                #Clica
                self.mouse.press(Button.left)
                sleep(0.25)
                self.mouse.release(Button.left)
                #Salva coordenada 
                self.click_history.append(target_pos)
            #Proximo target
            target_i += 1
        #retorna se localizou monstro
        return found_sword  
   
    def get_screen_position(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)
    
    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()
    
    def start(self):
        self.stopped= False
        t = Thread(target=self.run)
        t.start()
        
    def stop(self):
        self.stopped= True
        
    def run(self):
        while not self.stopped:
            #Acoes estado INITIALIZING
            if self.state == BotState.INITIALIZING:
                #Informar uma vez
                if self.info==1 and time()-self.timestamp>1:
                    print('\nInicializando...')
                    self.info=0
                #esperar tempo de incialização
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    #Reseta Info
                    self.info=1
                    #Ir para estado de procura
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()            
            
            #Acoes estado SEARCHING
            if self.state == BotState.SEARCHING:
                #Se tem monstros perto
                if len(self.targets)>0:
                      #Reseta Info
                      self.info=1
                      #Guarda tempo
                      self.timestamp = time()
                      #Ir para estado de ataque
                      self.lock.acquire()
                      self.state = BotState.ATTACKING
                      self.lock.release()
                #Se nao tem
                else:
                    #Informar uma vez
                    if self.info==1:
                        print('Monstro não encontrado')
                        print('Procurando no mapa')
                        self.info=0  
                    #Vai para direita
                    self.mouse.position= (self.my_pos_x+100,self.my_pos_y)
                    self.mouse.press(Button.left)
                    sleep(0.25)
                    self.mouse.release(Button.left)
            
            #Acoes estado ATTACKING
            elif self.state == BotState.ATTACKING:                 
                #Procura e clica em monstros na tela
                success = self.click_next_target()

                #Se clicou no monstro
                if success:
                    #Ir para estado de coleta
                    self.lock.acquire()
                    self.state = BotState.COLLECTING
                    self.lock.release()
                #Se passou 10 segundos, não tem monstros         
                elif(len(self.targets)==0 and time()-self.timestamp>10):
                    #Então voltar para estado SEARCHING     
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()                  
                #Fica procurando
                else:
                    pass
            elif self.state == BotState.COLLECTING:  
                #Informar uma vez
                if self.info==1:
                    print('Esperando monstro morrer')
                    self.info=0  
                #Se o char parou de andar
                elif self.have_stopped_moving():
                    #Pega item
                    self.pick_up_item()
                    #Ir para estado de procura
                    self.info=1
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
                #Esperando char parar de andar
                else:
                    sleep(0.5)