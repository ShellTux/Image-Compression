from common import DOCS_DIR, VALID_DOWNSAMPLES_TYPE, generate_path, TEST_PARAMETERS
import argparse
import cv2
import encoder
import matplotlib.pyplot as plt
import numpy as np
import step1_color_space_conversion as csc
import step2_chrominance_downsampling as cd
import step3_discrete_cosine_transform as dct
import step4_quatization as quant

def calculate_absolute_difference(original: np.ndarray, reconstructed: np.ndarray) -> np.ndarray:
    """
    Calcula a diferença absoluta entre a imagem original e reconstruída.

    Args:
        original (np.ndarray): Imagem original
        reconstructed (np.ndarray): Imagem reconstruída

    Returns:
        np.ndarray: Diferença absoluta entre as imagens
    """
    return np.abs(original.astype(float) - reconstructed.astype(float))

def calculate_error_metrics(original: np.ndarray, reconstructed: np.ndarray) -> dict:
    """
    Calcula várias métricas de erro entre a imagem original e reconstruída.

    Args:
        original (np.ndarray): Imagem original
        reconstructed (np.ndarray): Imagem reconstruída

    Returns:
        dict: Dicionário com as métricas de erro calculadas
    """
    # Converte para float para evitar overflow em cálculos
    original = original.astype(float)
    reconstructed = reconstructed.astype(float)

    # Calcula a diferença absoluta
    diff = np.abs(original - reconstructed)

    # Diferença máxima e mínima
    max_diff = np.max(diff)
    min_diff = np.min(diff)
    avg_diff = np.mean(diff)

    # Erro Médio ao Quadrado (MSE)
    mse = np.mean((original - reconstructed) ** 2)

    # Raiz Quadrada do MSE (RMSE)
    rmse = np.sqrt(mse)

    # Potência do sinal original
    signal_power = np.mean(original ** 2)

    # Rácio Sinal-Ruído (SNR) em dB
    snr = 10 * np.log10(signal_power / mse) if mse > 0 else float('inf')

    # Valor máximo do sinal original
    max_signal = np.max(original) ** 2

    # Rácio Sinal-Ruído do Pico (PSNR) em dB
    psnr = 10 * np.log10(max_signal / mse) if mse > 0 else float('inf')

    metrics = {
        'max_diff': max_diff,
        'min_diff': min_diff,
        'avg_diff': avg_diff,
        'mse': mse,
        'rmse': rmse,
        'snr': snr,
        'psnr': psnr
    }

    return metrics

def calculate_channel_error_metrics(
    Y_original: np.ndarray,
    Cb_original: np.ndarray,
    Cr_original: np.ndarray,
    Y_reconstructed: np.ndarray,
    Cb_reconstructed: np.ndarray,
    Cr_reconstructed: np.ndarray,
) -> dict:
    """
    Calcula métricas de erro para cada canal de cor (Y, Cb, Cr).

    Args:
        Y_original, Cb_original, Cr_original: Canais originais
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed: Canais reconstruídos

    Returns:
        dict: Dicionário com as métricas de erro para cada canal
    """
    metrics = {
        'Y': calculate_error_metrics(Y_original, Y_reconstructed),
        'Cb': calculate_error_metrics(Cb_original, Cb_reconstructed),
        'Cr': calculate_error_metrics(Cr_original, Cr_reconstructed),
    }

    return metrics

def visualize_difference(
    original: np.ndarray,
    reconstructed: np.ndarray,
    diff: np.ndarray,
    title: str = "Diferença entre imagens",
):
    """
    Visualiza a imagem original, reconstruída e a diferença entre elas.

    Args:
        original (np.ndarray): Imagem original
        reconstructed (np.ndarray): Imagem reconstruída
        diff (np.ndarray): Diferença entre as imagens
        title (str): Título para a visualização
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Imagem original
    axes[0].imshow(original)
    axes[0].set_title('Img Orig')
    axes[0].axis('off')

    # Imagem reconstruída
    axes[1].imshow(reconstructed)
    axes[1].set_title('Img Reconstr')
    axes[1].axis('off')

    # Diferença entre as imagens (amplificada para melhor visualização)
    # Normaliza a diferença para melhor visualização
    diff_normalized = diff / np.max(diff) if np.max(diff) > 0 else diff
    axes[2].imshow(diff_normalized, cmap='gray')
    axes[2].set_title('Imagem diferenças')
    axes[2].axis('off')

    plt.tight_layout()
    return fig

def print_error_metrics(metrics, channel_name=""):
    """
    Imprime as métricas de erro de forma formatada.

    Args:
        metrics (dict): Dicionário com as métricas de erro
        channel_name (str): Nome do canal (opcional)
    """
    prefix = f"Erros no canal {channel_name}:" if channel_name else "Erros na imagem:"
    print(f"\n{prefix}")
    print(f"Max diff: {metrics['max_diff']}")
    print(f"Avg diff: {metrics['avg_diff']}")

    if not channel_name:
        print(f"\nErros na imagem de 3 canais reconstruída:")
        print(f"MSE = {metrics['mse']}")
        print(f"RMSE = {metrics['rmse']}")
        print(f"SNR = {metrics['snr']}")
        print(f"PSNR = {metrics['psnr']}")

def reconstruct_image(image_path, quality_factor=75, downsampling: VALID_DOWNSAMPLES_TYPE = '4:2:0', interpolation=cv2.INTER_LINEAR):
    """
    Processa uma imagem através do pipeline de compressão e descompressão.

    Args:
        image_path (str): Caminho para a imagem
        quality_factor (int): Fator de qualidade para quantização
        downsampling (str): Método de subamostragem
        interpolation (int): Método de interpolação

    Returns:
        tuple: (imagem original, imagem reconstruída, valores intermediários)
    """
    # Carrega a imagem
    image = plt.imread(image_path)

    # Processa a imagem usando o encoder
    _, iv = encoder.encoder(
        image,
        quality_factor=quality_factor,
        downsampling=downsampling,
        interpolation=interpolation,
        return_intermidiate_values=True
    )

    # Extrai os canais originais
    Y_original = iv.Y
    Cb_original = iv.Cb
    Cr_original = iv.Cr

    # Extrai os canais quantizados
    Y_q = iv.Y_q
    Cb_q = iv.Cb_q
    Cr_q = iv.Cr_q

    # Desquantização
    Y_dq = quant.iquantization(Y_q, quality_factor=quality_factor)
    Cb_dq = quant.iquantization(Cb_q, quality_factor=quality_factor)
    Cr_dq = quant.iquantization(Cr_q, quality_factor=quality_factor)

    # IDCT
    Y_idct = dct.idct_blocks(Y_dq)
    Cb_idct = dct.idct_blocks(Cb_dq)
    Cr_idct = dct.idct_blocks(Cr_dq)

    # Upsampling (se necessário)
    if downsampling != '4:4:4':
        ycbcr_reconstructed = cd.upsample_ycbcr(Y_idct, Cb_idct, Cr_idct, sampling=downsampling, interpolation=interpolation)
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed = cv2.split(ycbcr_reconstructed)
    else:
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed = Y_idct, Cb_idct, Cr_idct

    # Conversão para RGB
    r_reconstructed, g_reconstructed, b_reconstructed = csc.ycbcr_to_rgb(Y_reconstructed, Cb_reconstructed, Cr_reconstructed)

    # Monta a imagem RGB reconstruída
    image_reconstructed = cv2.merge([r_reconstructed, g_reconstructed, b_reconstructed])

    # Recorta para o tamanho original (remove o padding)
    h, w, _ = image.shape
    image_reconstructed = image_reconstructed[:h, :w]

    # Garante que os valores estão no intervalo correto
    image_reconstructed = np.clip(image_reconstructed, 0, 255).astype(np.uint8)

    return image, image_reconstructed, iv, (Y_original, Cb_original, Cr_original), (Y_reconstructed, Cb_reconstructed, Cr_reconstructed)

def main():
    parser = argparse.ArgumentParser(description="Error Analysis")

    parser.add_argument('--hide-figures', action='store_true', help='Disable matplotlib figures')

    args = parser.parse_args()

    show_figures: bool = not args.hide_figures

    # Parâmetros de teste
    image_path = TEST_PARAMETERS.image_path
    quality_factor = TEST_PARAMETERS.quality_factor
    downsampling = TEST_PARAMETERS.downsampling
    interpolation = TEST_PARAMETERS.interpolation

    print(f"Analisando imagem: {image_path}")
    print(f"Parâmetros: QF={quality_factor}, Downsampling={downsampling}")

    # Reconstrói a imagem
    original, reconstructed, intermediate_values, original_channels, reconstructed_channels = reconstruct_image(
        image_path, quality_factor, downsampling, interpolation
    )

    # Extrai os canais
    Y_original, Cb_original, Cr_original = original_channels
    Y_reconstructed, Cb_reconstructed, Cr_reconstructed = reconstructed_channels

    # Calcula a diferença absoluta
    diff = calculate_absolute_difference(original, reconstructed)

    # Visualiza a diferença
    fig = visualize_difference(original, reconstructed, diff)

    # Calcula métricas de erro para a imagem completa
    metrics = calculate_error_metrics(original, reconstructed)
    print_error_metrics(metrics)

    # Calcula métricas de erro para cada canal
    channel_metrics = calculate_channel_error_metrics(
        Y_original, Cb_original, Cr_original,
        Y_reconstructed, Cb_reconstructed, Cr_reconstructed
    )

    # Imprime métricas para cada canal
    print_error_metrics(channel_metrics['Y'], "Y")

    if show_figures:
        plt.show()

    # Salva a visualização
    image_save_path = generate_path(image_path, f'error-analysis-qf{quality_factor}-{downsampling.replace(":", "")}', output_dir=DOCS_DIR)
    fig.savefig(image_save_path, bbox_inches='tight', dpi=150)
    print(f'Imagem salva em: {image_save_path}')

if __name__ == "__main__":
    main()
