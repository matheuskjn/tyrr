from vision import Screen 
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
detector = Detection('imagens/wormtail.png',threshold=THRESHOLD,output=OUTPUT)

#Criar Bot
bot = RagnarokBot(gx,gy,gw,gh)

#Iniciar threads
detector.start()
bot.start()


time_start = time()
while(True):
    
    #Cria imagem da tela do jogo
    screenshot = screen.capture()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)    

    #Processa imagem e localiza monstros 
    detector.update(screenshot)
    
    #Bot
    bot.update_targets(detector.point) 
    bot.update_screenshot(screenshot)
    #Modo Debug
    if DEBUG:
        if OUTPUT == 'rectangle':
            draw_image = Draw.rectangle(screenshot,detector.rectangle)
        else:
            draw_image = Draw.marker(screenshot,detector.point) 
         
        cv.imshow('Tyrr Vision',draw_image) 
    
    time_now= time()
    #Se apertar 'q' para o loop e threads
    if cv.waitKey(1) == ord('q') or (time_now-time_start)>120:
        detector.stop()
        bot.stop()
        cv.destroyAllWindows()
        break
    