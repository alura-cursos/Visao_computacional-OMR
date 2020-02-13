import cv2
import sys
import numpy as np

def abrir_imagem(img_caminho):

    imagem = cv2.imread(img_caminho)

    if(imagem is None):
        raise NameError('\nO OpenCV não conseguiu abrir a imagem. Verifique o caminho que você passou ou se a imagem existe.\n')

    return imagem

def mostrar(imagem, nome_tela='imagem'):
    cv2.namedWindow('imagem', cv2.WINDOW_NORMAL)
    cv2.imshow('imagem', imagem)
    while(cv2.waitKey(1)!=27):
        pass

def hough_para_cartesiano(raio, theta):

    seno = np.cos(theta)
    cosseno = np.sin(theta)

    x = seno*raio
    y = cosseno*raio

    return (x, y)

def criar_linhas(pontos, theta):

    seno = np.cos(theta)
    cosseno = np.sin(theta)

    x1 = int(pontos[0] + 10000*(-cosseno))

    y1 = int(pontos[1] + 10000*(seno))

    x2 = int(pontos[0] - 800*(-cosseno)) 

    y2 = int(pontos[1] - 800*(seno)) 

    return x1, y1, x2, y2


def main():


    img_original = abrir_imagem(sys.argv[1])

    img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

    # Algoritmo de otsu
    thres, img_binarizada = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #Aplicação de um filtro de gradiente para extração de bordas
    # Lembrando que o filtro de canny já faz a suavização
    canny = cv2.Canny(img_binarizada, 100,200)

    # Operações morfológicas: Operação para destacar linhas horizontais e verticais e operação Closing


    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
    operacao_cross = cv2.morphologyEx(canny, cv2.MORPH_CROSS, kernel_cross, iterations=1)
    kernel_closing = np.ones((5, 5),np.uint8)
    operacao_closing = cv2.morphologyEx(operacao_cross, cv2.MORPH_CROSS, kernel_closing, iterations=3)

    kernel_erosao = cv2.getStructuringElement(cv2.MORPH_ERODE, (3,3))
    operacao_closing = cv2.morphologyEx(operacao_cross, cv2.MORPH_ERODE, kernel_erosao, iterations=1)

    mostrar(operacao_closing)
    # Encontrar linhas com o algoritmo de hough
    l_linhas = cv2.HoughLines(operacao_closing,1,np.pi/180, 80)
    bounding_box = np.zeros(shape=(2,2)) # [[0., 0].       SUPERIOR-ESQUERDO (x,y)
                                        #   [0., 0.]]      INFERIOR-DIREITO  (x,y)

    for linha in l_linhas:
        for raio,theta in linha:

            # Remove todas as linhas que não sejam horizontais
            if(theta>0.001 and (theta<0.999*(np.pi/2.0) or theta>1.001*(np.pi/2.0))):
                continue

            x, y = hough_para_cartesiano(raio, theta)
            x1,y1,x2,y2 = criar_linhas((x,y), theta)

            if (y>bounding_box[0][1] and bounding_box): # bounding_box[0][1] = y superior esquerdo
                bounding_box

            if(np.isclose(theta,0.0)):
                cv2.line(img_original,(x1,y1), (x2,y2), (0,0,255),2)
            else:
                cv2.line(img_original,(x1,y1), (x2,y2), (0,255, 0),2)

    mostrar(img_original)


if __name__=='__main__':

    if(len(sys.argv)!=2):
        print('\n\ncompile da seguinte forma: \'python nome_do_seu_programa.py caminho_e_nome_da_imagem\'\n\n')
        sys.exit(0)

    try:
        main()
    except NameError as e:
        print(e)