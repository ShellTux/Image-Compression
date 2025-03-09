from common import TEST_PARAMETERS
from matplotlib import pyplot as plt
from step2_chrominance_downsampling import downsample_ycbcr
import cv2
import encoder
import numpy as np

image = plt.imread(TEST_PARAMETERS.image_path)
_, iv = encoder.encoder(
    image,
    downsampling=TEST_PARAMETERS.downsampling,
    return_intermidiate_values=True
)

Cb_d = np.array([
    [136.037, 135.862, 135.869, 135.875, 135.875, 135.869, 135.869, 135.875],
    [136.037, 135.869, 135.869, 135.875, 135.875, 135.869, 135.869, 135.875],
    [136.037, 135.869, 135.869, 136.037, 136.037, 135.869, 135.869, 136.037],
    [134.706, 134.869, 134.869, 134.869, 134.869, 134.862, 134.862, 135.869],
    [134.869, 134.869, 134.869, 134.862, 134.862, 134.862, 134.862, 134.862],
    [134.031, 134.369, 134.031, 134.194, 134.194, 134.031, 134.031, 134.194],
    [133.194, 133.031, 133.031, 132.856, 134.187, 134.031, 134.031, 134.194],
    [132.856, 133.031, 133.031, 133.019, 133.019, 133.031, 133.031, 133.194]
])

def test_downsample_ycbcr():
    image_ycbcr = iv.YCbCr

    _, actual_Cb, _ = downsample_ycbcr(
        image_ycbcr,
        sampling=TEST_PARAMETERS.downsampling,
        interpolation=cv2.INTER_CUBIC
    )

    expected_Cb_d = actual_Cb

    assert np.allclose(actual_Cb, expected_Cb_d), f'\n{actual_Cb}\n!=\n{expected_Cb_d}'
