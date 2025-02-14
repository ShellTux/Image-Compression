import numpy as np
from matplotlib import pyplot as plt
from common import IMAGES
from step0_preprocessing import preprocessing
from step1_color_space_conversion import rgb_to_ycbcr

DEBUG: bool = True

def encoder(img: np.ndarray) -> np.ndarray:
    img = preprocessing(img)
    # TODO(Luís Góis): Add unit test to confirm that the RGB image is 32x32 padded
    ycbcr_image = rgb_to_ycbcr(img)

    return ycbcr_image

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
