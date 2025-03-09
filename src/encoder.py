from common import VALID_DOWNSAMPLES, VALID_DOWNSAMPLES_TYPE
import cv2
import numpy as np
import step0_preprocessing as prep
import step1_color_space_conversion as csc
import step2_chrominance_downsampling as cd
import step3_discrete_cosine_transform as dct
import step4_quatization as quant
import step5_dpcm as dpcm

class JpegEncodedIntermidiateValues:
    original_image: np.ndarray = np.zeros(1)
    original_image_shape: np.ndarray = np.zeros(1)
    red: np.ndarray = np.zeros(1)
    green: np.ndarray = np.zeros(1)
    blue: np.ndarray = np.zeros(1)
    RGB: np.ndarray = np.zeros(1)
    image_padded: np.ndarray = np.zeros(1)
    Y: np.ndarray = np.zeros(1)
    Cb: np.ndarray = np.zeros(1)
    Cr: np.ndarray = np.zeros(1)
    YCbCr: np.ndarray = np.zeros(1)
    Y_d: np.ndarray = np.zeros(1)
    Cb_d: np.ndarray = np.zeros(1)
    Cr_d: np.ndarray = np.zeros(1)
    Y_dct: np.ndarray = np.zeros(1)
    Cb_dct: np.ndarray = np.zeros(1)
    Cr_dct: np.ndarray = np.zeros(1)
    Y_dct8: np.ndarray = np.zeros(1)
    Cb_dct8: np.ndarray = np.zeros(1)
    Cr_dct8: np.ndarray = np.zeros(1)
    Y_q: np.ndarray = np.zeros(1)
    Cb_q: np.ndarray = np.zeros(1)
    Cr_q: np.ndarray = np.zeros(1)
    Y_dpcm: np.ndarray = np.zeros(1)
    Cb_dpcm: np.ndarray = np.zeros(1)
    Cr_dpcm: np.ndarray = np.zeros(1)

class JpegEncodedData:
    original_image_shape: np.ndarray
    downsampling: VALID_DOWNSAMPLES_TYPE
    interpolation: int
    quality_factor: int
    block_size: int

    Y_dpcm: np.ndarray
    Cb_dpcm: np.ndarray
    Cr_dpcm: np.ndarray

    def __init__(
        self,
        *,
        Y_dpcm: np.ndarray,
        Cb_dpcm: np.ndarray,
        Cr_dpcm: np.ndarray,
        quality_factor: int,
        downsampling: VALID_DOWNSAMPLES_TYPE,
        block_size: int,
        image_shape: np.ndarray,
    ) -> None:
        self.Y_dpcm = Y_dpcm
        self.Cb_dpcm = Cb_dpcm
        self.Cr_dpcm = Cr_dpcm
        self.quality_factor = quality_factor
        self.downsampling = downsampling
        self.block_size = block_size
        self.original_image_shape = image_shape

def encoder(
    image: np.ndarray,
    *,
    downsampling: VALID_DOWNSAMPLES_TYPE = '4:2:0',
    interpolation: int | None = cv2.INTER_LINEAR,
    quality_factor: int = 100,
    block_size: int = 8,
    rle_and_huffman: bool = True,
    return_intermidiate_values: bool = False,
) -> tuple[JpegEncodedData, JpegEncodedIntermidiateValues]:
    assert downsampling in VALID_DOWNSAMPLES, f'Invalid downsampling: {downsampling}. Needs to be one of the following: {VALID_DOWNSAMPLES}'

    intermidiate_values = JpegEncodedIntermidiateValues()
    if return_intermidiate_values:
        intermidiate_values.original_image = image.copy()
        intermidiate_values.original_image_shape = np.ndarray(image.shape)

    r, g, b = csc.rgb_from_ndarray(image)
    if return_intermidiate_values:
        intermidiate_values.red = r.copy()
        intermidiate_values.green = g.copy()
        intermidiate_values.blue = b.copy()

    r_padded = prep.preprocessing(r)
    g_padded = prep.preprocessing(g)
    b_padded = prep.preprocessing(b)


    image_padded = cv2.merge([r_padded, g_padded, b_padded])
    if return_intermidiate_values:
        intermidiate_values.image_padded = image_padded.copy()

    # TODO(Luís Góis): Add unit test to confirm that the RGB image is 32x32 padded
    y, cb, cr = csc.rgb_to_ycbcr(r_padded, g_padded, b_padded)
    if return_intermidiate_values:
        intermidiate_values.Y = y.copy()
        intermidiate_values.Cb = cb.copy()
        intermidiate_values.Cr = cr.copy()

    ycbcr = cv2.merge([y, cb, cr])
    if return_intermidiate_values:
        intermidiate_values.YCbCr = ycbcr.copy()

    # TODO: remove or choose another interpolation method
    Y_d, Cb_d, Cr_d = cd.downsample_ycbcr(ycbcr, sampling=downsampling, interpolation=interpolation)
    if return_intermidiate_values:
        intermidiate_values.Y_d = Y_d.copy()
        intermidiate_values.Cb_d = Cb_d.copy()
        intermidiate_values.Cr_d = Cr_d.copy()

    Y_dct, Cb_dct, Cr_dct = dct.apply_dct_to_channels(Y_d, Cb_d, Cr_d)
    if return_intermidiate_values:
        intermidiate_values.Y_dct = Y_dct.copy()
        intermidiate_values.Cb_dct = Cb_dct.copy()
        intermidiate_values.Cr_dct = Cr_dct.copy()

    Y_dct8, Cb_dct8, Cr_dct8 = dct.dct_blocks(Y_d), dct.dct_blocks(Cb_d), dct.dct_blocks(Cr_d)
    if return_intermidiate_values:
        intermidiate_values.Y_dct8 = Y_dct8.copy()
        intermidiate_values.Cb_dct8 = Cb_dct8.copy()
        intermidiate_values.Cr_dct8 = Cr_dct8.copy()

    Y_q = quant.quantization(Y_dct8, quality_factor=quality_factor, block_size=block_size)
    Cb_q = quant.quantization(Cb_dct8, quality_factor=quality_factor, block_size=block_size)
    Cr_q = quant.quantization(Cr_dct8, quality_factor=quality_factor, block_size=block_size)
    if return_intermidiate_values:
        intermidiate_values.Y_q = Y_q.copy()
        intermidiate_values.Cb_q = Cb_q.copy()
        intermidiate_values.Cr_q = Cr_q.copy()

    Y_dpcm = dpcm.dpcm_encode(Y_q, block_size=block_size)
    Cb_dpcm = dpcm.dpcm_encode(Cb_q, block_size=block_size)
    Cr_dpcm = dpcm.dpcm_encode(Cr_q, block_size=block_size)
    if return_intermidiate_values:
        intermidiate_values.Y_dpcm = Y_dpcm.copy()
        intermidiate_values.Cb_dpcm = Cb_dpcm.copy()
        intermidiate_values.Cr_dpcm = Cr_dpcm.copy()

    if rle_and_huffman:
        pass

    encoded_data = JpegEncodedData(
        Y_dpcm=Y_dpcm,
        Cb_dpcm=Cb_dpcm,
        Cr_dpcm=Cr_dpcm,
        quality_factor=quality_factor,
        downsampling=downsampling,
        block_size=block_size,
        image_shape=np.array(image.shape),
    )

    return encoded_data, intermidiate_values
