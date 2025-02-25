from common import TEST_PARAMETERS
from matplotlib import pyplot as plt
from step1_color_space_conversion import rgb_to_ycbcr
from step3_discrete_cosine_transform import dct_channel, idct_channel, apply_dct_to_channels, recover_channels, dct_blocks, idct_blocks
import numpy as np

def test_dct_channel():
    # Cria uma matriz de teste simples 8x8
    test_channel = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ], dtype=np.float32)

    # Aplica DCT
    dct_result = dct_channel(test_channel)

    # Aplica IDCT para recuperar o sinal original
    recovered = idct_channel(dct_result)

    # Verifica se o sinal recuperado é aproximadamente igual ao original
    assert np.allclose(test_channel, recovered, atol=1e-10), \
        f"O sinal recuperado não corresponde ao original:\nOriginal:\n{test_channel}\nRecuperado:\n{recovered}"

def test_full_image_dct():
    # Carrega imagem de teste
    img = plt.imread(TEST_PARAMETERS['IMAGE-PATH'])

    # Converte para YCbCr
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    Y, Cb, Cr = rgb_to_ycbcr(r, g, b)

    # Aplica DCT
    Y_dct, Cb_dct, Cr_dct = apply_dct_to_channels(Y, Cb, Cr)

    # Recupera os canais
    Y_rec, Cb_rec, Cr_rec = recover_channels(Y_dct, Cb_dct, Cr_dct)

    # Verifica a recuperação de cada canal
    assert np.allclose(Y, Y_rec, atol=1e-10), "Canal Y não foi recuperado corretamente"
    assert np.allclose(Cb, Cb_rec, atol=1e-10), "Canal Cb não foi recuperado corretamente"
    assert np.allclose(Cr, Cr_rec, atol=1e-10), "Canal Cr não foi recuperado corretamente"

    # Verifica se os valores DCT têm características esperadas
    # A maior energia deve estar concentrada nos coeficientes de baixa frequência
    assert np.abs(Y_dct[0,0]) > np.mean(np.abs(Y_dct)), "Energia do canal Y não está concentrada nas baixas frequências"
    assert np.abs(Cb_dct[0,0]) > np.mean(np.abs(Cb_dct)), "Energia do canal Cb não está concentrada nas baixas frequências"
    assert np.abs(Cr_dct[0,0]) > np.mean(np.abs(Cr_dct)), "Energia do canal Cr não está concentrada nas baixas frequências"

def test_dct_8x8():
    # Carrega a imagem de teste (por exemplo, airport.bmp)
    img = plt.imread(TEST_PARAMETERS['IMAGE-PATH'])

    # Converte a imagem para o espaço de cor YCbCr
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    Y, Cb, Cr = rgb_to_ycbcr(r, g, b)

    # Aplica a DCT em blocos 8x8 no canal Y
    Y_dct8 = dct_blocks(Y)

    # Extrai o bloco de coordenadas [8:16, 8:16]
    block_dct = Y_dct8[8:16, 8:16]

    # Matriz esperada conforme os resultados da validação (alínea 7.2)
    expected_block = np.array([
        [1.80777663e+03, -9.23242261e-01, -5.29636497e-01,  3.59445648e-01, -1.76362500e+00,  5.55083588e-01, -2.98406749e-01, -4.60890519e-02],
        [-2.03673479e+01, -9.82171542e-01, -8.86593039e-02, -5.92479366e-01,  2.05786124e-01, -4.40442200e-01, -2.79880553e-01, -8.09695807e-02],
        [3.01421591e+00,  2.96358656e+00, -5.05785655e-01,  5.32572109e-01,  2.78262642e-01,  2.64984553e-01, -1.70624815e-01,  4.42421783e-01],
        [-1.55397910e+00, -5.90294119e-01, -2.27573528e-01,  4.87826728e-01,  1.58910590e-01,  2.61243202e-01,  3.27367962e-01, -2.07981922e-01],
        [1.15787500e+00,  2.03021506e-01,  2.68178989e-01, -1.23757464e-01,  7.06250000e-02, -4.00909176e-01,  1.85897985e-01, -9.99756393e-02],
        [3.91716121e-01, -2.49542185e-01, -3.88121070e-01,  8.46698258e-02, -1.12999755e-01,  1.77816633e-01, -2.46778824e-01, -1.26352968e-01],
        [1.25161893e-01,  2.41893572e-01,  1.28375185e-01,  3.35478925e-01, -5.71082576e-01,  4.37425155e-01, -4.84643446e-02,  3.97998520e-01],
        [-1.29250561e-01, -1.08042957e-01, -4.65970112e-01, -3.52498952e-01, -3.18990577e-01, -1.04955260e-01, -5.53132343e-01, -1.24718188e-02]
    ], dtype=np.float64)

    # Verifica se o bloco obtido é aproximadamente igual ao esperado
    assert np.allclose(block_dct, expected_block, atol=1e-5), (
        f"Bloco DCT 8x8 obtido:\n{block_dct}\n"
        f"não corresponde ao esperado:\n{expected_block}"
    )


def test_block_8x8_dct_idct():
    # Carrega a imagem de teste
    img = plt.imread(TEST_PARAMETERS['IMAGE-PATH'])

    # Converte para YCbCr
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    Y, Cb, Cr = rgb_to_ycbcr(r, g, b)

    # Aplica DCT em blocos 8x8
    Y_dct8 = dct_blocks(Y)
    Cb_dct8 = dct_blocks(Cb)
    Cr_dct8 = dct_blocks(Cr)

    # Aplica IDCT em blocos 8x8 para recuperar os canais
    Y_rec8 = idct_blocks(Y_dct8)
    Cb_rec8 = idct_blocks(Cb_dct8)
    Cr_rec8 = idct_blocks(Cr_dct8)

    # Verifica se os canais recuperados são aproximadamente iguais aos originais
    assert np.allclose(Y, Y_rec8, atol=1e-10), "Canal Y não foi recuperado corretamente (8x8)."
    assert np.allclose(Cb, Cb_rec8, atol=1e-10), "Canal Cb não foi recuperado corretamente (8x8)."
    assert np.allclose(Cr, Cr_rec8, atol=1e-10), "Canal Cr não foi recuperado corretamente (8x8)."
