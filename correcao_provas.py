import cv2
import sys

def mostrar(imagem, nome_tela='imagem'):
    cv2.imshow('imagem', imagem)
    cv2.waitKey(0)

def main():

    # tratamento de erros que podem ocorrer devido ao caminho da imagem passado

    if(len(sys.argv)<2):
        print('\n\ncompile da seguinte forma: \'python nome_do_seu_programa.py caminho_e_nome_da_imagem\'\n\n')
        return 0

    img_original = cv2.imread(sys.argv[1])

    if(img_original.any()==None):
        print('\n\nO OpenCV não conseguiu abrir a imagem. Verifique o caminho que você passou ou se a imagem existe.\n\n')
        return 0

    mostrar(img_original)
    

if __name__=='__main__':
    main()