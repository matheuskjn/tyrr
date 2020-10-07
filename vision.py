#Essa classe localiza templates na imagem, localiza pontos, faz desenhos nas imagem

import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter

class Vision:
    #Constantes
    TRACKBAR_WINDOW = "Trackbars"

    #Propriedades
    obj_img = None
    obj_w = 0
    obj_h = 0
    method = None

    #Construtor
    def __init__(self, obj_img_path, method=cv.TM_CCOEFF_NORMED,threshold=0.5,EPS=0.1):
        #Carrega imagem
        self.obj_img = cv.cvtColor(cv.imread(obj_img_path),cv.COLOR_RGB2BGR)        
        # Salva dimensoes
        self.obj_w = self.obj_img.shape[1]
        self.obj_h = self.obj_img.shape[0]
        # Define metodo
        self.method = method
        self.threshold=threshold
        self.EPS =EPS

    #Localiza na imagem os templates e retorna os retangulos
    def find(self,screen_img):
        result = cv.matchTemplate(screen_img, self.obj_img, self.method)
        locations = np.where(result >= self.threshold)
        locations = list(zip(*locations[::-1]))
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]),int(loc[1]),self.obj_w,self.obj_h]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, 1,self.EPS)
        return rectangles
    
    #Lista de pontos no centro dos retangulos
    def points(self,rectangles):
        points= []
        for (x, y, w, h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x,center_y))      
        return points     
    
    #Desenha retangulo na imagem
    def draw_rect(self,screen_img,rectangles):
         line_color = (0, 255, 0)
         line_type = cv.LINE_4
         for (x, y, w, h) in rectangles:
             top_left = (x, y)
             bottom_right = (x + w, y + h)
             cv.rectangle(screen_img, top_left, bottom_right, line_color, lineType=line_type)
         return screen_img
    
    #Desenha mira na imagem de acordo com os pontos
    def draw_marker(screen_img,points):
        marker_color = (0,255,0) 
        marker_type = cv.MARKER_CROSS   
        for (x,y) in points:
            cv.drawMarker(screen_img, (x, y), marker_color, marker_type)
        return screen_img

    #GUI para analisar HSV na imagem
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)
        def nothing(position):
            pass
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)
        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    #Retorna HsvFilter de acordo com meus filtros na GUI
    def get_hsv_filter_from_controls(self):
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter

    #Aplica filtro HSV na imagem
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    #Metodo auxiliar para aplicar HSV na imagem
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c


