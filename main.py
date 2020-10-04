from GameScreen import GameScreen
import cv2  as cv

img_char = cv.imread('imagens/dev_char.png',cv.IMREAD_UNCHANGED)
img_char =cv.cvtColor(img_char, cv.COLOR_BGR2BGRA)
needle_w = img_char.shape[1]
needle_h = img_char.shape[0]
while(True):
    
    screenshot = GameScreen.capture()
    
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2BGRA)
    
    result = cv.matchTemplate(screenshot, img_char, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
   
    threshold = 0.8
    if max_val >= threshold:
        top_left  = max_loc
        botton_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        cv.rectangle(screenshot, top_left, (top_left[0] + needle_w, top_left[1] + needle_h), (0, 255, 0), thickness=2, lineType =cv.LINE_4)
        cv.putText(screenshot, 'Char', (max_loc[0]+5,max_loc[1]-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (36,255,12), 2)
    cv.imshow('IA Vision',screenshot)
    
    #print('FPS {}'.format(1/ (time() - loop_time)))
    #loop_time = time()
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
    
print('Done')