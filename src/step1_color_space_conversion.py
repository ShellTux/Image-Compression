import numpy as np
import matplotlib.pyplot as plt

from common import IMAGES

def rgb_from_ndarray(img: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r, g, b = np.rollaxis(img, axis=-1)
    return r, g, b

def rgb_to_ycbcr(rgb_image: np.ndarray):
    """
    Convert image from RGB to YCbCr color space.

    Args:
        image (ndarray): RGB image.

    Returns:
        ndarray: YCbCr image.
    """
    r, g, b = rgb_from_ndarray(rgb_image)

    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 128 + (-0.168736 * r - 0.331264 * g + 0.5 * b)
    cr = 128 + (0.5 * r - 0.418688 * g - 0.081312 * b)

    return np.stack([y, cb, cr], axis=-1)

def ycbcr_to_rgb(ycbcr_img):
    ycbcr = ycbcr_img.astype(np.float32)
    ycbcr[..., [1,2]] -= 128
    matrix = np.array([[1, 0, 1.402],
                       [1, -0.34414, -0.71414],
                       [1, 1.772, 0]])
    return np.clip(np.dot(ycbcr, matrix.T), 0, 255).astype(np.uint8)

def main():
    for image in IMAGES:
        print(f'{image=}')

        image = plt.imread(image)

        ycbcr_image = rgb_to_ycbcr(image)

        print(ycbcr_image)
        break

if __name__ == "__main__":
    main()
