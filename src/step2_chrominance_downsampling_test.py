from common import TEST_PARAMETERS
from matplotlib import pyplot as plt
from step2_chrominance_downsampling import downsample_ycbcr
import cv2
import encoder
import numpy as np

def test_downsample_ycbcr():
    # Carregar imagem de teste
    image = plt.imread(TEST_PARAMETERS['IMAGE-PATH'])

    _, intermidiate_values = encoder.encoder(image, downsampling=TEST_PARAMETERS['DOWNSAMPLING'], return_intermidiate_values=True)

    image_ycbcr = intermidiate_values['ycbcr']

    # Aplicar downsampling
    Y_d, Cb_d, Cr_d = downsample_ycbcr(image_ycbcr, sampling=TEST_PARAMETERS['DOWNSAMPLING'], interpolation=cv2.INTER_CUBIC)

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
    actual_cb = Cb_d[8:16, 8:16]

    assert np.allclose(actual_cb, expected_cb), f'\n{actual_cb}\n!=\n{expected_cb}'
