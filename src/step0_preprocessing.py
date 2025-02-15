import numpy as np

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
    print(padded_needed)

    return np.pad(img, (0, padded_needed[1]), mode='edge')[:img.shape[0]]

def main():
    pass

if __name__ == '__main__':
    main()
