import cv2 as cv
import numpy as np


img = cv.imread('dev.png',cv.IMREAD_UNCHANGED)
img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
img_char = cv.imread('dev_char.png',cv.IMREAD_UNCHANGED)
img_char =cv.cvtColor(img_char, cv.COLOR_BGR2BGRA)
result = cv.matchTemplate(img, img_char, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

threshold = 0.8
if max_val >= threshold:
    print('Found')
    
    #get dimension
    needle_w = img_char.shape[1]
    needle_h = img_char.shape[0]
    
    top_left  = max_loc
    botton_right = (top_left[0] + needle_w, top_left[1] + needle_h)
    
    cv.rectangle(img, top_left, (top_left[0] + needle_w, top_left[1] + needle_h), (0, 255, 0), thickness=2, lineType =cv.LINE_4)
    cv.putText(img, 'Char', (max_loc[0]+5,max_loc[1]-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (36,255,12), 2)
    cv.imshow('Result',img)
    cv.waitKey()
else:
    print('Not found')