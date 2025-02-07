#!/usr/bin/env python

from matplotlib import colors as clr, pyplot as plt
import argparse
import numpy as np

cmRed = clr.LinearSegmentedColormap.from_list("red", [(0,0,0),(1,0,0)], N = 256)
cmGreen = clr.LinearSegmentedColormap.from_list("red", [(0,0,0),(0,1,0)], N = 256)
cmBlue = clr.LinearSegmentedColormap.from_list("red", [(0,0,0),(0,0,1)], N = 256)
cmGray = clr.LinearSegmentedColormap.from_list("gray", [(0,0,0),(1,1,1)], N = 256)

# NOTE: ex 3.4
def encoder(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    return R, G, B

# NOTE: ex 3.5
def decoder(R,G,B):
    nl, nc = R.shape
    imgRec = np.zeros((nl, nc, 3)).astype(np.uint8)
    imgRec[:,:,0] = R
    imgRec[:,:,1] = G
    imgRec[:,:,2] = B
    return imgRec

# NOTE: ex 4.1
def padding(img):
    pass


# NOTE: ex 3.2
def criarColorMap():
    R = float(input("Valor R [0-1]: "))
    G = float(input("Valor G [0-1]: "))
    B = float(input("Valor B [0-1]: "))
    cmPersonalizado = clr.LinearSegmentedColormap.from_list("personalizado", [(0,0,0),(R,G,B)], N = 256)
    return cmPersonalizado


# NOTE: ex 3.3
def showImg(img, title, cmap = None):
    plt.figure()
    plt.imshow(img, cmap)
    plt.axis('off')
    plt.title(title)
    plt.show()

def showSubMatrix(img, i, j, canal, dim):
    print(img[i:i+dim, j:j+dim, canal])

def main():
    # NOTE: Change this value for a different default image
    default_image = './images/airport.bmp'

    parser = argparse.ArgumentParser(description='Read an image file and convert it to a NumPy array.')
    parser.add_argument('image_path', nargs='?', type=str, default=default_image, help='The path to the image file to be read.')

    args = parser.parse_args()

    # NOTE: ex 3.1
    image_filepath = args.image_path
    img = plt.imread(image_filepath)

    print(type(img))
    print(img.shape)
    print(img[8:16, 8:16, 0])
    print(img.dtype)
    # showSubMatrix(img, 0, 0, 2, 8)

    showImg(img, image_filepath)
    R,G,B = encoder(img)

    imgRec = decoder(R,G,B)

    # NOTE: ex 3.5
    showImg(R, "Red", cmRed)
    showImg(G, "Green", cmGreen)
    showImg(B, "Blue", cmBlue)
    showImg(G, "Gray", cmGray)

    # cmPersonalizado = criarColorMap()
    # showImg(G, "Personalizado", cmPersonalizado)

    print(imgRec[8:16, 8:16, 0])
    showImg(imgRec, "Decodificada")


if __name__ == "__main__":
    main()
