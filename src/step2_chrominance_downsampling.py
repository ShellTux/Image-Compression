from common import DEFAULT_DOWNSAMPLE, DOCS_DIR, IMAGES, VALID_DOWNSAMPLES, VALID_DOWNSAMPLES_TYPE, generate_path
from itertools import product
from matplotlib import pyplot as plt
import cv2
import encoder
import numpy as np
import step1_color_space_conversion as csc

def downsample_ycbcr(
        ycbcr_image: np.ndarray,
        sampling: VALID_DOWNSAMPLES_TYPE = DEFAULT_DOWNSAMPLE,
        interpolation=cv2.INTER_LINEAR
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Realiza a sub-amostragem dos canais YCbCr com diferentes formatos suportados pelo JPEG.

    Args:
        ycbcr_image (ndarray): Imagem no espaço YCbCr.
        sampling (str): Método de sub-amostragem.
        interpolation (int): Método de interpolação do OpenCV.

    Returns:
        tuple: Y_d, Cb_d, Cr_d (canais subamostrados)
    """

    assert sampling in VALID_DOWNSAMPLES, f'Invalid downsampling: {downsampling}. Needs to be one of the following: {VALID_DOWNSAMPLES}'

    Y, Cb, Cr = cv2.split(ycbcr_image)
    h, w = Y.shape

    if sampling == "4:2:0":
        Cb_d = cv2.resize(Cb, (w // 2, h // 2), interpolation=interpolation)
        Cr_d = cv2.resize(Cr, (w // 2, h // 2), interpolation=interpolation)
    elif sampling == "4:2:2":
        Cb_d = cv2.resize(Cb, (w // 2, h), interpolation=interpolation)
        Cr_d = cv2.resize(Cr, (w // 2, h), interpolation=interpolation)
    else:
        raise ValueError(f"Invalid sampling value: {sampling}. Use '4:2:0' or '4:2:2'.")

    return Y, Cb_d, Cr_d

def upsample_ycbcr(
        Y: np.ndarray,
        Cb_d: np.ndarray,
        Cr_d: np.ndarray,
        sampling: VALID_DOWNSAMPLES_TYPE = DEFAULT_DOWNSAMPLE,
        interpolation=cv2.INTER_LINEAR
) -> np.ndarray:
    """
    Reverte a sub-amostragem, restaurando os canais Cb e Cr ao tamanho original.

    Args:
        Y (ndarray): Canal de luminância.
        Cb_d (ndarray): Canal Cb subamostrado.
        Cr_d (ndarray): Canal Cr subamostrado.
        sampling (str): Método de sub-amostragem aplicado anteriormente.
        interpolation (int): Método de interpolação do OpenCV.

    Returns:
        ndarray: Imagem reconstruída no espaço YCbCr.
    """
    h, w = Y.shape

    assert sampling in VALID_DOWNSAMPLES, f'Invalid downsampling: {downsampling}. Needs to be one of the following: {VALID_DOWNSAMPLES}'

    if sampling == "4:2:0":
        Cb_u = cv2.resize(Cb_d, (w, h), interpolation=interpolation)
        Cr_u = cv2.resize(Cr_d, (w, h), interpolation=interpolation)
    elif sampling == "4:2:2":
        Cb_u = cv2.resize(Cb_d, (w, h), interpolation=interpolation)
        Cr_u = cv2.resize(Cr_d, (w, h), interpolation=interpolation)
    else:
        raise ValueError(f"Invalid sampling value: {sampling}. Use '4:2:0' or '4:2:2'.")

    return cv2.merge([Y, Cb_u, Cr_u])

def main():
    interpolation = cv2.INTER_CUBIC
    for sampling, image_path in product(('4:2:2', '4:2:0'), IMAGES):
        print(f'{image_path=}, {sampling=}')

        image_rgb = plt.imread(image_path)

        _, intermidiate_values = encoder.encoder(image_rgb, return_intermidiate_values=True)

        image_ycbcr = intermidiate_values['ycbcr']

        print(f"Dimensões originais: {image_ycbcr.shape}")

        Y, Cb, Cr = cv2.split(image_ycbcr)
        Y_d, Cb_d, Cr_d = downsample_ycbcr(image_ycbcr, sampling=sampling, interpolation=interpolation)

        print(f"Dimensão Y_d: {Y_d.shape}")
        print(f"Dimensão Cb_d: {Cb_d.shape}")
        print(f"Dimensão Cr_d: {Cr_d.shape}")

        fig, axes = plt.subplots(2, 3, figsize=(12, 8))

        axes[0, 0].imshow(Y, cmap='gray')
        axes[0, 0].set_title('Y original')
        axes[0, 0].axis('off')

        axes[0, 1].imshow(Cb, cmap='cool')
        axes[0, 1].set_title('Cb original')
        axes[0, 1].axis('off')

        axes[0, 2].imshow(Cr, cmap='hot')
        axes[0, 2].set_title('Cr original')
        axes[0, 2].axis('off')

        axes[1, 0].imshow(Y_d, cmap='gray')
        axes[1, 0].set_title('Y downsampled')
        axes[1, 0].axis('off')

        axes[1, 1].imshow(Cb_d, cmap='cool')
        axes[1, 1].set_title('Cb downsampled')
        axes[1, 1].axis('off')

        axes[1, 2].imshow(Cr_d, cmap='hot')
        axes[1, 2].set_title('Cr downsampled')
        axes[1, 2].axis('off')

        fig.tight_layout()
        plt.show()

        image_save_path = generate_path(image_path, f'downsampling-{sampling}', output_dir=DOCS_DIR)
        fig.savefig(image_save_path, bbox_inches='tight', dpi=150)
        print(f'Saved image: {image_save_path}')

        # Decoder - Reconstrução (upsampling)
        image_reconstructed = upsample_ycbcr(Y_d, Cb_d, Cr_d, sampling=sampling, interpolation=interpolation)

        # Converter de volta para RGB para comparação
        y_r, cb_r, cr_r = cv2.split(image_reconstructed)
        r, g, b = csc.ycbcr_to_rgb(y_r, cb_r, cr_r)
        image_rgb_reconstructed = cv2.merge([r, g, b]).clip(0, 255).astype(np.uint8)

        # Comparação com a imagem original
        fig, axes = plt.subplots(1, 2)

        axes[0].imshow(image_rgb)
        axes[0].set_title('Imagem Original')
        axes[0].axis('off')

        axes[1].imshow(image_rgb_reconstructed)
        axes[1].set_title('Imagem Reconstruída')
        axes[1].axis('off')

        fig.tight_layout()
        plt.show()

        image_save_path = generate_path(image_path, f'downsampling-{sampling}-reconstruction-comparison', output_dir=DOCS_DIR)
        fig.savefig(image_save_path, bbox_inches='tight', dpi=150)
        print(f'Saved image: {image_save_path}')

if __name__ == "__main__":
    main()
