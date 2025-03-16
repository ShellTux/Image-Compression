from common import COLOR_CONVERSION, DOCS_DIR, IMAGES, custom_cmap, generate_path
import argparse
import encoder
import matplotlib.pyplot as plt
import numpy as np

def rgb_from_ndarray(img: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return r, g, b

def rgb_to_ycbcr(
    red: np.ndarray,
    green: np.ndarray,
    blue: np.ndarray,
    *,
    matrix_multiplication: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert image from RGB to YCbCr color space using matrix multiplication.

    Args:
        red (ndarray): Red channel of the image.
        green (ndarray): Green channel of the image.
        blue (ndarray): Blue channel of the image.
        matrix_multiplication (bool) [Optional]: use matrix multiplication

    Returns:
        tuple[ndarray, ndarray, ndarray]: Y, Cb, Cr channels.
    """

    # WARN: Matrix multiplication is not working, and Idk why? :(
    if matrix_multiplication:
        rgb = np.stack((red, green, blue), axis=-1)

        ycbcr = rgb @ COLOR_CONVERSION.RGB2YCbCr_matrix + COLOR_CONVERSION.RGB2YCbCr_offset

        y, cb, cr = ycbcr[:, :, 0], ycbcr[:, :, 1], ycbcr[:, :, 2]
    else:
        y = 0.299      * red + 0.587    * green + 0.114    * blue + 0
        cb = -0.168736 * red - 0.331264 * green + 0.5      * blue + 128
        cr = 0.5       * red - 0.418688 * green - 0.081312 * blue + 128

    return y, cb, cr

def ycbcr_to_rgb(
    y: np.ndarray,
    cb: np.ndarray,
    cr: np.ndarray,
    *,
    matrix_multiplication: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert image from YCbCr to RGB color space.

    Args:
        y (ndarray): Y channel
        cb (ndarray): Cb channel
        cr (ndarray): Cr channel
        matrix_multiplication (bool): Use matrix multiplication if True.

    Returns:
        tuple: (r, g, b) channels
    """
    cb = cb - 128
    cr = cr - 128

    if matrix_multiplication:
        channels = np.stack((y, cb, cr), axis=-1)

        rgb = (channels @ COLOR_CONVERSION.YCbCr2RGB_matrix.T).clip(0, 255).astype(np.uint8)

        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    else:
        r = y                 + 1.402    * cr
        g = y - 0.344136 * cb - 0.714136 * cr
        b = y + 1.772    * cb

        r = r.clip(0, 255).astype(np.uint8)
        g = g.clip(0, 255).astype(np.uint8)
        b = b.clip(0, 255).astype(np.uint8)

    return r, g, b

def main():
    parser = argparse.ArgumentParser(description="Color Space Conversion")

    parser.add_argument('--hide-figures', action='store_true', help='Disable matplotlib figures')

    args = parser.parse_args()

    show_figures: bool = not args.hide_figures

    for image_path in IMAGES:
        print(f'{image_path=}')

        image = plt.imread(image_path)

        _, intermidate_values = encoder.encoder(image, return_intermidiate_values=True)
        r, g, b = intermidate_values.red, intermidate_values.green, intermidate_values.blue

        y, cb, cr = rgb_to_ycbcr(r, g, b)

        fig, axes = plt.subplots(2, 3, figsize=(12, 8))

        axes[0, 0].imshow(r, custom_cmap.red)
        axes[0, 0].set_title('Red Channel')
        axes[0, 0].axis('off')

        axes[0, 1].imshow(g, custom_cmap.green)
        axes[0, 1].set_title('Green Channel')
        axes[0, 1].axis('off')

        axes[0, 2].imshow(b, custom_cmap.blue)
        axes[0, 2].set_title('Blue Channel')
        axes[0, 2].axis('off')

        axes[1, 0].imshow(y, custom_cmap.gray)
        axes[1, 0].set_title('Y Channel')
        axes[1, 0].axis('off')

        axes[1, 1].imshow(cb, custom_cmap.blue)
        axes[1, 1].set_title('Cb Channel')
        axes[1, 1].axis('off')

        axes[1, 2].imshow(cr, custom_cmap.red)
        axes[1, 2].set_title('Cr Channel')
        axes[1, 2].axis('off')

        plt.tight_layout()
        if show_figures:
            plt.show()

        image_save_path = generate_path(image_path, 'color-space-conversion', output_dir=f'{DOCS_DIR}/step1')
        fig.savefig(image_save_path,bbox_inches='tight', dpi=150)
        print(f'Saved image: {image_save_path}')

if __name__ == "__main__":
    main()
