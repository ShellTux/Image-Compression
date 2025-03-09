from common import IMAGES, TEST_PARAMETERS
from decoder import decoder
from encoder import encoder
from matplotlib import pyplot as plt
import numpy as np
import cv2
import step10_error_analysis as error_analysis

def main():
    # Parâmetros de teste
    quality_factor = TEST_PARAMETERS['QUALITY-FACTOR']
    downsampling = TEST_PARAMETERS['DOWNSAMPLING']
    interpolation = TEST_PARAMETERS['INTERPOLATION']

    for image_path in IMAGES:
        print(f'\nProcessando imagem: {image_path}')
        print(f'Parâmetros: QF={quality_factor}, Downsampling={downsampling}')

        # Carrega a imagem
        img = plt.imread(image_path)

        # Codifica a imagem
        encoded_data, intermediate_values = encoder(
            img,
            quality_factor=quality_factor,
            downsampling=downsampling,
            interpolation=interpolation,
            return_intermidiate_values=True
        )

        # Decodifica a imagem
        decoded_img = decoder(
            encoded_data,
            quality_factor=quality_factor,
            downsampling=downsampling,
            interpolation=interpolation
        )

        # Calcula a diferença absoluta
        diff = error_analysis.calculate_absolute_difference(img, decoded_img)

        # Visualiza a diferença
        fig = error_analysis.visualize_difference(img, decoded_img, diff)

        # Calcula métricas de erro para a imagem completa
        metrics = error_analysis.calculate_error_metrics(img, decoded_img)
        error_analysis.print_error_metrics(metrics)

        # Extrai os canais originais e reconstruídos para análise por canal
        Y_original = intermediate_values['y']
        Cb_original = intermediate_values['cb']
        Cr_original = intermediate_values['cr']

        # Converte a imagem decodificada para YCbCr para comparação por canal
        r, g, b = cv2.split(decoded_img)
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed = error_analysis.csc.rgb_to_ycbcr(r, g, b)

        # Calcula métricas de erro para cada canal
        channel_metrics = error_analysis.calculate_channel_error_metrics(
            Y_original, Cb_original, Cr_original,
            Y_reconstructed, Cb_reconstructed, Cr_reconstructed
        )

        # Imprime métricas para o canal Y
        error_analysis.print_error_metrics(channel_metrics['Y'], "Y")

        # Mostra a visualização
        plt.show()

if __name__ == '__main__':
    main()
