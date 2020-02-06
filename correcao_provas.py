import cv2
import sys

def mostrar(imagem, nome_tela='imagem'):
    cv2.imshow('imagem', imagem)
    cv2.waitKey(0)

def main():

    # tratamento de erros que podem ocorrer devido ao caminho da imagem passado

    if(len(sys.argv)!=2):
        print('\n\ncompile da seguinte forma: \'python nome_do_seu_programa.py caminho_e_nome_da_imagem\'\n\n')
        return 0

    img_original = cv2.imread(sys.argv[1],0)

    if(img_original is None):
        print('\n\nO OpenCV não conseguiu abrir a imagem. Verifique o caminho que você passou ou se a imagem existe.\n\n')
        return 0

    mostrar(img_original)

    img_suavizada = cv2.GaussianBlur(img_original, (5,5), 0)
    img_binarizada, thres = cv2.threshold(img_suavizada, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    operacao_closing = cv2.morphologyEx(img_binarizada, cv2.MORPH_CLOSE, (5,5))
    print(operacao_closing.shape)
    mostrar(operacao_closing)

if __name__=='__main__':
    main()