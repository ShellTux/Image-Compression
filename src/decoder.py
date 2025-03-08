import numpy as np
import cv2
from step1_color_space_conversion import ycbcr_to_rgb
from step2_chrominance_downsampling import upsample_ycbcr
from step3_discrete_cosine_transform import idct_blocks
from step4_quatization import iquantization
from step5_dpcm import dpcm_decode_dc

def decoder(encoded_data, *, quality_factor=75, downsampling='4:2:0', block_size=8, interpolation=cv2.INTER_LINEAR):
    """
    Decodifica uma imagem comprimida.
    
    Args:
        encoded_data (dict): Dados codificados da imagem
        quality_factor (int): Fator de qualidade usado na quantização
        downsampling (str): Método de subamostragem usado
        block_size (int): Tamanho do bloco usado na DCT
        interpolation (int): Método de interpolação para upsampling
        
    Returns:
        np.ndarray: Imagem decodificada em formato RGB
    """
    # Extrai os canais quantizados e codificados
    Y_q = encoded_data['y-q']
    Cb_q = encoded_data['cb-q']
    Cr_q = encoded_data['cr-q']
    
    # Decodifica os coeficientes DC usando DPCM
    Y_dpcm_decoded = dpcm_decode_dc(Y_q, block_size=block_size)
    Cb_dpcm_decoded = dpcm_decode_dc(Cb_q, block_size=block_size)
    Cr_dpcm_decoded = dpcm_decode_dc(Cr_q, block_size=block_size)
    
    # Desquantização
    Y_dq = iquantization(Y_dpcm_decoded, quality_factor=quality_factor, block_size=block_size)
    Cb_dq = iquantization(Cb_dpcm_decoded, quality_factor=quality_factor, block_size=block_size)
    Cr_dq = iquantization(Cr_dpcm_decoded, quality_factor=quality_factor, block_size=block_size)
    
    # IDCT
    Y_idct = idct_blocks(Y_dq, block_size=block_size)
    Cb_idct = idct_blocks(Cb_dq, block_size=block_size)
    Cr_idct = idct_blocks(Cr_dq, block_size=block_size)
    
    # Upsampling (se necessário)
    if downsampling != '4:4:4':
        ycbcr_reconstructed = upsample_ycbcr(Y_idct, Cb_idct, Cr_idct, sampling=downsampling, interpolation=interpolation)
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed = cv2.split(ycbcr_reconstructed)
    else:
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed = Y_idct, Cb_idct, Cr_idct
    
    # Conversão para RGB
    r_reconstructed, g_reconstructed, b_reconstructed = ycbcr_to_rgb(Y_reconstructed, Cb_reconstructed, Cr_reconstructed)
    
    # Monta a imagem RGB reconstruída
    image_reconstructed = cv2.merge([r_reconstructed, g_reconstructed, b_reconstructed])
    
    # Recorta para o tamanho original (remove o padding)
    original_shape = encoded_data.get('original_shape', None)
    if original_shape:
        h, w, _ = original_shape
        image_reconstructed = image_reconstructed[:h, :w]
    
    # Garante que os valores estão no intervalo correto
    image_reconstructed = np.clip(image_reconstructed, 0, 255).astype(np.uint8)
    
    return image_reconstructed
