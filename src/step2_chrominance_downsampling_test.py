from common import TEST_IMAGE
from matplotlib import pyplot as plt
from step1_color_space_conversion import rgb_to_ycbcr
from step2_chrominance_downsampling import downsample_ycbcr
import numpy as np
import cv2

def test_downsample_ycbcr():
    # Carregar imagem de teste
    image_rgb = plt.imread(TEST_IMAGE)
    
    # Converter para YCbCr
    r, g, b = cv2.split(image_rgb)
    y, cb, cr = rgb_to_ycbcr(r, g, b)
    image_ycbcr = cv2.merge([y, cb, cr])
    
    # Aplicar downsampling
    Y_d, Cb_d, Cr_d = downsample_ycbcr(image_ycbcr, sampling="4:2:0", interpolation=cv2.INTER_CUBIC)
    
    # Valores esperados para Cb[8:16, 8:16]
    expected_cb = np.array([
        [136.037, 135.862, 135.869, 135.875, 135.875, 135.869, 135.869, 135.875],
        [136.037, 135.869, 135.869, 135.875, 135.875, 135.869, 135.869, 135.875],
        [136.037, 135.869, 135.869, 136.037, 136.037, 135.869, 135.869, 136.037],
        [134.706, 134.869, 134.869, 134.869, 134.869, 134.862, 134.862, 135.869],
        [134.869, 134.869, 134.869, 134.862, 134.862, 134.862, 134.862, 134.862],
        [134.031, 134.369, 134.031, 134.194, 134.194, 134.031, 134.031, 134.194],
        [133.194, 133.031, 133.031, 132.856, 134.187, 134.031, 134.031, 134.194],
        [132.856, 133.031, 133.031, 133.019, 133.019, 133.031, 133.031, 133.194]
    ])
    
    # Extrair a região 8:16, 8:16 do canal Cb
    actual_cb = cb[8:16, 8:16]
    
    # Verificar se os valores estão próximos (usando tolerância devido a possíveis diferenças de arredondamento)
    np.testing.assert_allclose(actual_cb, expected_cb, rtol=1e-3, atol=1e-3,
                             err_msg=f"\nValores obtidos:\n{actual_cb}\n!=\nValores esperados:\n{expected_cb}")