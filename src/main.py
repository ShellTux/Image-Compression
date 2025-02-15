import numpy as np
from matplotlib import pyplot as plt
from common import IMAGES
from step0_preprocessing import preprocessing
from step1_color_space_conversion import rgb_from_ndarray, rgb_to_ycbcr

DEBUG: bool = True

def encoder(img: np.ndarray) -> np.ndarray:
    r, g, b = rgb_from_ndarray(img)
    r = preprocessing(r)
    g = preprocessing(g)
    b = preprocessing(b)

    # TODO(Luís Góis): Add unit test to confirm that the RGB image is 32x32 padded
    _ = rgb_to_ycbcr(r, g, b)

    return np.zeros(1)

def decoder(img: np.ndarray) -> np.ndarray:
    return img

def main():
    for image in IMAGES:
        print(f'{image=}')

        img = plt.imread(image)

        jpeg_img = encoder(img)
        if DEBUG:
            print(f'{jpeg_img=}')


        decoded_img = decoder(jpeg_img)
        if DEBUG:
            print(f'{decoded_img=}')

        break

if __name__ == '__main__':
    main()
