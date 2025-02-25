import os
from typing import Literal
import cv2
import numpy as np

IMAGES = ('./images/airport.bmp', './images/geometric.bmp', './images/nature.bmp')
QUALITIES = (75, 50, 25)

BUILD_DIR = './build'
DOCS_DIR = './docs'

TEST_PARAMETERS = {
    'IMAGE-PATH': './images/airport.bmp',
    'INTERPOLATION': cv2.INTER_LINEAR,
    'DOWNSAMPLING': '4:2:2',
    'QUALITY-FACTOR': 75,
}

RGB_TO_YCBCR_MATRIX = np.array([
    [0.299, 0.587, 0.114],
    [-0.168736, -0.331264, 0.5],
    [0.5, -0.418688, -0.081312],
])
RGB_TO_YCBCR_OFFSET = np.array([0, 128, 128])
YCBCR_TO_RGB_MATRIX = np.linalg.inv(RGB_TO_YCBCR_MATRIX)
YCBCR_TO_RGB_OFFSET = np.array([0, -128, -128])

VALID_DOWNSAMPLES = ('4:2:0', '4:2:2')
VALID_DOWNSAMPLES_TYPE = Literal['4:2:0', '4:2:2']
DEFAULT_DOWNSAMPLE = '4:2:0'

def generate_path(image_path: str, suffix: str, *, output_dir: str, file_extension: str | None = 'png') -> str:
    assert output_dir is not None and len(output_dir) > 0, f'Invalid output_dir: {output_dir}. Needs to be not empty'
    base = os.path.basename(image_path).split('.')
    if file_extension is None:
        return f'{output_dir}/{base[-2]}-{suffix}.{base[-1]}'
    else:
        return f'{output_dir}/{base[-2]}-{suffix}.{file_extension}'
