# Compressão de Imagem: JPEG Codec

---
title: Relatório de Multimédia
lang: pt-PT
toc: true
author:
  - Gonçalo José dos Santos Silva, nº 2022233004
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Pedro Francisco Madureira Garcia Teixeira, nº 2017261525
  - Renato Marques Reis, nº 2022232936
date: \today
header-includes: |
    \usepackage[utf8]{inputenc}
    \usepackage{fdsymbol}
    \usepackage{newunicodechar}
    \usepackage[a4paper, margin=1in]{geometry}
    \newunicodechar{ϵ}{\ensuremath{\epsilon}}
    \usepackage{float}
    \makeatletter
    \def\fps@figure{H}
    \makeatother
---

<!-- TODO: Depois de terminar o relatório, adicionar code snippets.-->

## 1: Compressão das imagens

> Compressão de imagens bmp no formato jpeg utilizando um editor de imagem
> (e.g., GIMP).

Ficheiro: `src/compress-ffmpeg.py`

Para comprimirmos as imagens, escrevemos um python script que invoca ffmpeg.

| Imagem        | Qualidade | Taxa de Compressão | Resultado |
| ---           | :-------: | :---------------:  | :-------: |
| airport.bmp   | 75        | 21.21              | Ótimo     |
| airport.bmp   | 50        | 32.75              | Bom       |
| airport.bmp   | 25        | 41.87              | Médio     |
| geometric.bmp | 75        | 55.05              | Bom       |
| geometric.bmp | 50        | 81.36              | Médio     |
| geometric.bmp | 25        | 97.01              | Mau       |
| nature.bmp    | 75        | 19.96              | Ótimo     |
| nature.bmp    | 50        | 39.31              | Bom       |
| nature.bmp    | 25        | 57.35              | Médio     |

### 1.4: Resultados e Conclusão

> Compare os resultados e tire conclusões.

<!--![Airport ffmpeg compression](docs/airport-compression-ffmpeg.png)-->
<!---->
<!--![Geometric ffmpeg compression](docs/geometric-compression-ffmpeg.png)-->
<!---->
<!--![Nature ffmpeg compression](docs/nature-compression-ffmpeg.png)-->

![Compression Plot](docs/compression-plot.png)

A compressão pelo codec JPEG produz resultados diferentes dependendo do tipo de
imagem (ex: fotográfica vs geométrica). No caso das geométricas, com alterações
repentinas a nível de cores, podemos observar um maior número de artefactos na
imagem comprimida, e por isso será melhor optar por outros codecs de
compressão. O mesmo não acontece com imagens fotográficas, visto que estas
normalmente têm transições de cores e tonalidades mais suaves.


## 2: Funções encoder e decoder

> Crie duas funções, encoder e decoder, para encapsular as funções a
> desenvolver nas alíenas 3 a 9. Nota: a ordem da chamada de funções no decoder
> deve ser inversa da do encoder, dado que corresponderá à inversão da
> cofificação realizada.

Ficheiros: `src/encoder.py` e `src/decoder.py`

## 3: Visualização de imagem representada pelo modelo de cor RGB

### 3.2: Palete customizada

Ficheiro: `src/common.py`

> Crie uma função para implementar um colormap definido pelo utilizador.


### 3.3: Visualização de uma imagem com uma palete

> Crie uma função que permita visualizar a imagem com um dado colormap.

Ficheiro: `src/step1_color_space_conversion.py`

### 3.4: Encoder

> Encoder: Crie uma função para separar a imagem nos seus componentes RGB.

Função: `rgb_from_ndarray`

### 3.6: Resultados

> Visualize a imagem e cada um dos canais RGB (com o colormap adequado).

Ver resposta ao [ex. 5.5](#5.5-resultados-e-conclusões).


## 4: Pré-processamento

> Pré-processamento da imagem: padding.

Ficheiro: `src/step0_preprocessing.py`

### 4.1: Encoder

> Encoder: Crie uma função para fazer padding dos canais RGB. Caso a dimensão
> da imagem não seja múltipla de 32x32, faça padding da mesma, replicando a
> última linha e a última coluna em conformidade.

Função: `padding`

### 4.2: Decoder

> Decoder: Crie também a função inversa para remover o padding. Certifique-se
> de que recupera os canais RGB com a dimensão original, visualizando a imagem
> original.

Função: `ipadding`

### Resultados

![Airport Padding](docs/step0/airport-padding.png)

![Geometric Padding](docs/step0/geometric-padding.png)

![Nature Padding](docs/step0/nature-padding.png)

## 5: Conversão para o modelo cor YCbCr

Ficheiro: `src/step1_color_space_conversion.py`

### 5.1: Conversão

> Crie uma função para converter a imagem do modelo de cor RGB para o modelo de
> cor YCbCr.

Função: `rgb_to_ycbcr`

### 5.2: Inversa conversão

> Crie também a função inversa (conversão de YCbCr para RGB). Nota: na
> conversão inversa, garanta que os valores R, G e B obtidos sejam números
> inteiros no intervalo {0, 1, …, 255}.

Função: `ycbcr_to_rgb`

### 5.5: Resultados e Conclusões

> Compare a imagem de Y com R, G e B e com Cb e Cr. Tire conclusões.

![Airport Color Space Conversion](docs/step1/airport-color-space-conversion.png)

![Geometric Color Space Conversion](docs/step1/geometric-color-space-conversion.png)

![Nature Color Space Conversion](docs/step1/nature-color-space-conversion.png)


Na conversão de RGB para YCbCr, a componente Y (luminância) representa o brilho
da imagem, enquanto Cb e Cr representam a crominância (informação de cor). Para
analisar a relação entre Y e os canais R, G e B, bem como com Cb e Cr, podemos
observar o seguinte:

- O canal G (verde) tem o maior peso na formação de Y, seguido de R
    (vermelho) e depois B (azul). Isso significa que áreas verdes
    aparecem mais brilhantes no canal Y, pois a contribuição de G é
    maior. Regiões predominantemente vermelhas terão luminância
    intermédia, enquanto as áreas azuis tendem a ser mais escuras na
    imagem Y.

- Cb representa a diferença entre Y e B.
    Assim, áreas mais azuis terão valores mais altos de Cb, enquanto
    áreas alaranjadas (opostas ao azul) terão valores mais baixos. Cr
    representa a diferença entre Y e R. Portanto, áreas avermelhadas
    terão valores mais altos de Cr, enquanto áreas verdes (opostas ao
    vermelho) terão valores mais baixos. Como Y se baseia
    principalmente em G, a separação da crominância (Cb e Cr) ajuda a
    distinguir melhor as cores, sem influenciar diretamente o brilho.

### Conclusões:

O canal Y é mais parecido com o G do que com R e B, devido à maior influência
do verde na percepção da luminância. Cb e Cr destacam diferenças de cor que não
são evidentes no canal Y, ajudando na compressão de imagem e na transmissão de
cor em sistemas como JPEG.

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

### 6.4: Decoder

> Decoder: Reconstrua e visualize os canais Y, Cb e Cr. Compare-os com os
> originais.

### 6.5: Resultados

> Apresente e analise o resultado da compressão para as variantes de
> downsampling 4:2:2 e 4:2:0 (taxa de compressão, destrutividade, etc.)

![Airport Downsampling 4:2:0](docs/step2/airport-downsampling-420.png)

![Airport Downsampling 4:2:0 Comparison](docs/step2/airport-downsampling-420-reconstruction-comparison.png)

![Airport Downsampling 4:2:2](docs/step2/airport-downsampling-422.png)

![Airport Downsampling 4:2:2 Comparison](docs/step2/airport-downsampling-422-reconstruction-comparison.png)

![Geometric Downsampling 4:2:0](docs/step2/geometric-downsampling-420.png)

![Geometric Downsampling 4:2:0 Comparison](docs/step2/geometric-downsampling-420-reconstruction-comparison.png)

![Geometric Downsampling 4:2:2](docs/step2/geometric-downsampling-422.png)

![Geometric Downsampling 4:2:2 Comparison](docs/step2/geometric-downsampling-422-reconstruction-comparison.png)

![Nature Downsampling 4:2:0](docs/step2/nature-downsampling-420.png)

![Nature Downsampling 4:2:0 Comparison](docs/step2/nature-downsampling-420-reconstruction-comparison.png)

![Nature Downsampling 4:2:2](docs/step2/nature-downsampling-422.png)

![Nature Downsampling 4:2:2 Comparison](docs/step2/nature-downsampling-422-reconstruction-comparison.png)

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

## 7: Transformada de Coseno Discreta (DCT)

Ficheiro: `src/step3_discrete_cosine_transform.py`

### 7.1: DCT nos canais completos

#### 7.1.1: DCT de um canal completo

> Crie uma função para calcular a DCT de um canal completo. Utilize a função
> scipy.fftpack.dct.

Função: `dct_channel`

#### 7.1.2: DCT inverso de um canal completo

> Crie também a função inversa (usando scipy.fftpack.idct). Nota: para uma
> matriz, X, com duas dimensões, deverá fazer: X_dct = dct(dct(X,
> norm=”ortho”).T, norm=”ortho”).T

Função: `idct_channel`

#### 7.1.3: Encoder

> Encoder: Aplique a função desenvolvida em 7.1.1 a Y_d, Cb_d, Cr_d e visualize
> as imagens obtidas (Y_dct, Cb_dct, Cr_dct). Sugestão: atendendo à gama ampla
> de valores da DCT, visualize as imagens usando uma transformação logarítmica
> (apta para compressão de gama), de acordo com o seguinte pseudo-código:
> imshow(log(abs(X) + 0.0001))

Função: `apply_dct_to_channels`

#### 7.1.4: Decoder

> Decoder: Aplique a função inversa (7.1.2) e certifique-se de que consegue
> obter os valores originais de Y_d, Cb_d e Cr_d.

Função: `recover_channels`

### 7.2: DCT em blocos 8x8

#### 7.2.1: DCT em blocos

> Usando as mesmas funções para cálculo da DCT, crie uma função que calcule a
> DCT de um canal completo em blocos BSxBS.

Função: `dct_blocks`

#### 7.2.2: IDCT em blocos

> Crie também a função inversa (IDCT BSxBS).

Função: `idct_blocks`

#### 7.2.3: Encoder

> Encoder: Aplique a função desenvolvida (7.2.1) a Y_d, Cb_d, Cr_d com blocos
> 8x8 e visualize as imagens obtidas (Y_dct8, Cb_dct8, Cr_dct8).

#### 7.2.4: Decoder

>  Decoder:  Aplique a função inversa (7.2.2) e certifique-se de que consegue
>  obter os valores originais de Y_d, Cb_d e Cr_d.

### 7.3: DCT em blocos 64x64

> DCT em blocos 64x64. Repita 7.2 para blocos com dimensão 64x64.

Função: `dct_blocks`

### 7.4: Potencial de compressão

> Compare e discuta os resultados obtidos em 7.1, 7.2 e 7.3 em termos de
> potencial de compressão.

![Airport DCT nos canais completos](docs/step3/airport-dct-logarithmic-transformation.png)

![Airport DCT blocos 8x8](docs/step3/airport-dct-blocks-8x8.png)

![Airport DCT blocos 64x64](docs/step3/airport-dct-blocks-64x64.png)

![Geometric DCT nos canais completos](docs/step3/geometric-dct-logarithmic-transformation.png)

![Geometric DCT blocos 8x8](docs/step3/geometric-dct-blocks-8x8.png)

![Geometric DCT blocos 64x64](docs/step3/geometric-dct-blocks-64x64.png)

![Nature DCT nos canais completos](docs/step3/nature-dct-logarithmic-transformation.png)

![Nature DCT blocos 8x8](docs/step3/nature-dct-blocks-8x8.png)

![Nature DCT blocos 64x64](docs/step3/nature-dct-blocks-64x64.png)

A comparação dos resultados obtidos em 7.1 (DCT de canais completos), 7.2 (DCT
em blocos de 8x8) e 7.3 (DCT em blocos de 64x64) demonstra diferenças
significativas no potencial de compressão. Quando se utiliza a DCT em blocos de
8x8, observa-se uma melhoria considerável na compressão em comparação com a
aplicação da DCT no canal completo. Isso porque a abordagem em blocos permite
uma melhor representação da informação de frequência, aproveitando a
redundância espacial nas imagens, resultando em melhores taxas de compressão.

Por outro lado, a utilização de blocos de 64x64, apesar de ainda fornecer
compressão, pode levar a uma perda maior na qualidade visual, uma vez que uma
maior quantidade de informação é perdida devido ao tamanho do bloco. Os
artefatos visuais podem ser mais evidentes, especialmente em imagens com
detalhes finos. Assim, a escolha do tamanho do bloco tem impacto direto tanto
na taxa de compressão quanto na qualidade da imagem reconstruída.

Em suma, o método de blocos de 8x8 demonstra um ótimo equilíbrio entre
compressão e qualidade visual, enquanto o método de blocos de 64x64, apesar de
uma maior compressão, pode resultar em perdas visuais significativas.

## 8: Quantização

Ficheiro: `src/step4_quatization.py`

### 8.1: Quantização dos coeficientes

> Crie uma função para quantizar os coeficientes da DCT para cada bloco 8x8.

Função: `quantization`

### 8.2: Inversa quantização

> Crie também a função inversa.

Função: `iquantization`

### 8.3: Encoder

> Encoder: Quantize os coeficientes da DCT, usando os seguintes factores de
> qualidade: 10, 25, 50, 75 e 100. Visualize as imagens obtidas (Y_q, CB_q e
> Cr_q).

### 8.4: Decoder

> Decoder: Desquantize os coeficientes da DCT, usando os mesmos factores de
> qualidade. Visualize as imagens obtidas.

### 8.5: Compare os resultados

> Compare os resultados obtidos com os vários factores de qualidade e
> discuta-os em termos de potencial de compressão.

A comparação dos resultados obtidos com diferentes fatores de qualidade ao
realizar a quantização dos coeficientes da DCT mostra uma clara relação entre a
qualidade da imagem e a taxa de compressão. Os fatores de qualidade mais baixos
(por exemplo, 10 e 25) resultam em uma compressão mais forte, mas também
introduzem artefatos visuais notáveis e perda de detalhes na imagem. À medida
que o fator de qualidade aumenta, a qualidade visual da imagem reconstruída
melhora, mas a taxa de compressão diminui.

Imagens quantizadas com fatores de qualidade mais altos (50, 75, e 100) mantêm
mais detalhes e apresentam menos artefatos, resultando em uma sensação visual
mais agradável, mas com menor compressão. Portanto, a escolha do fator de
qualidade deve estar alinhada às necessidades específicas de cada aplicação,
considerando um trade-off entre a qualidade da imagem desejada e a eficiência
de compressão.

### 8.6: Compare os resultados

> Compare os resultados obtidos com os da alínea 7 (DCT) e tire conclusões.

Ao comparar os resultados obtidos nas alíneas 7 (DCT) e 8 (quantização),
torna-se evidente que a quantização tem um impacto significativo no potencial
de compressão e na qualidade da imagem resultante. Enquanto a DCT reduz a
informação espacial em frequências, a quantização aplica um nível adicional de
redução de dados ao eliminar informações que são percebidas como menos
relevantes para a visualização humana.

Os resultados mostram que a DCT sozinha pode ainda gerar uma imagem de
qualidade aceitável, mas a aplicação de quantização acentua a redução de
detalhes em contrapartida a um aumento na taxa de compressão. A quantização,
dependendo do fator de qualidade, pode acentuar a perda de dados e introduzir
artefatos, enquanto resulta em formatos mais compactos de armazenamento.

Em suma, a combinação de DCT e quantização é crucial para o processo de
compressão JPEG, e a escolha cuidadosa de fatores de qualidade pode otimizar
tanto a compressão quanto a qualidade visual da imagem.

## 9: Codificação DPCM dos coeficientes DC

Ficheiro: `src/step5_dpcm.py`

### 9.1: Codificação dos coeficientes DC de cada bloco

> Crie uma função para realizar a codificação dos coeficientes DC de cada
> bloco. Em cada bloco, substitua o valor DC pelo valor da diferença.

Função: `dpcm_encode`

### 9.2: Decodificação dos coeficientes DC de cada bloco

> Crie também a função inversa.

Função: `dpcm_decode`

### 9.3: Encoder

> Encoder: Aplique a função 9.1 aos valores da DCT quantizada, obtendo Y_dpcm,
> Cb_dpcm e Cr_dpcm).

### 9.4: Decoder

> Decoder: Aplique a função inversa (9.2) e certifique-se de que consegue obter
> os valores originais de Y_q, Cb_q e Cr_q.

### 9.5: Resultados e Conclusões

> Analise os resultados e tire conclusões.

Ao analisar os resultados da codificação DPCM dos coeficientes DC, observa-se
uma redução significativa na quantidade de dados necessários para representar
as diferenças entre os valores DC de cada bloco. A codificação DPCM melhora
ainda mais a eficiência da compressão ao armazenar a diferença de cada valor DC
em vez do valor absoluto, que é especialmente útil quando os valores
consecutivos são geralmente similares, resultando em valores de diferença
pequenos que caem num espetro mais pequeno portanto mais fácil de comprimir.

As conclusões tiradas a partir dos resultados indicam que esta abordagem não
apenas reduz o tamanho do arquivo, mas também pode ser integrada eficazmente
com outros passos do processo de compressão (como a DCT e a quantização) para
otimizar o desempenho geral do codec JPEG. Esta técnica é especialmente eficaz
em imagens com alta redundância, onde as diferenças entre pixels adjacentes são
mínimas.

## 10: Codificação e descodificação end-to-end

> Codificação e descodificação end-to-end.

> [!NOTE]
> As funções criadas na alínea 2 deverão conter, neste momento, todo o código
> de codificação e descodificação desenvolvido nas alíenas 3 a 9. Note que,
> após a quantização da DCT, não se pretende, neste trabalho, aplicar os passos
> de compressão não destrutiva dos coeficientes AC (RLE, Huffman / códigos
> aritméticos).

Ficheiro: `src/step10_error_analysis.py`

### 10.1: Encoder

> Encoder: Codifique as imagens fornecidas com os seguintes parâmetros de
> qualidade: 10, 25, 50, 75 e 100.

### 10.2: Decoder

> Decoder: Reconstrua as imagens com base no resultado de 10.1.

### 10.3 Cálculo das diferenças

> Crie uma função para cálculo da imagem das diferenças (entre o canal Y da
> original e da descompactada).

Função: `calculate_absolute_difference`

### 10.4 Cálculo das métricas de distorção

> Crie uma função para cálculo das métricas de distorção MSE, RMSE, SNR, PSNR,
> max_diff e avg_diff (por comparação da imagem original com a descompactada).

Função: `calculate_error_metrics`

### 10.5: Visualização das imagens e métricas

> Visualize as imagens descodificadas. Visualize também a imagem das diferenças
> entre o canal Y de cada uma das imagens originais e da imagem descodificada
> respectiva para cada um dos factores de qualidade testados. Calcule as várias
> métricas de distorção (imagem RGB: MSE, RMSE, SNR, PSNR; canal Y: max_diff e
> avg_diff) para cada uma das imagens e factores de qualidade. Tire conclusões.

Função: `visualize_difference`

```console
Analisando imagem: ./images/airport.bmp
Parâmetros: QF=75, Downsampling=4:2:2

Erros na imagem:
Max diff: 116.0
Avg diff: 3.2201460905349792

Erros na imagem de 3 canais reconstruída:
MSE = 25.2575987654321
RMSE = 5.025693859103646
SNR = 30.855772102426812
PSNR = 34.106883009705484

Erros no canal Y:
Max diff: 42.590732421874975
Avg diff: 2.6200079295793888
```

![Airport Error Analysis](docs/airport-error-analysis-qf75-422.png)

A visualização das imagens descodificadas e das imagens de diferença entre o
canal Y original e o canal Y descodificado revela as distorções introduzidas ao
longo do processo de compressão e descompressão. Através dos cálculos das
métricas de distorção, como MSE, RMSE, SNR e PSNR, podemos quantificar a
qualidade da imagem resultante em comparação com a imagem original.

As métricas demonstram que, à medida que o fator de qualidade aumenta, as
medidas de distorção (como MSE e RMSE) diminuem, indicando uma melhoria na
qualidade visual da imagem. As médias de diferença, max_diff e avg_diff no
canal Y nos fornecem uma visão mais granular sobre como a compressão afeta a
imagem em termos de luminosidade e detalhes.

Esses dados são cruciais para entender o trade-off entre compressão e qualidade
e podem ajudar a refinar ainda mais algoritmos de compressão, garantindo que a
qualidade visual desejada seja mantida enquanto a quantidade de dados é
reduzida com sucesso.

### 10.6: Análise e conclusões

> 10.6. Volte a analisar a alínea 1, de forma a validar/complementar as
> conclusões tiradas nesse ponto.

Após revisar a alínea 1, confirmam-se várias conclusões iniciais sobre o
impacto da compressão JPEG na qualidade das imagens. À medida que ajustamos os
fatores de qualidade e as técnicas aplicadas (como DCT, quantização e DPCM),
notamos que a qualidade da imagem é influenciada pela natureza da imagem
(fotográfica, geométrica) e pelas configurações de compressão escolhidas. As
imagens fotográficas geralmente mantêm uma aparência mais natural mesmo em
compressões mais altas, enquanto as imagens geométricas tendem a sofrer mais
com artefatos de compressão, o que reafirma a necessidade de escolher o método
de compressão de acordo com o conteúdo da imagem.

A análise conclui que um equilíbrio adequado entre a taxa de compressão e a
qualidade visual é crucial para aplicações práticas e que as decisões sobre
quais técnicas aplicar e quais parâmetros utilizar devem ser informadas pelo
contexto em que as imagens serão utilizadas.
mais, é só avisar.
