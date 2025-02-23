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

## 6: Sub-amostragem

Ficheiro: `src/step2_chrominance_downsampling.py`

### 6.1: Downsampling

> Crie uma função para sub-amostrar (downsampling) os canais Y, Cb, e Cr,
> segundo as possibilidades definidas pelo codec JPEG, a qual deve devolver
> Y_d, Cb_d e Cr_d. Utilize, para o efeito, a função cv2.resize (biblioteca
> Computer Vision), testando diferentes métodos de interpolação (e.g., linear,
> cúbica, etc.).

Função: `downsample_ycbcr`

### 6.2: Upsampling

> Crie também a função para efectuar a operação inversa, i.e., upsampling.

Função: `upsample_ycbcr`

### 6.3: Encoder

> Encoder: Obtenha e visualize os canais Y_d, Cb_d e Cr_d com downsampling
> 4:2:0. Apresente as dimensões das matrizes correspondentes.

```console
$ python src/step2_chrominance_downsampling.py
image_path='./images/airport.bmp', sampling='4:2:2'
Dimensões originais: (675, 1216, 3)
Dimensão Y_d: (675, 1216)
Dimensão Cb_d: (675, 608)
Dimensão Cr_d: (675, 608)
image_path='./images/geometric.bmp', sampling='4:2:2'
Dimensões originais: (1001, 1024, 3)
Dimensão Y_d: (1001, 1024)
Dimensão Cb_d: (1001, 512)
Dimensão Cr_d: (1001, 512)
image_path='./images/nature.bmp', sampling='4:2:2'
Dimensões originais: (1200, 1632, 3)
Dimensão Y_d: (1200, 1632)
Dimensão Cb_d: (1200, 816)
Dimensão Cr_d: (1200, 816)
image_path='./images/airport.bmp', sampling='4:2:0'
Dimensões originais: (675, 1216, 3)
Dimensão Y_d: (675, 1216)
Dimensão Cb_d: (337, 608)
Dimensão Cr_d: (337, 608)
image_path='./images/geometric.bmp', sampling='4:2:0'
Dimensões originais: (1001, 1024, 3)
Dimensão Y_d: (1001, 1024)
Dimensão Cb_d: (500, 512)
Dimensão Cr_d: (500, 512)
image_path='./images/nature.bmp', sampling='4:2:0'
Dimensões originais: (1200, 1632, 3)
Dimensão Y_d: (1200, 1632)
Dimensão Cb_d: (600, 816)
Dimensão Cr_d: (600, 816)
```

### 6.4: Decoder

> Decoder: Reconstrua e visualize os canais Y, Cb e Cr. Compare-os com os
> originais.

### Resultados

![Airport Downsampling 4:2:0](docs/airport-downsampling-4:2:0.png)

![Airport Downsampling 4:2:0 Comparison](docs/airport-downsampling-4:2:0-reconstruction-comparison.png)

![Airport Downsampling 4:2:2](docs/airport-downsampling-4:2:2.png)

![Airport Downsampling 4:2:2 Comparison](docs/airport-downsampling-4:2:2-reconstruction-comparison.png)

![Geometric Downsampling 4:2:0](docs/geometric-downsampling-4:2:0.png)

![Geometric Downsampling 4:2:0 Comparison](docs/geometric-downsampling-4:2:0-reconstruction-comparison.png)

![Geometric Downsampling 4:2:2](docs/geometric-downsampling-4:2:2.png)

![Geometric Downsampling 4:2:2 Comparison](docs/geometric-downsampling-4:2:2-reconstruction-comparison.png)

![Nature Downsampling 4:2:0](docs/nature-downsampling-4:2:0.png)

![Nature Downsampling 4:2:0 Comparison](docs/nature-downsampling-4:2:0-reconstruction-comparison.png)

![Nature Downsampling 4:2:2](docs/nature-downsampling-4:2:2.png)

![Nature Downsampling 4:2:2 Comparison](docs/nature-downsampling-4:2:2-reconstruction-comparison.png)
