from common import IMAGES
from decoder import decoder
from encoder import encoder
from matplotlib import pyplot as plt

DEBUG: bool = True

def main():
    for image in IMAGES:
        print(f'{image=}')

        img = plt.imread(image)

        jpeg_img, _ = encoder(img)
        if DEBUG:
            print(f'{jpeg_img=}')


        decoded_img = decoder(jpeg_img)
        if DEBUG:
            print(f'{decoded_img=}')

        break

if __name__ == '__main__':
    main()
