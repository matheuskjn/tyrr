import cv2 as cv
from PIL import Image

IMAGENS = True

#Funcao pra ver imagem
def ver_imagem(a):
    img = Image.fromarray(a,'RGB')
    img.show()


#Parametros
imagem_objeto = 'mystcase_b1t.png'
imagem_cenario = 'xmas.png'
metodo = cv.TM_CCOEFF_NORMED
limite = 0.5

#Criar Array com as imagens
array_objeto = cv.imread(imagem_objeto)
array_cenario = cv.imread(imagem_cenario)

#Tratamento de cor das imagens
array_objeto = cv.cvtColor(array_objeto, cv.COLOR_RGB2BGR)
array_cenario = cv.cvtColor(array_cenario, cv.COLOR_RGB2BGR)

#Resultado matchTemplate
result = cv.matchTemplate(array_cenario, array_objeto, metodo)

#Melhores valores
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print('Melhor posição: %s' % str(max_loc))
print('Confiança: {:.1%}'.format(max_val))


if max_val >= limite:
    print('Objeto Localizado')  
    
    #Dimensao do objeto
    objeto_w = array_objeto.shape[1]
    objeto_h = array_objeto.shape[0]
    
    # Pontos para contruir o retangulo
    cima_esquerda = max_loc
    baixo_direita = (cima_esquerda[0] + objeto_w, cima_esquerda[1] + objeto_h)
    
    #Cria retangulos na imagem
    cv.rectangle(array_cenario, cima_esquerda, baixo_direita,color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
else:
    print('Objeto não localizado')

#Ver imagens
if IMAGENS:
    ver_imagem(array_objeto)
    ver_imagem(array_cenario)