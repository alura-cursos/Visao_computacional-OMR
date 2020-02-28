import cv2
import sys
import numpy as np
import math

QTD_QUESTOES = 21 # Quantidade de questões+1
QTD_ALTERNATIVAS = 5 # Quantidade de alternativas+1

def abrir_imagem(img_caminho):
    '''
    Entrada: String com o caminho da imagem
    Saída: Matriz da imagem
    '''
    imagem = cv2.imread(img_caminho)

    if(imagem is None):
        raise NameError('\nO OpenCV não conseguiu abrir a imagem. Verifique o caminho que você passou ou se a imagem existe.\n')

    return imagem

def mostrar(imagem, nome_tela='imagem'):
    '''
    Entrada: Matriz da imagem e opcional o nome da janela a ser mostrada
    Saída: mostra imagem na tela até a tecla ESC ser apertada
    '''
    cv2.namedWindow(nome_tela, cv2.WINDOW_NORMAL)
    cv2.imshow(nome_tela, imagem)
    while(cv2.waitKey(1)!=27):
        pass

def hough_para_cartesiano(raio, theta):
    '''
    Transformação do espaço de cordenadas polar para o cartesiana

    Entrada: raio e o ângulo theta que o raio faz com a horizontal
    Saída: pontos (x,y)
    '''
    cosseno = math.cos(theta)
    seno = math.sin(theta)

    x = cosseno*raio
    y = seno*raio

    return (x, y)

def criar_linhas(pontos, theta):

    '''
    Gera linhas para dados o ponto e o raio da reta que vai de (0,0) até o ponto indicado

    Entrada: Ponto e o ângulo do raio com a horizontal
    Saída: 4 valores correspondendo a 2 pontos (x,y)
    '''

    seno = np.sin(theta)
    cosseno = np.cos(theta)

    x1 = int(pontos[0] + 10000*(-seno))

    y1 = int(pontos[1] + 10000*(cosseno))

    x2 = int(pontos[0] - 800*(-seno)) 

    y2 = int(pontos[1] - 800*(cosseno)) 

    return (x1, y1, x2, y2)

def encontrar_intenseccao(raio1, raio2):
    '''
    Encontra intersecção entre duas retas

    Entrada: raio da reta no plano polar
    Saída: Raio do ponto de intersecção e o respectivo ângulo

    OBS: Para esta operação é considerado que o ângulo entre os dois raios é 90º(pi/2 rad) que são as respectivas linhas horizontais e verticais
    '''

    resultante = math.sqrt((raio1**2+raio2**2))

    theta = math.atan(raio1/raio2)

    return (resultante,theta)

def get_resposta(imagem, questao_numero):

    '''
    Entrada: imagem e o número da questão a ser retornada a respectiva resposta
    Saída: anternativa marcada
    '''

    map_indice = {3:'a', 2:'b', 1:'c', 0:'d'}
    espacamento_questoes = int(imagem.shape[0]/QTD_QUESTOES)
    espacamento_anternativas = int(imagem.shape[1]/QTD_ALTERNATIVAS)

    inicio_questao = int(espacamento_questoes*questao_numero)
    fim_questao = int(espacamento_questoes*(questao_numero+1))
    questao = imagem[inicio_questao:fim_questao,:]

    respostas = np.empty(4)
    for alternativa in range(QTD_ALTERNATIVAS-1):
        inicio_alternativa = int(espacamento_anternativas*alternativa)
        fim_alternativa = int(espacamento_anternativas*(alternativa+1))
        respostas[alternativa] = np.mean(questao[:, inicio_alternativa:fim_alternativa])

    indice = np.where(respostas == np.amin(respostas))[0][0]

    return map_indice[indice]

def corrige(imagem):
    '''
    Entrada: é a imagem já cordada
    Saída: dicionário com cada questao como chave e sua respectiva resposta
    '''

    respostas = {}
    for questao in range(1,QTD_QUESTOES):
        respostas[questao] = get_resposta(imagem, questao)
    
    return respostas

def ler_csv(caminho_csv, nome_prova):
    conteudo = np.loadtxt(caminho_csv, dtype=str, delimiter=',')
    indice = np.where(conteudo[:,:1] == nome_prova)[0][0]

    return conteudo[indice]

def main(nome_arquivo):

    img_original = abrir_imagem(nome_arquivo)

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

    # Encontrar linhas com o algoritmo de hough
    l_linhas = cv2.HoughLines(operacao_closing,1,np.pi/180, 80)

    limites_horizontais = np.array([[img_original.size,img_original.size],# [[img_size, img_size], MENOR (raio,theta)
                                [0.0, 0.0]], dtype=np.float64)          #  [0., 0.]], MAIOR (raio,theta)

    limites_verticais = np.array([[img_original.size,img_original.size],# [[img_size, img_size], MENOR (raio,theta)
                                  [0.0, 0.0]], dtype=np.float64)        #  [0., 0.]], MAIOR (raio,theta)

    for linha in l_linhas:
        for raio,theta in linha:

            # Descarta todas as linhas que não sejam horizontais ou verticais

            if np.isclose(theta,0.0): #linhas verticais
                if raio < limites_verticais[0][0]:
                    limites_verticais[0][0] = raio
                    limites_verticais[0][1] = theta

                if raio>limites_verticais[1][0]:
                    limites_verticais[1][0] = raio
                    limites_verticais[1][1] = theta

            elif np.isclose(theta,(np.pi/2.0)):# linhas horizontais

                if raio < limites_horizontais[0][0]:
                    limites_horizontais[0][0] = raio
                    limites_horizontais[0][1] = theta

                if raio>limites_horizontais[1][0]:
                    limites_horizontais[1][0] = raio
                    limites_horizontais[1][1] = theta

    # Ponto superior esquerdo (se)
    raio_se, theta_se = encontrar_intenseccao(limites_horizontais[0][0], limites_verticais[0][0])
    x_se,y_se = hough_para_cartesiano(raio_se,theta_se)

    # Ponto inferior direito (id)
    raio_id, theta_id = encontrar_intenseccao(limites_horizontais[1][0], limites_verticais[1][0])
    x_id,y_id = hough_para_cartesiano(raio_id,theta_id)


    nova_imagem = img_binarizada[int(y_se):int(y_id), int(x_se):int(x_id)]


    respostas = corrige(nova_imagem)
    verdadeiras = ler_csv('images-test/corretas.csv', nome_arquivo)

    print('Questão\tletra\tverdadeira')
    for questao in range(1,QTD_QUESTOES):
        print('  {0} \t {1} \t {2}'.format(questao, respostas[questao],verdadeiras[questao]))


if __name__=='__main__':

    if(len(sys.argv)!=2):
        print('\n\ncompile da seguinte forma: \'python nome_do_seu_programa.py caminho_e_nome_da_imagem\'\n\n')
        sys.exit(0)

    try:
        main(sys.argv[1])
    except NameError as e:
        print(e)