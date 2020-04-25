# OMR-oriented-to-MCQ

Este repositório faz parte dos cursos de visão computacional da alura, aqui fazemos o uso de processamento de imagens para reconhecimento de escolhas marcadas em testes.

O objetivo do curso é utilizar alguns métodos simples de processamento de imagem para criar uma algoritmo capaz de detectar e reconhecer as escolhas feitas nos testes de múltipla escolha.

## Base de dados

Os dados utilizados no curso e nos algoritmos testados são 10 imagens que são encontradas [neste repositório](https://github.com/suayder/OMR-oriented-to-MCQ/tree/master/images-test) que foram extraidas e modificadas do [data set original](https://sites.google.com/view/mcq-dataset) usado para obter os resultados encontrados no artigo de [Afifi, Mahmoud, and Khaled F. Hussain.](https://arxiv.org/pdf/1711.00972.pdf)


## Rodando o projeto

Este projeto possui dois arquivos, ambos são os projetos finais, um com extensão `.ipynb` que é adaptado para rodar no colab do Google e outro é um arquivo `.py`, para roda-lo ele utiliza uma flag para passar a imagem: 

```
python projeto-final.py `caminho-da-imagem`
```

## Conteúdo deste curso

> Você vai aprender:
>
>   - Operações básicas com imagens
>      - Abrir a imagem
>      - Mostra-la em uma janela
>   - Filtros de transformação
>       - Threshold
>       - Canny
>       - morfológicos
>   - Encontrar contornos dos objetos
>   - Encontrar linhas com a [transformada de Hough](https://www.learnopencv.com/hough-transform-with-opencv-c-python/)
>   - Extrair informações baseados em cores

---

# OMR-oriented-to-MCQ

This is part of computer vision courses, in this depository we use image processing to recognize mark choice in tests.

The goal of the course is to use some simple image processing methods to create an algorithm able to detect and recognize the choice in multiple-choice test based.

## Data test

The [data set](https://github.com/suayder/OMR-oriented-to-MCQ/tree/master/images-test) used for our test is extracted and modified from the original [data set](https://sites.google.com/view/mcq-dataset) used to obtain results the paper of [Afifi, Mahmoud, and Khaled F. Hussain.](https://arxiv.org/pdf/1711.00972.pdf)


## Running this project

This git contains two files, both of them are final projects, one with the extension `.ipynb` which is adapted to run on the Google colab and the other is a `.py` file, to run it it uses a flag to pass the image :

```
python projeto-final.py `path-to-your-image`
```

## Content of this course

> You will learn:
>
>   - Basic image operations
>      - Read and open the image
>      - Show an image in a window
>   - Transformation filters
>       - Threshold
>       - Canny
>       - mophological
>   - Object contour finding
>   - Find lines with [Hough's transform](https://www.learnopencv.com/hough-transform-with-opencv-c-python/)
>   - Color description information