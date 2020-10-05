from gamescreen import GameScreen 
from vision import Vision
from hsvfilter import HsvFilter
import cv2 as cv


#Monstros procurados
mystcase = Vision('imagens/mystcase_final.png')

#Filtro de imagem
hsv_filter = HsvFilter(0,73,0,0,223,255,0,0,0,0)


while(True):
    
    #Carrega tela do jogo
    screenshot = GameScreen.capture()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) 
    
    #Processa imagem e localiza monstros 
    screenshot_processed = mystcase.apply_hsv_filter(screenshot,hsv_filter)
    rect=mystcase.find(screenshot_processed,threshold=0.12)
    point = mystcase.points(rect)
    
    #Desenha os pontos no mapa
    output = mystcase.draw_marker(screenshot,point)   

    cv.imshow('Tyrr Vision',output)    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
