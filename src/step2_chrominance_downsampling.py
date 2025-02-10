from common import IMAGES
from matplotlib import pyplot as plt
from step1_color_space_conversion import rgb_to_ycbcr
import numpy as np

def downsampling_ycbcr(image: np.ndarray, block_size=8):
    """
    Downsample the Cb and Cr components of the YCbCr image.

    Args:
        image (ndarray): YCbCr image.
        block_size (int): Size of the block.

    Returns:
        ndarray: Downsampled YCbCr image.
    """
    h, w, _ = image.shape
    print(h, w)

    # Create a new image
    downsampled_image = np.zeros((h // block_size, w // block_size, 3))

    # Downsample the image in 8x8 blocks
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i + block_size, j:j + block_size, :]

            # Downsample Cb and Cr components
            cb_downsampled = block[:, :, 1][::2, ::2]
            cr_downsampled = block[:, :, 2][::2, ::2]

            # Store the downsampled block in the new image
            downsampled_image[i // block_size, j // block_size] = [block[:, :, 0].mean(), cb_downsampled.mean(), cr_downsampled.mean()]

    return downsampled_image

def downsample_cbcr(chroma):
    return chroma[::2, ::2]

def upsample_cbcr(downsampled, original_shape):
    return np.repeat(np.repeat(downsampled, 2, axis=0), 2, axis=1)[:original_shape[0], :original_shape[1]]

def main():
    for image in IMAGES:
        print(f'{image=}')

        # NOTE: Load the YCbCr image
        ycbcr_image = rgb_to_ycbcr(plt.imread(image))

        # NOTE: Downsample the image
        downsampled_image = downsampling_ycbcr(ycbcr_image)

        print(downsampled_image)
        break

if __name__ == "__main__":
    main()
