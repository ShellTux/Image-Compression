import numpy as np
from step3_discrete_cosine_transform import dct_channel, idct_channel, apply_dct_to_channels, recover_channels
from step1_color_space_conversion import rgb_to_ycbcr
from matplotlib.pyplot import imread
from common import TEST_IMAGE

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
    img = imread(TEST_IMAGE)
    
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
