from common import DOCS_DIR, IMAGES, generate_path
from itertools import product
from matplotlib import pyplot as plt
from scipy.fftpack import dct, idct
import encoder
import numpy as np

def dct_channel(channel: np.ndarray, norm: str = "ortho") -> np.ndarray:
    """
    Aplica a DCT em um canal completo.

    Args:
        channel (np.ndarray): Canal de entrada (Y, Cb ou Cr)
        norm (str): Tipo de normalização a ser usada

    Returns:
        np.ndarray: Canal transformado pela DCT
    """
    return dct(dct(channel, type=2, norm="ortho").T, type=2, norm="ortho").T
    # Aplica DCT-2D usando a propriedade de separabilidade
    # Primeiro aplica DCT nas linhas
    dct_rows = dct(channel, type=2, norm=norm)
    # Depois aplica DCT nas colunas do resultado anterior
    dct_2d = dct(dct_rows.T, type=2, norm=norm).T

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
    return idct(idct(channel.T, type=2, norm=norm).T, type=2, norm=norm)
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

def visualize_dct_channels(Y_dct: np.ndarray, Cb_dct: np.ndarray, Cr_dct: np.ndarray, *, image_save_path: str | None = None):
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

    fig.tight_layout()
    plt.show()
    if image_save_path is not None:
        fig.savefig(image_save_path, bbox_inches='tight', dpi=150)

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

def dct_blocks(image: np.ndarray, block_size: int = 8) -> np.ndarray:
    """
    Aplica a DCT em blocos de tamanho block_size x block_size.

    Args:
        image (np.ndarray): Imagem de entrada.
        block_size (int): Tamanho do bloco.

    Returns:
        np.ndarray: Imagem transformada pela DCT.
    """
    h, w = image.shape
    dct_image = np.zeros_like(image)

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i + block_size, j:j + block_size]
            dct_image[i:i + block_size, j:j + block_size] = dct_channel(block)

    return dct_image

def idct_blocks(image: np.ndarray, block_size: int = 8) -> np.ndarray:
    """
    Aplica a IDCT em blocos de tamanho block_size x block_size.

    Args:
        image (np.ndarray): Imagem transformada pela DCT.
        block_size (int): Tamanho do bloco.

    Returns:
        np.ndarray: Imagem recuperada pela IDCT.
    """
    h, w = image.shape
    idct_image = np.zeros_like(image)

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i + block_size, j:j + block_size]
            idct_image[i:i + block_size, j:j + block_size] = idct_channel(block)

    return idct_image

def main():
    for sampling, image_path in product(('4:2:0',), IMAGES):
        print(f'{image_path=}')
        img = plt.imread(image_path)

        # Converte para YCbCr
        _, intermidiate_values = encoder.encoder(img, return_intermidiate_values=True)
        # TODO: We need to apply dct on upscaled downsampled cb and cr
        Y, Cb, Cr = intermidiate_values['y'], intermidiate_values['cb'], intermidiate_values['cr']

        Y_dct, Cb_dct, Cr_dct = apply_dct_to_channels(Y, Cb, Cr)

        # Visualiza os resultados da DCT
        print("Visualizando resultados da DCT (usando transformação logarítmica)...")
        image_save_path = generate_path(image_path, 'dct-logarithmic-transformation', output_dir=DOCS_DIR)
        visualize_dct_channels(Y_dct, Cb_dct, Cr_dct, image_save_path=image_save_path)

        # 7.2.3: Encoder - Aplicar DCT em blocos 8x8
        Y_dct8 = dct_blocks(Y)
        Cb_dct8 = dct_blocks(Cb)
        Cr_dct8 = dct_blocks(Cr)

        # Visualizar as imagens obtidas
        print("Visualizando resultados da DCT em blocos 8x8...")
        image_save_path = generate_path(image_path, 'dct-blocks-8x8', output_dir=DOCS_DIR)
        visualize_dct_channels(Y_dct8, Cb_dct8, Cr_dct8, image_save_path=image_save_path)

        # 7.3: Aplicar DCT em blocos 64x64
        Y_dct64 = dct_blocks(Y, 64)
        Cb_dct64 = dct_blocks(Cb, 64)
        Cr_dct64 = dct_blocks(Cr, 64)

        # Visualizar as imagens obtidas
        print("Visualizando resultados da DCT em blocos 64x64...")
        image_save_path = generate_path(image_path, 'dct-blocks-64x64', output_dir=DOCS_DIR)
        visualize_dct_channels(Y_dct64, Cb_dct64, Cr_dct64, image_save_path=image_save_path)

if __name__ == "__main__":
    main()
