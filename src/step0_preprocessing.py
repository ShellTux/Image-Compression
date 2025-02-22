from common import DOCS_DIR, IMAGES, generate_path
from matplotlib import pyplot as plt
import encoder
import numpy as np
import os

def preprocessing(img: np.ndarray) -> np.ndarray:
    img = padding(img, (32, 32))
    return img

def padding(img: np.ndarray, size: tuple) -> np.ndarray:
    """
    Pads an image with zeros to a specified size.

    Args:
        img (np.ndarray): The input image as a NumPy array.
        size (tuple[int, int]): The desired output size (height, width).

    Returns:
        np.ndarray: The padded image.

    Raises:
        TypeError: if img is not a numpy ndarray
        TypeError: if size is not a tuple
        ValueError: If size has the wrong number of elements.
    """
    if not isinstance(img, np.ndarray):
        raise TypeError("img must be a numpy ndarray")
    if not isinstance(size, tuple):
        raise TypeError("size must be a tuple")

    padded_needed = size - (np.array(img.shape) % size)

    return np.pad(img, (0, padded_needed[1]), mode='edge')[:img.shape[0]]

def main():
    for image_path in IMAGES:
        print(f'{image_path=}')

        image = plt.imread(image_path)

        _, intermidiate_values = encoder.encoder(image, return_intermidiate_values=True)
        image_padded = intermidiate_values['image-padded']

        print(f'{image_path} size        = {image.shape}')
        print(f'{image_path} padded size = {image_padded.shape}')

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        axes[0].imshow(image)
        axes[0].set_title('Original Image')
        axes[0].axis('off')

        axes[1].imshow(image_padded)
        axes[1].set_title('Padded Image')
        axes[1].axis('off')

        plt.tight_layout()
        plt.show()

        image_save_path = generate_path(image_path, 'padding', output_dir=DOCS_DIR)
        fig.savefig(image_save_path,bbox_inches='tight', dpi=150)
        print(f'Saved image: {image_save_path}')

if __name__ == '__main__':
    main()
