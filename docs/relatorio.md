# Multimédia

---
title: Relatório de Multimédia
author:
  - Gonçalo José dos Santos Silva, nº 2022233004
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Pedro
  - Renato Marques Reis, nº 2022232936
date: \today
---

<!-- TODO: Depois de terminar o relatório, adicionar code snippets.-->

## 1: Compressão de imagens bmp no formato jpeg utilizando um editor de imagem (e.g., GIMP).

Para comprimirmos as imagens, escrevemos um python script que invoca ffmpeg.
Esse ficheiro encontra-se em `src/ex1.py`.

| Image         | Quality | Compression Ratio |
| ---           | :-----: | :--------------:  |
| airport.bmp   | 75      | 21.21             |
| airport.bmp   | 50      | 32.75             |
| airport.bmp   | 25      | 41.87             |
| geometric.bmp | 75      | 55.05             |
| geometric.bmp | 50      | 81.36             |
| geometric.bmp | 25      | 97.01             |
| nature.bmp    | 75      | 19.96             |
| nature.bmp    | 50      | 39.31             |
| nature.bmp    | 25      | 57.35             |

## 2: encoder e decoder

As funções `encoder` e `decoder` implementadas no `src/main.py`.

## 3: Visualização de imagem representada pelo modelo de cor RGB

## 4: Pré-processamento da imagem: padding

Ficheiro: `src/step0_preprocessing.py`

### 4.1: Encoder

> Encoder: Crie uma função para fazer padding dos canais RGB. Caso a dimensão
> da imagem não seja múltipla de 32x32, faça padding da mesma, replicando a
> última linha e a última coluna em conformidade.

Função: `encoder`

### Decoder

Função: `decoder`

### Resultados

![Airport Padding](docs/airport-padding.png)

![Geometric Padding](docs/geometric-padding.png)

![Nature Padding](docs/nature-padding.png)

## 5: Conversão para o modelo cor YCbCr

Ficheiro: `src/step1_color_space_conversion.py`

### 5.1

> Crie uma função para converter a imagem do modelo de cor RGB para o modelo de
> cor YCbCr.

Função: `rgb_to_ycbcr`

### 5.2

> Crie também a função inversa (conversão de YCbCr para RGB). Nota: na
> conversão inversa, garanta que os valores R, G e B obtidos sejam números
> inteiros no intervalo {0, 1, …, 255}.

Função: `ycbcr_to_rgb`

### Resultados

![Airport Color Space Conversion](docs/airport-color-space-conversion.png)

![Geometric Color Space Conversion](docs/geometric-color-space-conversion.png)

![Nature Color Space Conversion](docs/nature-color-space-conversion.png)
