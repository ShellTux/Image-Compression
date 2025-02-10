import numpy as np
from itertools import product

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
    pass

if __name__ == "__main__":
    main()
