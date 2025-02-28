from common import VALID_DOWNSAMPLES, VALID_DOWNSAMPLES_TYPE
import cv2
import numpy as np
import step0_preprocessing as prep
import step1_color_space_conversion as csc
import step2_chrominance_downsampling as cd

from step3_discrete_cosine_transform import apply_dct_to_channels, dct_blocks
from step4_quatization import quantization

def encoder(
    image: np.ndarray,
    *,
    downsampling: VALID_DOWNSAMPLES_TYPE = '4:2:0',
    interpolation: int | None = cv2.INTER_LINEAR,
    quality_factor: int = 100,
    block_size: int = 8,
    return_intermidiate_values: bool = False,
) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    assert downsampling in VALID_DOWNSAMPLES, f'Invalid downsampling: {downsampling}. Needs to be one of the following: {VALID_DOWNSAMPLES}'

    intermidiate_values: dict[str, np.ndarray] = dict()

    if return_intermidiate_values:
        intermidiate_values['image'] = image.copy()

    r, g, b = csc.rgb_from_ndarray(image)
    if return_intermidiate_values:
        intermidiate_values['red'] = r.copy()
        intermidiate_values['green'] = g.copy()
        intermidiate_values['blue'] = b.copy()

    r_padded = prep.preprocessing(r)
    g_padded = prep.preprocessing(g)
    b_padded = prep.preprocessing(b)


    image_padded = cv2.merge([r_padded, g_padded, b_padded])
    if return_intermidiate_values:
        intermidiate_values['image-padded'] = image_padded.copy()

    # TODO(Luís Góis): Add unit test to confirm that the RGB image is 32x32 padded
    y, cb, cr = csc.rgb_to_ycbcr(r_padded, g_padded, b_padded)
    if return_intermidiate_values:
        intermidiate_values['y'] = y.copy()
        intermidiate_values['cb'] = cb.copy()
        intermidiate_values['cr'] = cr.copy()

    ycbcr = cv2.merge([y, cb, cr])
    if return_intermidiate_values:
        intermidiate_values['ycbcr'] = ycbcr.copy()

    # TODO: remove or choose another interpolation method
    Y_d, Cb_d, Cr_d = cd.downsample_ycbcr(ycbcr, sampling=downsampling, interpolation=interpolation)
    if return_intermidiate_values:
        intermidiate_values['y-downsampled'] = Y_d.copy()
        intermidiate_values['cb-downsampled'] = Cb_d.copy()
        intermidiate_values['cr-downsampled'] = Cr_d.copy()

    Y_dct, Cb_dct, Cr_dct = apply_dct_to_channels(Y_d, Cb_d, Cr_d)
    if return_intermidiate_values:
        intermidiate_values['y-dct'] = Y_dct.copy()
        intermidiate_values['cb-dct'] = Cb_dct.copy()
        intermidiate_values['cr-dct'] = Cr_dct.copy()

    Y_dct8, Cb_dct8, Cr_dct8 = dct_blocks(Y_d), dct_blocks(Cb_d), dct_blocks(Cr_d)
    if return_intermidiate_values:
        intermidiate_values['y-dct8'] = Y_dct8.copy()
        intermidiate_values['cb-dct8'] = Cb_dct8.copy()
        intermidiate_values['cr-dct8'] = Cr_dct8.copy()

    Y_q = quantization(Y_dct, quality_factor=quality_factor, block_size=block_size)
    CB_q = quantization(Cb_dct, quality_factor=quality_factor, block_size=block_size)
    Cr_q = quantization(Cr_dct, quality_factor=quality_factor, block_size=block_size)
    if return_intermidiate_values:
        intermidiate_values['y-q'] = Y_q.copy()
        intermidiate_values['cb-q'] = CB_q.copy()
        intermidiate_values['cr-q'] = Cr_q.copy()

    return np.zeros(1), intermidiate_values
