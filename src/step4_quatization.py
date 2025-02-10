import numpy as np

def quantization(image, quant_matrix, block_size=8):
    """
    Quantize the image.

    Args:
        image (ndarray): DCT-applied image.
        quant_matrix (ndarray): Quantization matrix.
        block_size (int): Size of the block.

    Returns:
        ndarray: Quantized image.
    """
    h, w, _ = image.shape

    # Create a new image
    quantized_image = np.zeros(image.shape)

    # Quantize the image in 8x8 blocks
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i + block_size, j:j + block_size]

            # Apply the quantization matrix
            quantized_block = np.round(block / quant_matrix).astype(np.uint8)

            # Store the quantized block in the new image
            quantized_image[i:i + block_size, j:j + block_size] = quantized_block

    return quantized_image

def main():
    pass

if __name__ == "__main__":
    main()
