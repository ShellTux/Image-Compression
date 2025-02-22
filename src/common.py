import numpy as np

IMAGES = ('./images/airport.bmp', './images/geometric.bmp', './images/nature.bmp')
QUALITIES = (75, 50, 25)
TEST_IMAGE = './images/airport.bmp'

RGB_TO_YCBCR_MATRIX = np.array([
    [0.299, 0.587, 0.114],
    [-0.168736, -0.331264, 0.5],
    [0.5, -0.418688, -0.081312],
])
RGB_TO_YCBCR_OFFSET = np.array([0, 128, 128])
YCBCR_TO_RGB_MATRIX = np.linalg.inv(RGB_TO_YCBCR_MATRIX)
YCBCR_TO_RGB_OFFSET = np.array([0, -128, -128])
