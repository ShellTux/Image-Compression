import numpy as np
import matplotlib.pyplot as plt

from common import IMAGES, RGB_TO_YCBCR_MATRIX, RGB_TO_YCBCR_OFFSET, YCBCR_TO_RGB_MATRIX

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

def ycbcr_to_rgb(ycbcr_img):
    ycbcr = ycbcr_img.astype(np.float32)
    ycbcr[..., [1,2]] -= 128
    return ycbcr.dot(YCBCR_TO_RGB_MATRIX).clip(0, 255).astype(np.uint8)

def main():
    for image in IMAGES:
        print(f'{image=}')

        image = plt.imread(image)

        r, g, b = rgb_from_ndarray(image)

        y, cb, cr = rgb_to_ycbcr(r, g, b)

        print(y, cb, cr)
        break

if __name__ == "__main__":
    main()
