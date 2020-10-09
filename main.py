from vision import Screen 
from detection import Detection,Draw
from bot import RagnarokBot
import cv2 as cv

#Parametro
DEBUG = True
threshold=0.6
output='rectangle'

#Captura tela do jogo
screen = Screen('TalonRO')
gx,gy,gw,gh = screen.position()

#Detecção Monstro
detector = Detection('imagens/wormtail.png',threshold=threshold,output=output)


#Criar Bot
bot = RagnarokBot(gx,gy,gw,gh)

#Iniciar threads
detector.start()
bot.start()
#screen.start()

while(True):
    
    #Cria imagem da tela do jogo
    screenshot = screen.capture()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)    


    #Processa imagem e localiza monstros 
    detector.update(screenshot)
    
    '''
    #Bot
    if len(detector.point)>0:
        bot.update(detector.point) 
    '''  
    #Modo Debug
    if DEBUG:
        #output = Draw.marker(screenshot,detector.point) 
        output = Draw.rectangle(screenshot,detector.rectangle) 
        cv.imshow('Tyrr Vision',output) 
    
    #Se apertar 'q' para o loop e threads
    if cv.waitKey(1) == ord('q'):
        detector.stop()
        bot.stop()
        #screen.stop()
        cv.destroyAllWindows()
        break
    