from sys import stderr
from typing import Literal, NamedTuple
import cv2
import matplotlib.colors as clr
import numpy as np
import os

IMAGES = ('./images/airport.bmp', './images/geometric.bmp', './images/nature.bmp')
QUALITIES = (75, 50, 25)

BUILD_DIR = './build'
DOCS_DIR = './docs'

VALID_DOWNSAMPLES = ('4:2:0', '4:2:2')
VALID_DOWNSAMPLES_TYPE = Literal['4:2:0', '4:2:2']
DEFAULT_DOWNSAMPLE = '4:2:0'

class TestParameters(NamedTuple):
    image_path: str
    interpolation: int
    downsampling: VALID_DOWNSAMPLES_TYPE
    quality_factor: int

TEST_PARAMETERS = TestParameters(
    './images/airport.bmp',
    cv2.INTER_LINEAR,
    '4:2:2',
    75,
)

class ColorMap(NamedTuple):
    red: clr.LinearSegmentedColormap
    green: clr.LinearSegmentedColormap
    blue: clr.LinearSegmentedColormap
    gray: clr.LinearSegmentedColormap

red_cmap = clr.LinearSegmentedColormap.from_list("red", [(0,0,0),(1,0,0)], N = 256)
green_cmap = clr.LinearSegmentedColormap.from_list("red", [(0,0,0),(0,1,0)], N = 256)
blue_cmap = clr.LinearSegmentedColormap.from_list("red", [(0,0,0),(0,0,1)], N = 256)
gray_cmap = clr.LinearSegmentedColormap.from_list("gray", [(0,0,0),(1,1,1)], N = 256)

custom_cmap = ColorMap(red_cmap, green_cmap, blue_cmap, gray_cmap)

class ColorConversion(NamedTuple):
    RGB2YCbCr_matrix: np.ndarray
    RGB2YCbCr_offset: np.ndarray
    YCbCr2RGB_matrix: np.ndarray
    YCbCr2RGB_offset: np.ndarray

COLOR_CONVERSION = ColorConversion(
    np.array([
        [0.299, 0.587, 0.114],
        [-0.168736, -0.331264, 0.5],
        [0.5, -0.418688, -0.081312],
    ]),
    np.array([0, 128, 128]),
    np.linalg.inv(np.array([
        [0.299, 0.587, 0.114],
        [-0.168736, -0.331264, 0.5],
        [0.5, -0.418688, -0.081312],
    ])),
    np.array([0, -128, -128]),
)

def generate_path(
    image_path: str,
    suffix: str,
    *,
    output_dir: str,
    file_extension: str | None = 'png',
    create_directory: bool = True,
) -> str:
    assert output_dir is not None and len(output_dir) > 0, f'Invalid output_dir: {output_dir}. Needs to be not empty'

    if create_directory:
        try:
            os.mkdir(output_dir)
            print(f"Directory '{output_dir}' created successfully.")
        except FileExistsError:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")

    base = os.path.basename(image_path).split('.')
    if file_extension is None:
        return f'{output_dir}/{base[-2]}-{suffix}.{base[-1]}'
    else:
        return f'{output_dir}/{base[-2]}-{suffix}.{file_extension}'
