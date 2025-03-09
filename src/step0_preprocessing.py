from common import DOCS_DIR, IMAGES, generate_path
from matplotlib import pyplot as plt
import argparse
import cv2
import encoder
import numpy as np

def preprocessing(img: np.ndarray) -> np.ndarray:
    img = padding(img, (32, 32))
    return img

def padding(img: np.ndarray, size: tuple[int, int]) -> np.ndarray:
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
    if len(size) != 2:
        raise ValueError("size must have two elements")

    mod = np.array(size)
    pad_needed = mod - (img.shape % mod)
    pad_needed = (
        (0, pad_needed[0]),
        (0, pad_needed[1]),
    )

    padded_img = np.pad(img, pad_needed, mode='edge')

    return padded_img

def main():
    parser = argparse.ArgumentParser(description="Preprocessing")

    parser.add_argument('--hide-figures', action='store_true', help='Disable matplotlib figures')

    args = parser.parse_args()

    show_figures: bool = not args.hide_figures

    for image_path in IMAGES:
        print(f'{image_path=}')

        image = plt.imread(image_path)

        _, intermidiate_values = encoder.encoder(image, return_intermidiate_values=True)
        r, g, b = intermidiate_values.red, intermidiate_values.green, intermidiate_values.blue

        r_p, g_p, b_p = preprocessing(r), preprocessing(g), preprocessing(b)
        image_padded = cv2.merge([r_p, g_p, b_p])

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
        if show_figures:
            plt.show()

        image_save_path = generate_path(image_path, 'padding', output_dir=DOCS_DIR)
        fig.savefig(image_save_path,bbox_inches='tight', dpi=150)
        print(f'Saved image: {image_save_path}')

if __name__ == '__main__':
    main()
