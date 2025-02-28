import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import cv2
from matplotlib import pyplot as plt
from step1_color_space_conversion import rgb_to_ycbcr, ycbcr_to_rgb
from step2_chrominance_downsampling import downsample_ycbcr, upsample_ycbcr
from step3_discrete_cosine_transform import dct_blocks, idct_blocks
from step4_quatization import quantization, iquantization


def normalize_for_display(image, use_log=False):
    """
    Normaliza a imagem para visualização, mantendo o fundo escuro
    (valores baixos → preto, valores altos → branco).
    """
    if use_log:
        # Transformação logarítmica para ampliar variações em valores pequenos
        display = np.log(np.abs(image) + 1e-3)
    else:
        # Sem log, apenas valor absoluto
        display = np.abs(image)
    
    # Normaliza entre 0 e 1
    img_min = np.min(display)
    img_max = np.max(display)
    if img_max == img_min:
        return np.zeros_like(display)  # Evita divisão por zero
    
    normalized = (display - img_min) / (img_max - img_min)
    return normalized


def visualize_channels(Y, Cb, Cr, title_prefix="", use_log=False):
    """
    Visualiza os três canais lado a lado, mantendo fundo escuro
    e detalhes claros.
    """
    fig = plt.figure(figsize=(20, 5))
    gs = plt.GridSpec(1, 3, width_ratios=[2, 1, 1], wspace=0.1)
    
    Y_norm = normalize_for_display(Y, use_log=use_log)
    Cb_norm = normalize_for_display(Cb, use_log=use_log)
    Cr_norm = normalize_for_display(Cr, use_log=use_log)
    
    ax1 = plt.subplot(gs[0])
    ax1.imshow(Y_norm, cmap='gray', aspect='auto')
    ax1.set_title(f'Y{title_prefix}')
    ax1.axis('off')
    
    ax2 = plt.subplot(gs[1])
    ax2.imshow(Cb_norm, cmap='gray', aspect='auto')
    ax2.set_title(f'Cb{title_prefix}')
    ax2.axis('off')
    
    ax3 = plt.subplot(gs[2])
    ax3.imshow(Cr_norm, cmap='gray', aspect='auto')
    ax3.set_title(f'Cr{title_prefix}')
    ax3.axis('off')
    
    plt.tight_layout(pad=1.2)
    plt.show()


def pad_to_multiple_of_8(image):
    """Adiciona padding para garantir que as dimensões são múltiplas de 8."""
    h, w = image.shape
    new_h = ((h + 7) // 8) * 8
    new_w = ((w + 7) // 8) * 8
    padded = np.pad(image, ((0, new_h - h), (0, new_w - w)), mode='edge')
    return padded


def dpcm_encode_dc(quantized_blocks, block_size=8):
    """
    Codifica os coeficientes DC usando DPCM.
    
    Args:
        quantized_blocks (ndarray): Blocos quantizados
        block_size (int): Tamanho do bloco (padrão: 8)
    
    Returns:
        ndarray: Blocos com coeficientes DC codificados
    """
    h, w = quantized_blocks.shape
    encoded = quantized_blocks.copy()
    
    # Para cada bloco, pegamos apenas o coeficiente DC (posição 0,0)
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            if i == 0 and j == 0:
                # Primeiro bloco mantém o valor original
                continue
            
            # Pega o coeficiente DC do bloco atual
            current_dc = encoded[i, j]
            
            # Pega o coeficiente DC do bloco anterior
            if j == 0:  # Primeira coluna, pega o bloco da linha anterior
                prev_i = i - block_size
                prev_j = w - block_size
            else:  # Outros casos, pega o bloco anterior na mesma linha
                prev_i = i
                prev_j = j - block_size
            
            prev_dc = encoded[prev_i, prev_j]
            
            # Codifica a diferença
            encoded[i, j] = current_dc - prev_dc
    
    return encoded


def dpcm_decode_dc(encoded_blocks, block_size=8):
    """
    Decodifica os coeficientes DC usando DPCM.
    
    Args:
        encoded_blocks (ndarray): Blocos com coeficientes DC codificados
        block_size (int): Tamanho do bloco (padrão: 8)
    
    Returns:
        ndarray: Blocos com coeficientes DC decodificados
    """
    h, w = encoded_blocks.shape
    decoded = encoded_blocks.copy()
    
    # Para cada bloco, recuperamos o coeficiente DC original
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            if i == 0 and j == 0:
                # Primeiro bloco mantém o valor original
                continue
            
            # Pega a diferença codificada
            diff = decoded[i, j]
            
            # Pega o coeficiente DC do bloco anterior
            if j == 0:  # Primeira coluna, pega o bloco da linha anterior
                prev_i = i - block_size
                prev_j = w - block_size
            else:  # Outros casos, pega o bloco anterior na mesma linha
                prev_i = i
                prev_j = j - block_size
            
            prev_dc = decoded[prev_i, prev_j]
            
            # Decodifica o valor original
            decoded[i, j] = diff + prev_dc
    
    return decoded


def test_dpcm():
    """
    Testa a codificação e decodificação DPCM.
    Demonstra que podemos recuperar os valores originais após codificação/decodificação.
    """
    # Carrega e processa a imagem
    image = cv2.imread("imagens/airport.bmp")
    if image is None:
        raise FileNotFoundError("Imagem não encontrada")
    
    # Converte BGR para RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Converte para YCbCr
    Y, Cb, Cr = rgb_to_ycbcr(image_rgb[:,:,0], image_rgb[:,:,1], image_rgb[:,:,2])
    
    # Garante dimensões múltiplas de 8
    Y = pad_to_multiple_of_8(Y)
    Cb = pad_to_multiple_of_8(Cb)
    Cr = pad_to_multiple_of_8(Cr)
    
    # Aplica DCT
    Y_dct = dct_blocks(Y)
    Cb_dct = dct_blocks(Cb)
    Cr_dct = dct_blocks(Cr)
    
    # Quantização
    Y_q = quantization(Y_dct)
    Cb_q = quantization(Cb_dct)
    Cr_q = quantization(Cr_dct)
    
    # 9.3 - Codificação DPCM
    Y_dpcm = dpcm_encode_dc(Y_q)
    Cb_dpcm = dpcm_encode_dc(Cb_q)
    Cr_dpcm = dpcm_encode_dc(Cr_q)
    
    # 9.4 - Decodificação DPCM
    Yb_iDPCM = dpcm_decode_dc(Y_dpcm)
    Cb_iDPCM = dpcm_decode_dc(Cb_dpcm)
    Cr_iDPCM = dpcm_decode_dc(Cr_dpcm)
    
    # 9.5 - Verifica se os valores foram recuperados corretamente
    print("\nVerificando recuperação dos valores originais:")
    print("Y_q recuperado corretamente:", np.allclose(Y_q, Yb_iDPCM))
    print("Cb_q recuperado corretamente:", np.allclose(Cb_q, Cb_iDPCM))
    print("Cr_q recuperado corretamente:", np.allclose(Cr_q, Cr_iDPCM))
    
    # Visualiza os resultados
    print("\nVisualizando canais após DPCM:")
    visualize_channels(Y_dpcm, Cb_dpcm, Cr_dpcm, "_DPCM", use_log=True)

    print("\nVisualizando canais após decodificação DPCM:")
    visualize_channels(Yb_iDPCM, Cb_iDPCM, Cr_iDPCM, "_iDPCM", use_log=False)

    print("\nVisualizando canais após quantização (original):")
    visualize_channels(Y_q, Cb_q, Cr_q, "_iQ", use_log=False)
    

    
    # Mostra os blocos na ordem especificada
    print("\nYb_DPCM [8:16, 8:16]")
    print(np.array2string(Y_dpcm[8:16, 8:16], separator='   ', prefix=''))
    
    print("\nYb_iDPCM [8:16, 8:16]")
    print(np.array2string(Yb_iDPCM[8:16, 8:16], separator='   ', prefix=''))
    
    print("\nQY")
    # Matriz de quantização JPEG padrão para luminância
    QY = np.array([
        [ 8,  6,  5,  8, 12, 20, 26, 30],
        [ 6,  6,  7, 10, 13, 29, 30, 28],
        [ 7,  6,  8, 12, 20, 28, 34, 28],
        [ 7,  8, 11, 14, 26, 44, 40, 31],
        [ 9, 11, 18, 28, 34, 54, 52, 38],
        [12, 18, 28, 32, 40, 52, 56, 46],
        [24, 32, 39, 44, 52, 60, 60, 50],
        [36, 46, 48, 49, 56, 50, 52, 50]
    ])
    print(np.array2string(QY, separator='  ', prefix=''))
    
    print("\nYb_iQ [8:16, 8:16]")
    print(np.array2string(Y_q[8:16, 8:16], separator='.    ', formatter={'float_kind':lambda x: "%.1f" % x}, prefix=''))


if __name__ == "__main__":
    test_dpcm()