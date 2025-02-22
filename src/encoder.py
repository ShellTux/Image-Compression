from common import VALID_DOWNSAMPLES, VALID_DOWNSAMPLES_TYPE
from step0_preprocessing import preprocessing
from step1_color_space_conversion import rgb_from_ndarray, rgb_to_ycbcr
from step2_chrominance_downsampling import downsample_ycbcr
import cv2
import numpy as np

def encoder(image: np.ndarray, *, downsampling: VALID_DOWNSAMPLES_TYPE = '4:2:0', return_intermidiate_values: bool = False) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    assert downsampling in VALID_DOWNSAMPLES, f'Invalid downsampling: {downsampling}. Needs to be one of the following: {VALID_DOWNSAMPLES}'

    intermidiate_values: dict[str, np.ndarray] = dict()

    if return_intermidiate_values:
        intermidiate_values['image'] = image.copy()

    r_padded, g_padded, b_padded = rgb_from_ndarray(image)
    if return_intermidiate_values:
        intermidiate_values['red'] = r_padded.copy()
        intermidiate_values['green'] = g_padded.copy()
        intermidiate_values['blue'] = b_padded.copy()

    r_padded = preprocessing(r_padded)
    g_padded = preprocessing(g_padded)
    b_padded = preprocessing(b_padded)

    image_padded = cv2.merge([r_padded, g_padded, b_padded])
    if return_intermidiate_values:
        intermidiate_values['image-padded'] = image_padded.copy()

    # TODO(Luís Góis): Add unit test to confirm that the RGB image is 32x32 padded
    y, cb, cr = rgb_to_ycbcr(r_padded, g_padded, b_padded)
    if return_intermidiate_values:
        intermidiate_values['y'] = y.copy()
        intermidiate_values['cb'] = cb.copy()
        intermidiate_values['cr'] = cr.copy()

    ycbcr = cv2.merge([y, cb, cr])
    if return_intermidiate_values:
        intermidiate_values['ycbcr'] = ycbcr.copy()

    # TODO: remove or choose another interpolation method
    y_d, cb_d, cr_d = downsample_ycbcr(ycbcr, sampling=downsampling, interpolation=cv2.INTER_CUBIC)
    if return_intermidiate_values:
        intermidiate_values['y-downsampled'] = y_d.copy()
        intermidiate_values['cb-downsampled'] = cb_d.copy()
        intermidiate_values['cr-downsampled'] = cr_d.copy()

    return np.zeros(1), intermidiate_values
