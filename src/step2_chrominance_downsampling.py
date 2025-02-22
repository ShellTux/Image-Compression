from common import DEFAULT_DOWNSAMPLE, IMAGES, VALID_DOWNSAMPLES, VALID_DOWNSAMPLES_TYPE
from matplotlib import pyplot as plt
from step1_color_space_conversion import rgb_to_ycbcr, ycbcr_to_rgb
import numpy as np
import cv2

def downsample_ycbcr(ycbcr_image: np.ndarray, sampling: VALID_DOWNSAMPLES_TYPE = DEFAULT_DOWNSAMPLE, interpolation=cv2.INTER_LINEAR):
    """
    Realiza a sub-amostragem dos canais YCbCr com diferentes formatos suportados pelo JPEG.

    Args:
        image (ndarray): Imagem no espaço YCbCr.
        sampling (str): Método de sub-amostragem, pode ser "4:2:0" ou "4:2:2".
        interpolation (int): Método de interpolação do OpenCV.

    Returns:
        tuple: Y_d, Cb_d, Cr_d (canais subamostrados)
    """

    assert sampling in VALID_DOWNSAMPLES, f'Invalid downsampling: {downsampling}. Needs to be one of the following: {VALID_DOWNSAMPLES}'

    Y, Cb, Cr = cv2.split(ycbcr_image)
    h, w = Y.shape

    if sampling == "4:2:0":
        Cb_d = cv2.resize(Cb, (w // 2, h // 2), interpolation=interpolation)
        Cr_d = cv2.resize(Cr, (w // 2, h // 2), interpolation=interpolation)
    elif sampling == "4:2:2":
        Cb_d = cv2.resize(Cb, (w // 2, h), interpolation=interpolation)
        Cr_d = cv2.resize(Cr, (w // 2, h), interpolation=interpolation)
    else:
        raise ValueError(f"Invalid sampling value: {sampling}. Use '4:2:0' or '4:2:2'.")

    return Y, Cb_d, Cr_d

def upsample_ycbcr(Y: np.ndarray, Cb_d: np.ndarray, Cr_d: np.ndarray, sampling: VALID_DOWNSAMPLES_TYPE = DEFAULT_DOWNSAMPLE, interpolation=cv2.INTER_LINEAR):
    """
    Reverte a sub-amostragem, restaurando os canais Cb e Cr ao tamanho original.

    Args:
        Y (ndarray): Canal de luminância original.
        Cb_d (ndarray): Canal Cb subamostrado.
        Cr_d (ndarray): Canal Cr subamostrado.
        sampling (str): Método de sub-amostragem aplicado anteriormente.
        interpolation (int): Método de interpolação do OpenCV.

    Returns:
        ndarray: Imagem reconstruída no espaço YCbCr.
    """
    h, w = Y.shape

    assert sampling in VALID_DOWNSAMPLES, f'Invalid downsampling: {downsampling}. Needs to be one of the following: {VALID_DOWNSAMPLES}'

    if sampling == "4:2:0":
        Cb_u = cv2.resize(Cb_d, (w, h), interpolation=interpolation)
        Cr_u = cv2.resize(Cr_d, (w, h), interpolation=interpolation)
    elif sampling == "4:2:2":
        Cb_u = cv2.resize(Cb_d, (w, h), interpolation=interpolation)
        Cr_u = cv2.resize(Cr_d, (w, h), interpolation=interpolation)
    else:
        raise ValueError(f"Invalid sampling value: {sampling}. Use '4:2:0' or '4:2:2'.")

    return cv2.merge([Y, Cb_u, Cr_u])

def main():
    for image in IMAGES:
        print(f'Processando imagem: {image}')

        # Carregar imagem RGB
        image_rgb = plt.imread(image)

        # Separar os canais RGB e converter para YCbCr
        r, g, b = cv2.split(image_rgb)
        y, cb, cr = rgb_to_ycbcr(r, g, b)
        image_ycbcr = cv2.merge([y, cb, cr])

        # Mostrar dimensões originais
        print(f"Dimensões originais: {image_ycbcr.shape}")

        # Encoder - Downsampling 4:2:0
        Y_d, Cb_d, Cr_d = downsample_ycbcr(image_ycbcr, sampling="4:2:0", interpolation=cv2.INTER_CUBIC)

        # Mostrar dimensões depois da compressão
        print(f"Dimensão Y_d: {Y_d.shape}")
        print(f"Dimensão Cb_d: {Cb_d.shape}")
        print(f"Dimensão Cr_d: {Cr_d.shape}")

        # Visualizar os canais subamostrados
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 3, 1)
        plt.imshow(Y_d, cmap="gray")
        plt.title("Y_d downsampling")

        plt.subplot(1, 3, 2)
        plt.imshow(Cb_d, cmap="gray")
        plt.title("Cb_d downsampling")

        plt.subplot(1, 3, 3)
        plt.imshow(Cr_d, cmap="gray")
        plt.title("Cr_d downsampling")

        plt.show()

        # Decoder - Reconstrução (upsampling)
        image_reconstructed = upsample_ycbcr(Y_d, Cb_d, Cr_d, sampling="4:2:0", interpolation=cv2.INTER_CUBIC)

        # Converter de volta para RGB para comparação
        y_r, cb_r, cr_r = cv2.split(image_reconstructed)
        r, g, b = ycbcr_to_rgb(y_r, cb_r, cr_r)
        image_rgb_reconstructed = cv2.merge([r, g, b])

        image_rgb_reconstructed = np.clip(image_rgb_reconstructed, 0, 255).astype(np.uint8)

        # Mostrar imagem reconstruída
        plt.figure()
        plt.imshow(image_rgb_reconstructed.astype(np.uint8))
        plt.title("Imagem Reconstruída")
        plt.show()

        # Comparação com a imagem original
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(image_rgb.astype(np.uint8))
        plt.title("Imagem Original")

        plt.subplot(1, 2, 2)
        plt.imshow(image_rgb_reconstructed.astype(np.uint8))
        plt.title("Imagem Reconstruída")

        plt.show()

        break  # Processa apenas a primeira imagem para teste

if __name__ == "__main__":
    main()
