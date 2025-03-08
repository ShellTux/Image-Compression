import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import cv2
import matplotlib.pyplot as plt
from common import IMAGES, QUALITIES, generate_path, DOCS_DIR
from encoder import encoder
from decoder import decoder
import step10_error_analysis as error_analysis

def analyze_image_with_parameters(image_path, quality_factors, downsampling_methods):
    """
    Analisa uma imagem com diferentes parâmetros de qualidade e métodos de subamostragem.
    
    Args:
        image_path (str): Caminho para a imagem
        quality_factors (list): Lista de fatores de qualidade a serem testados
        downsampling_methods (list): Lista de métodos de subamostragem a serem testados
    """
    # Carrega a imagem
    image = plt.imread(image_path)
    image_name = os.path.basename(image_path).split('.')[0]
    
    # Cria tabelas para armazenar os resultados
    results = []
    
    # Processa a imagem com diferentes parâmetros
    for quality_factor in quality_factors:
        for downsampling in downsampling_methods:
            print(f"\nProcessando {image_name} com QF={quality_factor}, Downsampling={downsampling}")
            
            # Codifica a imagem
            encoded_data, _ = encoder(
                image, 
                quality_factor=quality_factor,
                downsampling=downsampling,
                return_intermidiate_values=True
            )
            
            # Decodifica a imagem
            decoded_img = decoder(
                encoded_data,
                quality_factor=quality_factor,
                downsampling=downsampling
            )
            
            # Calcula a diferença absoluta
            diff = error_analysis.calculate_absolute_difference(image, decoded_img)
            
            # Calcula métricas de erro
            metrics = error_analysis.calculate_error_metrics(image, decoded_img)
            
            # Visualiza a diferença
            fig = error_analysis.visualize_difference(
                image, decoded_img, diff, 
                title=f"{image_name} - QF={quality_factor}, DS={downsampling}"
            )
            
            # Salva a visualização
            save_path = generate_path(
                image_path, 
                f'error-analysis-qf{quality_factor}-{downsampling.replace(":", "")}', 
                output_dir=DOCS_DIR
            )
            fig.savefig(save_path, bbox_inches='tight', dpi=150)
            print(f'Imagem salva em: {save_path}')
            
            # Armazena os resultados
            results.append({
                'image': image_name,
                'quality_factor': quality_factor,
                'downsampling': downsampling,
                'mse': metrics['mse'],
                'rmse': metrics['rmse'],
                'snr': metrics['snr'],
                'psnr': metrics['psnr'],
                'max_diff': metrics['max_diff'],
                'avg_diff': metrics['avg_diff']
            })
            
            # Imprime as métricas
            print(f"MSE = {metrics['mse']}")
            print(f"RMSE = {metrics['rmse']}")
            print(f"SNR = {metrics['snr']} dB")
            print(f"PSNR = {metrics['psnr']} dB")
            print(f"Max diff = {metrics['max_diff']}")
            print(f"Avg diff = {metrics['avg_diff']}")
            
            plt.close(fig)  # Fecha a figura para liberar memória
    
    return results

def plot_quality_comparison(results, metric='psnr'):
    """
    Plota um gráfico comparando os resultados para diferentes fatores de qualidade.
    
    Args:
        results (list): Lista de resultados
        metric (str): Métrica a ser comparada ('mse', 'rmse', 'snr', 'psnr')
    """
    # Agrupa os resultados por imagem e método de subamostragem
    grouped_results = {}
    for result in results:
        key = (result['image'], result['downsampling'])
        if key not in grouped_results:
            grouped_results[key] = []
        grouped_results[key].append(result)
    
    # Cria o gráfico
    plt.figure(figsize=(12, 8))
    
    for (image, downsampling), group in grouped_results.items():
        # Ordena por fator de qualidade
        group.sort(key=lambda x: x['quality_factor'])
        
        # Extrai os dados para o gráfico
        quality_factors = [item['quality_factor'] for item in group]
        metric_values = [item[metric] for item in group]
        
        # Plota a linha
        plt.plot(quality_factors, metric_values, marker='o', label=f"{image} - {downsampling}")
    
    # Configura o gráfico
    plt.xlabel('Fator de Qualidade')
    plt.ylabel(metric.upper())
    plt.title(f'Comparação de {metric.upper()} para diferentes fatores de qualidade')
    plt.grid(True)
    plt.legend()
    
    # Salva o gráfico
    save_path = os.path.join(DOCS_DIR, f'quality_comparison_{metric}.png')
    plt.savefig(save_path, bbox_inches='tight', dpi=150)
    print(f'Gráfico salvo em: {save_path}')
    
    plt.show()

def plot_downsampling_comparison(results, metric='psnr'):
    """
    Plota um gráfico comparando os resultados para diferentes métodos de subamostragem.
    
    Args:
        results (list): Lista de resultados
        metric (str): Métrica a ser comparada ('mse', 'rmse', 'snr', 'psnr')
    """
    # Agrupa os resultados por imagem e fator de qualidade
    grouped_results = {}
    for result in results:
        key = (result['image'], result['quality_factor'])
        if key not in grouped_results:
            grouped_results[key] = []
        grouped_results[key].append(result)
    
    # Cria o gráfico
    plt.figure(figsize=(10, 6))
    
    # Define as posições das barras
    bar_width = 0.35
    index = np.arange(len(grouped_results))
    
    # Extrai os métodos de subamostragem únicos
    downsampling_methods = sorted(list(set(result['downsampling'] for result in results)))
    
    # Plota as barras para cada método de subamostragem
    for i, downsampling in enumerate(downsampling_methods):
        values = []
        labels = []
        
        for (image, quality_factor), group in grouped_results.items():
            # Encontra o resultado para este método de subamostragem
            for result in group:
                if result['downsampling'] == downsampling:
                    values.append(result[metric])
                    labels.append(f"{image}\nQF={quality_factor}")
                    break
        
        # Plota as barras
        plt.bar(index + i * bar_width, values, bar_width, label=downsampling)
    
    # Configura o gráfico
    plt.xlabel('Imagem e Fator de Qualidade')
    plt.ylabel(metric.upper())
    plt.title(f'Comparação de {metric.upper()} para diferentes métodos de subamostragem')
    plt.xticks(index + bar_width / 2, labels, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    # Salva o gráfico
    save_path = os.path.join(DOCS_DIR, f'downsampling_comparison_{metric}.png')
    plt.savefig(save_path, bbox_inches='tight', dpi=150)
    print(f'Gráfico salvo em: {save_path}')
    
    plt.show()

def main():
    """Função principal para análise de resultados."""
    # Parâmetros a serem testados
    quality_factors = QUALITIES  # [75, 50, 25]
    downsampling_methods = ['4:2:0', '4:2:2']
    
    # Lista para armazenar todos os resultados
    all_results = []
    
    # Processa cada imagem
    for image_path in IMAGES:
        results = analyze_image_with_parameters(image_path, quality_factors, downsampling_methods)
        all_results.extend(results)
    
    # Plota gráficos comparativos
    plot_quality_comparison(all_results, 'psnr')
    plot_quality_comparison(all_results, 'mse')
    plot_downsampling_comparison(all_results, 'psnr')
    
    # Imprime uma tabela resumo
    print("\n\nTabela Resumo de Resultados:")
    print("Imagem | QF | DS | MSE | RMSE | SNR (dB) | PSNR (dB) | Max Diff | Avg Diff")
    print("-" * 100)
    
    for result in all_results:
        print(f"{result['image']} | {result['quality_factor']} | {result['downsampling']} | "
              f"{result['mse']:.2f} | {result['rmse']:.2f} | {result['snr']:.2f} | "
              f"{result['psnr']:.2f} | {result['max_diff']:.2f} | {result['avg_diff']:.2f}")

if __name__ == "__main__":
    main()