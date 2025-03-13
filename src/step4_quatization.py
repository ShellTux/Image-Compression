from common import DOCS_DIR, IMAGES, custom_cmap, generate_path
from itertools import product
from matplotlib import pyplot as plt
import argparse
import encoder
import numpy as np

def get_quantization_matrix(quality_factor: int) -> np.ndarray:
    """
    Generates a quantization matrix based on the quality factor.
    The default quality factor is 50, which is typically used as a baseline.

    Args:
        quality_factor (int): Quality factor. quality_factor ϵ [1-100].

    Returns:
        ndarray: Quantization matrix.
    """

    # Standard JPEG quantization matrix for luminance
    jpeg_quantization_matrix = np.array([
        [16, 11, 10, 16, 24,  40,  51,  61],
        [12, 12, 14, 19, 26,  58,  60,  55],
        [14, 13, 16, 24, 40,  57,  69,  56],
        [14, 17, 22, 29, 51,  87,  80,  62],
        [18, 22, 37, 56, 68,  109, 103, 77],
        [24, 35, 55, 64, 81,  104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])

    quality_factor = np.clip(quality_factor, 1, 100)

    if quality_factor < 50:
        scale_factor = 50 / quality_factor
    else:
        scale_factor = (100 - quality_factor) / 50

    if scale_factor == 0:
        return jpeg_quantization_matrix

    quantization_matrix = (jpeg_quantization_matrix * scale_factor).round().clip(0, 255).astype(np.uint8)

    return quantization_matrix

def quantization(
    dct_image: np.ndarray,
    quality_factor: int = 100,
    block_size: int = 8,
) -> np.ndarray:
    """
    This function quantizes the DCT coeficients for each block.

    Args:
        image (ndarray): DCT-applied image.
        quality_factor (int): Quality factor. quality_factor ϵ [1-100].
        block_size (int): Size of the block. Default = 8.

    Returns:
        ndarray: Quantized image.
    """

    h, w = dct_image.shape
    quantized_image = np.zeros_like(dct_image)

    quant_matrix = get_quantization_matrix(quality_factor)

    for i, j in product(range(0, h, block_size), range(0, w, block_size)):
        block = dct_image[i : i + block_size, j : j + block_size]
        quantized_image[i : i + block_size, j : j + block_size] = np.round(block / quant_matrix)

    quantized_image = quantized_image.astype(np.int32)

    return quantized_image

def iquantization(
    quantized_image: np.ndarray,
    quality_factor: int = 100,
    block_size: int = 8
) -> np.ndarray:
    """
    This function dequantizes the quantized image back to DCT coefficients.

    Args:
        quantized_image (ndarray): Quantized image.
        quality_factor (int): Quality factor. quality_factor ϵ [1-100].
        block_size (int): Size of the block. Default = 8.

    Returns:
        ndarray: Dequantized image (approximate DCT coefficients).
    """
    h, w = quantized_image.shape
    dct_image = np.zeros_like(quantized_image)

    quant_matrix = get_quantization_matrix(quality_factor)

    for i, j in product(range(0, h, block_size), range(0, w, block_size)):
        block = quantized_image[i : i + block_size, j : j + block_size]
        dct_image[i : i + block_size, j : j + block_size] = block * quant_matrix

    dct_image = dct_image.astype(np.float32)

    return dct_image

def main():
    parser = argparse.ArgumentParser(description="Quantization")

    parser.add_argument('--hide-figures', action='store_true', help='Disable matplotlib figures')

    args = parser.parse_args()

    show_figures: bool = not args.hide_figures

    for image_path in IMAGES:
        print(f'{image_path=}')
        img = plt.imread(image_path)

        _, iv = encoder.encoder(img, downsampling='4:2:2', return_intermidiate_values=True)

        Y_dct8, Cb_dct8, Cr_dct8 = iv.Y_dct8, iv.Cb_dct8, iv.Cr_dct8

        for quality_factor in (100,):
            Y_q = quantization(Y_dct8, quality_factor=quality_factor)[::8, ::8]
            Cb_q = quantization(Cb_dct8, quality_factor=quality_factor)[::8, ::8]
            Cr_q = quantization(Cr_dct8, quality_factor=quality_factor)[::8, ::8]

            fig, axis = plt.subplots(1, 3, figsize=(15, 5))

            axis[0].imshow(Y_q, cmap=custom_cmap.gray)
            axis[0].set_title('Quantized Y Channel')
            axis[0].axis('off')

            axis[1].imshow(Cb_q, cmap=custom_cmap.gray)
            axis[1].set_title('Quantized Cb Channel')
            axis[1].axis('off')

            axis[2].imshow(Cr_q, cmap=custom_cmap.gray)
            axis[2].set_title('Quantized Cr Channel')
            axis[2].axis('off')

            fig.tight_layout()
            if show_figures:
                plt.show()

            image_save_path = generate_path(image_path, f'quantization-{quality_factor}', output_dir=f'{DOCS_DIR}/step4')
            fig.savefig(image_save_path, bbox_inches='tight', dpi=150)
            print(f'Saved image: {image_save_path}')


if __name__ == "__main__":
    main()
