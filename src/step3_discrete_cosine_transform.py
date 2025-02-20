import numpy as np
from scipy.fftpack import dct as scipy_dct, idct
from itertools import product
import matplotlib.pyplot as plt

def dct_channel(channel: np.ndarray, norm: str = "ortho") -> np.ndarray:
    """
    Aplica a DCT em um canal completo.

    Args:
        channel (np.ndarray): Canal de entrada (Y, Cb ou Cr)
        norm (str): Tipo de normalização a ser usada

    Returns:
        np.ndarray: Canal transformado pela DCT
    """
    # Aplica DCT-2D usando a propriedade de separabilidade
    # Primeiro aplica DCT nas linhas
    dct_rows = scipy_dct(channel, type=2, norm=norm)
    # Depois aplica DCT nas colunas do resultado anterior
    dct_2d = scipy_dct(dct_rows.T, type=2, norm=norm).T
    
    return dct_2d

def idct_channel(channel: np.ndarray, norm: str = "ortho") -> np.ndarray:
    """
    Aplica a IDCT em um canal completo.

    Args:
        channel (np.ndarray): Canal transformado pela DCT
        norm (str): Tipo de normalização a ser usada

    Returns:
        np.ndarray: Canal recuperado
    """
    # Aplica IDCT-2D usando a propriedade de separabilidade
    # Primeiro aplica IDCT nas colunas
    idct_cols = idct(channel.T, type=2, norm=norm).T
    # Depois aplica IDCT nas linhas do resultado anterior
    idct_2d = idct(idct_cols, type=2, norm=norm)
    
    return idct_2d

def apply_dct_to_channels(Y: np.ndarray, Cb: np.ndarray, Cr: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Aplica a DCT nos três canais (Y, Cb, Cr).

    Args:
        Y (np.ndarray): Canal Y
        Cb (np.ndarray): Canal Cb
        Cr (np.ndarray): Canal Cr

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Canais transformados (Y_dct, Cb_dct, Cr_dct)
    """
    Y_dct = dct_channel(Y)
    Cb_dct = dct_channel(Cb)
    Cr_dct = dct_channel(Cr)
    
    return Y_dct, Cb_dct, Cr_dct

def visualize_dct_channels(Y_dct: np.ndarray, Cb_dct: np.ndarray, Cr_dct: np.ndarray):
    """
    Visualiza os canais transformados usando transformação logarítmica.

    Args:
        Y_dct (np.ndarray): Canal Y transformado
        Cb_dct (np.ndarray): Canal Cb transformado
        Cr_dct (np.ndarray): Canal Cr transformado
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Aplica transformação logarítmica e visualiza
    Y_log = np.log(np.abs(Y_dct) + 0.0001)
    Cb_log = np.log(np.abs(Cb_dct) + 0.0001)
    Cr_log = np.log(np.abs(Cr_dct) + 0.0001)
    
    ax1.imshow(Y_log, cmap='gray')
    ax1.set_title('Y DCT')
    ax1.axis('off')
    
    ax2.imshow(Cb_log, cmap='gray')
    ax2.set_title('Cb DCT')
    ax2.axis('off')
    
    ax3.imshow(Cr_log, cmap='gray')
    ax3.set_title('Cr DCT')
    ax3.axis('off')
    
    plt.tight_layout()
    plt.show()

def recover_channels(Y_dct: np.ndarray, Cb_dct: np.ndarray, Cr_dct: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Recupera os canais originais aplicando IDCT.

    Args:
        Y_dct (np.ndarray): Canal Y transformado
        Cb_dct (np.ndarray): Canal Cb transformado
        Cr_dct (np.ndarray): Canal Cr transformado

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Canais recuperados (Y, Cb, Cr)
    """
    Y = idct_channel(Y_dct)
    Cb = idct_channel(Cb_dct)
    Cr = idct_channel(Cr_dct)
    
    return Y, Cb, Cr

def dct(image, block_size=8):
    """
    Apply the Discrete Cosine Transform to the image.

    Args:
        image (ndarray): Downsampled image.
        block_size (int): Size of the block.

    Returns:
        ndarray: DCT-applied image.
    """
    h, w, _ = image.shape

    # Create a new image
    dct_image = np.zeros(image.shape)

    # Apply DCT in 8x8 blocks
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i + block_size, j:j + block_size]

            # Create the DCT matrix
            dct_matrix = np.zeros_like(block)

            # Apply DCT formula
            for u, v, x, y in product(range(block_size), range(block_size), range(block_size), range(block_size)):
                dct_matrix[x, y] += block[x, y] * np.cosh(np.pi * (u + 0.5) / block_size) * np.cos(np.pi * (x + 0.5) / block_size) * np.cos(np.pi * (y + 0.5) / block_size)

            # Store the DCT block in the new image
            dct_image[i:i + block_size, j:j + block_size] = dct_matrix

    return dct_image

def main():
    # Exemplo de uso
    from matplotlib.pyplot import imread
    from common import IMAGES
    from step1_color_space_conversion import rgb_to_ycbcr
    
    print("Iniciando processamento DCT...")
    
    # Carrega uma imagem de teste
    img = imread(IMAGES[0])  # airport.bmp
    print(f"Imagem carregada: {IMAGES[0]}")
    
    # Converte para YCbCr
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    Y, Cb, Cr = rgb_to_ycbcr(r, g, b)
    
    # Aplica DCT
    Y_dct, Cb_dct, Cr_dct = apply_dct_to_channels(Y, Cb, Cr)
    
    # Visualiza os resultados da DCT
    print("\nVisualizando resultados da DCT (usando transformação logarítmica)...")
    visualize_dct_channels(Y_dct, Cb_dct, Cr_dct)

if __name__ == "__main__":
    main()
