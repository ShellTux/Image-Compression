from common import TEST_PARAMETERS
from matplotlib import pyplot as plt
import step1_color_space_conversion as csc
import numpy as np

image = plt.imread(TEST_PARAMETERS.image_path)

RED = np.array([
    [209, 212, 210, 208, 208, 210, 210, 207],
    [209, 210, 210, 208, 208, 210, 210, 208],
    [209, 211, 211, 210, 210, 211, 212, 210],
    [210, 212, 212, 212, 212, 215, 215, 213],
    [212, 213, 213, 215, 215, 216, 216, 216],
    [216, 214, 216, 217, 217, 217, 217, 217],
    [219, 218, 218, 221, 221, 218, 218, 218],
    [223, 220, 220, 223, 223, 219, 219, 219]
])

Y = np.array([
    [222.758, 223.068, 223.057, 223.046, 223.046, 223.057, 223.057, 222.046],
    [222.758, 223.057, 223.057, 223.046, 223.046, 223.057, 223.057, 223.046],
    [222.758, 224.057, 224.057, 223.758, 223.758, 224.057, 225.057, 223.758],
    [224.117, 224.829, 224.829, 224.829, 224.829, 225.84,  225.84,  226.057],
    [224.829, 225.829, 225.829, 225.84,  225.84,  226.84,  226.84,  226.84 ],
    [227.313, 226.715, 227.313, 227.025, 227.025, 228.313, 228.313, 227.025],
    [228.797, 229.085, 229.085, 229.395, 229.036, 229.313, 229.313, 228.025],
    [231.395, 231.085, 231.085, 230.107, 230.107, 230.085, 230.085, 228.797]
])

Cb = np.array([
    [136.037, 135.862, 135.869, 135.875, 135.875, 135.869, 135.869, 135.875],
    [136.037, 135.869, 135.869, 135.875, 135.875, 135.869, 135.869, 135.875],
    [136.037, 135.869, 135.869, 136.037, 136.037, 135.869, 135.869, 136.037],
    [134.706, 134.869, 134.869, 134.869, 134.869, 134.862, 134.862, 135.869],
    [134.869, 134.869, 134.869, 134.862, 134.862, 134.862, 134.862, 134.862],
    [134.031, 134.369, 134.031, 134.194, 134.194, 134.031, 134.031, 134.194],
    [133.194, 133.031, 133.031, 132.856, 134.187, 134.031, 134.031, 134.194],
    [132.856, 133.031, 133.031, 133.019, 133.019, 133.031, 133.031, 133.194]
])

def test_rgb_from_ndarray():
    r, _, _ = csc.rgb_from_ndarray(image)
    r = r[8:16, 8:16]
    expected_r = RED

    assert np.array_equal(r, expected_r), f'\n{r}\n!=\n{expected_r}'

def test_rgb_to_ycbcr():
    r, g, b = csc.rgb_from_ndarray(image)
    y, cb, _ = csc.rgb_to_ycbcr(r, g, b)

    y = y[8:16, 8:16]
    cb = cb[8:16, 8:16]

    expected_y = Y
    expected_cb = Cb

    assert np.allclose(y, expected_y), f'\n{y}\n!=\n{expected_y}'
    assert np.allclose(cb, expected_cb), f'\n{cb}\n!=\n{expected_cb}'
