from gamescreen import GameScreen 
from detection import Detection
from bot import RagnarokBot#,BotState
import cv2 as cv
from time import time
'''
import keyboard
def killer():
    raise KeyboardInterrupt
keyboard.add_hotkey('ctrl+shift+s', killer)  
'''
from vision import Vision
DEBUG = True

#Detecção Monstro
detector = Detection('imagens/mystcase_final.png')

#Tela do jogo
gamescreen = GameScreen('TalonRO')
gx,gy,gw,gh = gamescreen.screen_position()
#Criar Bot
bot = RagnarokBot(gx,gy,gw,gh)

#Iniciar threads
detector.start()
bot.start()


loop_time=time()
while(True):
    
    #Cria imagem da tela do jogo
    screenshot = gamescreen.capture()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)    

    #Processa imagem e localiza monstros 
    detector.update(screenshot)

    #Bot
    if len(detector.point)>0:
        bot.update(detector.point) 

    #Modo Debug
    if DEBUG:
        output = Vision.draw_marker(screenshot,detector.point) 
        cv.imshow('Tyrr Vision',output) 
        print('FPS {}'.format(1/ (time() - loop_time)))
        loop_time=time()
    if cv.waitKey(1) == ord('q'):
        detector.stop()
        bot.stop()
        cv.destroyAllWindows()
        break
    