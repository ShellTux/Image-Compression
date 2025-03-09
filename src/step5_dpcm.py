from common import DOCS_DIR, IMAGES, TEST_PARAMETERS, generate_path, custom_cmap
from matplotlib import pyplot as plt
import argparse
import cv2
import encoder
import itertools
import numpy as np

def dpcm_encode(quantized_dct_blocks: np.ndarray, block_size: int = 8) -> np.ndarray:
    """
    Realiza a codificação DPCM (Differential Pulse-Code Modulation) dos coeficientes DC.
    Substitui o valor DC pelo valor da diferença em cada bloco.

    Args:
        quantized_dct_blocks (np.ndarray): Blocos DCT quantizados
        block_size (int): Tamanho do bloco (padrão: 8)

    Returns:
        np.ndarray: Blocos com codificação DPCM aplicada
    """
    # Get the number of blocks
    num_blocks = quantized_dct_blocks.shape[0]

    # Ensure output array is the same shape as the input
    dpcm_blocks = np.zeros_like(quantized_dct_blocks)

    # Initialize the previous DC value
    previous_dc = 0

    for i in range(num_blocks):
        # Extract the DC coefficient (top-left corner for a standard DCT block)
        current_dc = quantized_dct_blocks[i, 0]

        # Calculate the difference (DPCM)
        dpcm_dc = current_dc - previous_dc

        # Store the encoded DC value
        dpcm_blocks[i, 0] = dpcm_dc

        # Update the previous DC for the next iteration
        previous_dc = current_dc

    # Copy the rest of the coefficients (AC coefficients) unchanged
    dpcm_blocks[:, 1:] = quantized_dct_blocks[:, 1:]

    return dpcm_blocks
    # Cria uma cópia dos blocos para não modificar o original
    dpcm_blocks = quantized_dct_blocks.copy()

    # Obtém as dimensões da imagem em blocos
    h, w = dpcm_blocks.shape[:2]

    # Valor DC anterior (inicialmente 0)
    prev_dc = 0

    # Percorre todos os blocos
    for i, j in itertools.product(range(h), range(w)):
        # Obtém o valor DC atual (posição 0,0 do bloco)
        current_dc = dpcm_blocks[i, j, 0, 0]

        # Calcula a diferença
        diff = current_dc - prev_dc

        # Substitui o valor DC pela diferença
        dpcm_blocks[i, j, 0, 0] = diff

        # Atualiza o valor DC anterior
        prev_dc = current_dc

    return dpcm_blocks

def dpcm_decode(dpcm_blocks: np.ndarray, block_size: int = 8) -> np.ndarray:
    """
    Realiza a decodificação DPCM (Differential Pulse-Code Modulation) dos coeficientes DC.
    Recupera os valores DC originais a partir das diferenças.

    Args:
        dpcm_blocks (np.ndarray): Blocos com codificação DPCM aplicada
        block_size (int): Tamanho do bloco (padrão: 8)

    Returns:
        np.ndarray: Blocos com os valores DC originais recuperados
    """
    # Get the number of blocks
    num_blocks = dpcm_blocks.shape[0]

    # Ensure output array has the same shape as the input
    decoded_blocks = np.zeros_like(dpcm_blocks)

    # Initialize the previous DC value
    previous_dc = 0

    for i in range(num_blocks):
        # Retrieve the DPCM value (the difference)
        dpcm_dc = dpcm_blocks[i, 0]

        # Calculate the original DC value
        current_dc = previous_dc + dpcm_dc

        # Store the reconstructed DC value
        decoded_blocks[i, 0] = current_dc

        # Update the previous DC for the next iteration
        previous_dc = current_dc

    # Copy the rest of the coefficients (AC coefficients) unchanged
    decoded_blocks[:, 1:] = dpcm_blocks[:, 1:]

    return decoded_blocks
    # Cria uma cópia dos blocos para não modificar o original
    idpcm_blocks = dpcm_blocks.copy()

    # Obtém as dimensões da imagem em blocos
    h, w = idpcm_blocks.shape[:2]

    # Valor DC acumulado (inicialmente 0)
    accumulated_dc = 0

    # Percorre todos os blocos
    for i, j in itertools.product(range(h), range(w)):
        # Obtém a diferença atual
        diff = idpcm_blocks[i, j, 0, 0]

        # Calcula o valor DC original
        original_dc = accumulated_dc + diff

        # Substitui a diferença pelo valor DC original
        idpcm_blocks[i, j, 0, 0] = original_dc

        # Atualiza o valor DC acumulado
        accumulated_dc = original_dc

    return idpcm_blocks

def apply_dpcm_to_channels(
    Y_blocks: np.ndarray,
    Cb_blocks: np.ndarray,
    Cr_blocks: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Aplica a codificação DPCM nos três canais (Y, Cb, Cr).

    Args:
        Y_blocks (np.ndarray): Blocos do canal Y
        Cb_blocks (np.ndarray): Blocos do canal Cb
        Cr_blocks (np.ndarray): Blocos do canal Cr

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Blocos com DPCM aplicado para cada canal
    """
    Y_dpcm = dpcm_encode(Y_blocks)
    Cb_dpcm = dpcm_encode(Cb_blocks)
    Cr_dpcm = dpcm_encode(Cr_blocks)

    return Y_dpcm, Cb_dpcm, Cr_dpcm

def recover_channels_from_dpcm(
    Y_dpcm: np.ndarray,
    Cb_dpcm: np.ndarray,
    Cr_dpcm: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Recupera os canais originais a partir da codificação DPCM.

    Args:
        Y_dpcm (np.ndarray): Blocos do canal Y com DPCM
        Cb_dpcm (np.ndarray): Blocos do canal Cb com DPCM
        Cr_dpcm (np.ndarray): Blocos do canal Cr com DPCM

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Blocos recuperados para cada canal
    """
    Y_recovered = dpcm_decode(Y_dpcm)
    Cb_recovered = dpcm_decode(Cb_dpcm)
    Cr_recovered = dpcm_decode(Cr_dpcm)

    return Y_recovered, Cb_recovered, Cr_recovered

def visualize_dpcm_channels(
    Y_dpcm: np.ndarray,
    Cb_dpcm: np.ndarray,
    Cr_dpcm: np.ndarray,
    *,
    visualize: bool = True,
    image_save_path: str | None = None
):
    """
    Visualiza os canais após a aplicação do DPCM.

    Args:
        Y_dpcm (np.ndarray): Canal Y com DPCM aplicado
        Cb_dpcm (np.ndarray): Canal Cb com DPCM aplicado
        Cr_dpcm (np.ndarray): Canal Cr com DPCM aplicado
        image_save_path (str, optional): Caminho para salvar a imagem. Se None, não salva.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Aplicar log para melhor visualização (valores podem ser muito diferentes)
    log_transform = lambda x: np.log(np.abs(x) + 0.0001)

    # Visualizar cada canal
    axes[0].imshow(log_transform(Y_dpcm), cmap=custom_cmap.gray)
    axes[0].set_title('Yb_DPCM')
    axes[0].axis('off')

    axes[1].imshow(log_transform(Cb_dpcm), cmap=custom_cmap.gray)
    axes[1].set_title('Cbb_DPCM')
    axes[1].axis('off')

    axes[2].imshow(log_transform(Cr_dpcm), cmap=custom_cmap.gray)
    axes[2].set_title('Crb_DPCM')
    axes[2].axis('off')

    plt.tight_layout()

    if visualize:
        plt.show()

    if image_save_path:
        fig.savefig(image_save_path)
        print(f"Imagem DPCM salva em: {image_save_path}")

def visualize_idpcm_channels(
    Y_idpcm: np.ndarray,
    Cb_idpcm: np.ndarray,
    Cr_idpcm: np.ndarray,
    *,
    visualize: bool = True,
    image_save_path: str | None = None
):
    """
    Visualiza os canais após a decodificação do DPCM.

    Args:
        Y_idpcm (np.ndarray): Canal Y com DPCM decodificado
        Cb_idpcm (np.ndarray): Canal Cb com DPCM decodificado
        Cr_idpcm (np.ndarray): Canal Cr com DPCM decodificado
        image_save_path (str, optional): Caminho para salvar a imagem. Se None, não salva.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    log_transform = lambda x: np.log(np.abs(x) + 0.0001)

    # Visualizar cada canal
    axes[0].imshow(log_transform(Y_idpcm), cmap=custom_cmap.gray)
    axes[0].set_title('Yb_iDPCM')
    axes[0].axis('off')

    axes[1].imshow(log_transform(Cb_idpcm), cmap=custom_cmap.gray)
    axes[1].set_title('Cbb_iDPCM')
    axes[1].axis('off')

    axes[2].imshow(log_transform(Cr_idpcm), cmap=custom_cmap.gray)
    axes[2].set_title('Crb_iDPCM')
    axes[2].axis('off')

    plt.tight_layout()

    if image_save_path:
        fig.savefig(image_save_path)
        print(f"Imagem iDPCM salva em: {image_save_path}")

    if visualize:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="DPCM")

    parser.add_argument('--hide-figures', action='store_true', help='Disable matplotlib figures')

    args = parser.parse_args()

    show_figures: bool = not args.hide_figures

    for image_path in IMAGES:
        print(f'{image_path=}')

        image = plt.imread(image_path)

        _, iv = encoder.encoder(
            image,
            downsampling='4:2:2',
            interpolation=TEST_PARAMETERS.interpolation,
            quality_factor=TEST_PARAMETERS.quality_factor,
            return_intermidiate_values=True,
        )

        Yb_dct8, Cbb_dct8, Crb_dct8 = iv.Y_dct8, iv.Cb_dct8, iv.Cr_dct8

        Y_dpcm, Cb_dpcm, Cr_dpcm = apply_dpcm_to_channels(Yb_dct8, Cbb_dct8, Crb_dct8)

        # Visualizar os canais com DPCM
        dpcm_path = generate_path(image_path, "dpcm", output_dir=DOCS_DIR)
        visualize_dpcm_channels(
            Y_dpcm,
            Cb_dpcm,
            Cr_dpcm,
            image_save_path=dpcm_path,
            visualize=show_figures
        )

        # Recuperar os canais originais
        Y_recovered, Cb_recovered, Cr_recovered = recover_channels_from_dpcm(Y_dpcm, Cb_dpcm, Cr_dpcm)

        # Visualizar os canais recuperados
        idpcm_path = generate_path(image_path, "idpcm", output_dir=DOCS_DIR)
        visualize_idpcm_channels(
            Y_recovered,
            Cb_recovered,
            Cr_recovered,
            image_save_path=idpcm_path,
            visualize=show_figures
        )

        # Verificar se a recuperação foi bem-sucedida
        Y_maxerr = np.abs(Yb_dct8 - Y_recovered).max()
        Cb_maxerr = np.abs(Cbb_dct8 - Cb_recovered).max()
        Cr_maxerr = np.abs(Crb_dct8 - Cr_recovered).max()

        print(f"Erro máximo na recuperação do canal Y: {Y_maxerr}")
        print(f"Erro máximo na recuperação do canal Cb: {Cb_maxerr}")
        print(f"Erro máximo na recuperação do canal Cr: {Cr_maxerr}")

if __name__ == "__main__":
    main()
