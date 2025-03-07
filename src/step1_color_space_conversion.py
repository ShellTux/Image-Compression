from common import DOCS_DIR, IMAGES, cmRed, cmBlue, cmGray, cmGreen, RGB_TO_YCBCR_MATRIX, RGB_TO_YCBCR_OFFSET, YCBCR_TO_RGB_MATRIX, generate_path
import encoder
import matplotlib.pyplot as plt
import numpy as np
import os

def rgb_from_ndarray(img: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r, g, b = np.rollaxis(img, axis=-1)
    return r, g, b

def rgb_to_ycbcr(red: np.ndarray, green: np.ndarray, blue: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert image from RGB to YCbCr color space.

    Args:
        image (ndarray): RGB image.

    Returns:
        ndarray: YCbCr image.
    """

    # TODO(Luís Góis): eu tentei multiplicação de matrizes mas
    # não consigo meter isso a funcionar
    y = 0.299 * red + 0.587 * green + 0.114 * blue
    cb = -0.168736 * red - 0.331264 * green + 0.5 * blue
    cr = 0.5 * red - 0.418688 * green - 0.081312 * blue

    cb += 128
    cr += 128

    return y, cb, cr

def ycbcr_to_rgb(y: np.ndarray, cb: np.ndarray, cr: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert image from YCbCr to RGB color space.

    Args:
        y (ndarray): Y channel
        cb (ndarray): Cb channel
        cr (ndarray): Cr channel

    Returns:
        tuple: (r, g, b) channels
    """
    cb = cb - 128
    cr = cr - 128

    r = y + 1.402 * cr
    g = y - 0.344136 * cb - 0.714136 * cr
    b = y + 1.772 * cb

    return r, g, b

def main():
    for image_path in IMAGES:
        print(f'{image_path=}')

        image = plt.imread(image_path)

        _, intermidate_values = encoder.encoder(image, return_intermidiate_values=True)
        r, g, b = intermidate_values['red'], intermidate_values['green'], intermidate_values['blue']

        y, cb, cr = rgb_to_ycbcr(r, g, b)

        fig, axes = plt.subplots(2, 3, figsize=(12, 8))

        axes[0, 0].imshow(r, cmRed)
        axes[0, 0].set_title('Red Channel')
        axes[0, 0].axis('off')

        axes[0, 1].imshow(g, cmGreen)
        axes[0, 1].set_title('Green Channel')
        axes[0, 1].axis('off')

        axes[0, 2].imshow(b, cmBlue)
        axes[0, 2].set_title('Blue Channel')
        axes[0, 2].axis('off')

        axes[1, 0].imshow(y, cmGray)
        axes[1, 0].set_title('Y Channel')
        axes[1, 0].axis('off')

        axes[1, 1].imshow(cb, cmBlue)
        axes[1, 1].set_title('Cb Channel')
        axes[1, 1].axis('off')

        axes[1, 2].imshow(cr, cmRed)
        axes[1, 2].set_title('Cr Channel')
        axes[1, 2].axis('off')

        plt.tight_layout()
        plt.show()

        image_save_path = generate_path(image_path, 'color-space-conversion', output_dir=DOCS_DIR)
        fig.savefig(image_save_path,bbox_inches='tight', dpi=150)
        print(f'Saved image: {image_save_path}')

if __name__ == "__main__":
    main()
