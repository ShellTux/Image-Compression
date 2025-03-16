from common import VALID_DOWNSAMPLES_TYPE
from encoder import JpegEncodedData
import cv2
import numpy as np
import step0_preprocessing as prep
import step1_color_space_conversion as csc
import step2_chrominance_downsampling as cd
import step3_discrete_cosine_transform as dct
import step4_quatization as quant
import step5_dpcm as dpcm

class JpegDecodedIntermidiateValues:
    Yb_iDPCM: np.ndarray
    Cbb_iDPCM: np.ndarray
    Crb_iDPCM: np.ndarray
    Yb_iQ: np.ndarray
    Cbb_iQ: np.ndarray
    Crb_iQ: np.ndarray
    Yb_iDCT: np.ndarray
    Cbb_iDCT: np.ndarray
    Crb_iDCT: np.ndarray


def decoder(
    encoded_data: JpegEncodedData,
    *,
    downsampling: VALID_DOWNSAMPLES_TYPE = '4:2:0',
    interpolation: int | None = cv2.INTER_LINEAR,
    quality_factor: int = 100,
    block_size: int = 8,
    rle_and_huffman: bool = True,
    return_intermidiate_values: bool = False,
) -> tuple[np.ndarray, JpegDecodedIntermidiateValues]:
    """
    Decodifica uma imagem comprimida.

    Args:
        encoded_data (JpegEncodedData): Dados codificados da imagem
        quality_factor (int): Fator de qualidade usado na quantização
        downsampling (str): Método de subamostragem usado
        block_size (int): Tamanho do bloco usado na DCT
        interpolation (int): Método de interpolação para upsampling

    Returns:
        np.ndarray: Imagem decodificada em formato RGB
    """
    intermidiate_values = JpegDecodedIntermidiateValues()

    if rle_and_huffman:
        pass

    # Extrai os canais quantizados e codificados
    Y_dpcm, Cb_dpcm, Cr_dpcm = encoded_data.Y_dpcm, encoded_data.Cb_dpcm, encoded_data.Cr_dpcm

    # Decodifica os coeficientes DC usando DPCM
    Yb_iDPCM = dpcm.dpcm_decode(Y_dpcm, block_size=block_size)
    Cbb_iDPCM = dpcm.dpcm_decode(Cb_dpcm, block_size=block_size)
    Crb_iDPCM = dpcm.dpcm_decode(Cr_dpcm, block_size=block_size)
    if return_intermidiate_values:
        intermidiate_values.Yb_iDPCM = Yb_iDPCM.copy()
        intermidiate_values.Cbb_iDPCM = Cbb_iDPCM.copy()
        intermidiate_values.Crb_iDPCM = Crb_iDPCM.copy()


    # Desquantização
    Yb_iQ = quant.iquantization(Yb_iDPCM, quality_factor=quality_factor, block_size=block_size)
    Cbb_iQ = quant.iquantization(Cbb_iDPCM, quality_factor=quality_factor, block_size=block_size)
    Crb_iQ = quant.iquantization(Crb_iDPCM, quality_factor=quality_factor, block_size=block_size)
    if return_intermidiate_values:
       intermidiate_values.Yb_iQ  = Yb_iQ.copy()
       intermidiate_values.Cbb_iQ = Cbb_iQ.copy()
       intermidiate_values.Crb_iQ = Crb_iQ.copy()

    # IDCT
    Yb_iDCT = dct.idct_blocks(Yb_iQ, block_size=block_size)
    Cbb_iDCT = dct.idct_blocks(Cbb_iQ, block_size=block_size)
    Crb_iDCT = dct.idct_blocks(Crb_iQ, block_size=block_size)
    if return_intermidiate_values:
        intermidiate_values.Yb_iDCT = Yb_iDCT.copy()
        intermidiate_values.Cbb_iDCT = Cbb_iDCT.copy()
        intermidiate_values.Crb_iDCT = Crb_iDCT.copy()

    # Upsampling (se necessário)
    if downsampling != '4:4:4':
        assert interpolation is not None
        ycbcr_reconstructed = cd.upsample_ycbcr(
            Yb_iDCT,
            Cbb_iDCT,
            Crb_iDCT,
            sampling=downsampling,
            interpolation=interpolation
        )
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed = cv2.split(ycbcr_reconstructed)
    else:
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed = Yb_iDCT, Cbb_iDCT, Crb_iDCT

    # Conversão para RGB
    r_reconstructed, g_reconstructed, b_reconstructed = csc.ycbcr_to_rgb(Y_reconstructed, Cb_reconstructed, Cr_reconstructed)

    # Monta a imagem RGB reconstruída
    image_reconstructed = cv2.merge([r_reconstructed, g_reconstructed, b_reconstructed])

    # Recorta para o tamanho original (remove o padding)
    h, w, _ = encoded_data.original_image_shape
    image_reconstructed = prep.ipadding(image_reconstructed, (h, w))

    # Garante que os valores estão no intervalo correto
    image_reconstructed = image_reconstructed.clip(0, 255).astype(np.uint8)

    return image_reconstructed, intermidiate_values
