#Arquivo principal para rodar o bot

from screen import Screen 
from detection import Detection,Draw
from bot import RagnarokBot
import cv2 as cv
from time import time

#Parametro
DEBUG = False
THRESHOLD=0.6
OUTPUT='marker'

#Captura tela do jogo
screen = Screen('TalonRO')
gx,gy,gw,gh = screen.position()

#Detecção Monstro
detector = Detection('imagens/wormtail.png',threshold=THRESHOLD,output=OUTPUT,debug=DEBUG)

#Criar Bot
bot = RagnarokBot(gx,gy,gw,gh)

#Iniciar threads
detector.start()
bot.start()


time_start = time()
while(True):
    
    #Captura imagem da tela do jogo
    screenshot = screen.capture()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)    

    #Processa imagem e localiza monstros 
    detector.update(screenshot)
    
    #Aciona bot de acordo com a deteccao
    bot.update_targets(detector.point) 
    bot.update_screenshot(screenshot)

    
    #Se apertar 'q' então para o loop e threads (com cronometro)
    time_now= time()
    if cv.waitKey(1) == ord('q') or (time_now-time_start)>300:
        detector.stop()
        bot.stop()
        cv.destroyAllWindows()
        break
    
    #Modo Debug
    if DEBUG:
        if OUTPUT == 'rectangle':
            draw_image = Draw.rectangle(screenshot,detector.rectangle)
        else:
            draw_image = Draw.marker(screenshot,detector.point)         
        cv.imshow('Tyrr Vision',draw_image) 
    

    