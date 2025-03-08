from common import DOCS_DIR, IMAGES, generate_path
from matplotlib import pyplot as plt
import numpy as np
import os
from itertools import product

def dpcm_encode(dct_blocks: np.ndarray, block_size: int = 8) -> np.ndarray:
    """
    Realiza a codificação DPCM (Differential Pulse-Code Modulation) dos coeficientes DC.
    Substitui o valor DC pelo valor da diferença em cada bloco.
    
    Args:
        dct_blocks (np.ndarray): Blocos DCT quantizados
        block_size (int): Tamanho do bloco (padrão: 8)
        
    Returns:
        np.ndarray: Blocos com codificação DPCM aplicada
    """
    # Cria uma cópia dos blocos para não modificar o original
    dpcm_blocks = dct_blocks.copy()
    
    # Obtém as dimensões da imagem em blocos
    h, w = dpcm_blocks.shape[:2]
    
    # Valor DC anterior (inicialmente 0)
    prev_dc = 0
    
    # Percorre todos os blocos
    for i in range(h):
        for j in range(w):
            # Obtém o valor DC atual (posição 0,0 do bloco)
            current_dc = dpcm_blocks[i, j, 0, 0]
            
            # Calcula a diferença
            diff = current_dc - prev_dc
            
            # Substitui o valor DC pela diferença
            dpcm_blocks[i, j, 0, 0] = diff
            
            # Atualiza o valor DC anterior
            prev_dc = current_dc
    
    return dpcm_blocks

def dpcm_decode(dpcm_blocks: np.ndarray, block_size: int = 8) -> np.ndarray:
    """
    Realiza a decodificação DPCM (Differential Pulse-Code Modulation) dos coeficientes DC.
    Recupera os valores DC originais a partir das diferenças.
    
    Args:
        dpcm_blocks (np.ndarray): Blocos com codificação DPCM aplicada
        block_size (int): Tamanho do bloco (padrão: 8)
        
    Returns:
        np.ndarray: Blocos com os valores DC originais recuperados
    """
    # Cria uma cópia dos blocos para não modificar o original
    idpcm_blocks = dpcm_blocks.copy()
    
    # Obtém as dimensões da imagem em blocos
    h, w = idpcm_blocks.shape[:2]
    
    # Valor DC acumulado (inicialmente 0)
    accumulated_dc = 0
    
    # Percorre todos os blocos
    for i in range(h):
        for j in range(w):
            # Obtém a diferença atual
            diff = idpcm_blocks[i, j, 0, 0]
            
            # Calcula o valor DC original
            original_dc = accumulated_dc + diff
            
            # Substitui a diferença pelo valor DC original
            idpcm_blocks[i, j, 0, 0] = original_dc
            
            # Atualiza o valor DC acumulado
            accumulated_dc = original_dc
    
    return idpcm_blocks

def apply_dpcm_to_channels(Y_blocks: np.ndarray, Cb_blocks: np.ndarray, Cr_blocks: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Aplica a codificação DPCM nos três canais (Y, Cb, Cr).
    
    Args:
        Y_blocks (np.ndarray): Blocos do canal Y
        Cb_blocks (np.ndarray): Blocos do canal Cb
        Cr_blocks (np.ndarray): Blocos do canal Cr
        
    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Blocos com DPCM aplicado para cada canal
    """
    Y_dpcm = dpcm_encode(Y_blocks)
    Cb_dpcm = dpcm_encode(Cb_blocks)
    Cr_dpcm = dpcm_encode(Cr_blocks)
    
    return Y_dpcm, Cb_dpcm, Cr_dpcm

def recover_channels_from_dpcm(Y_dpcm: np.ndarray, Cb_dpcm: np.ndarray, Cr_dpcm: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Recupera os canais originais a partir da codificação DPCM.
    
    Args:
        Y_dpcm (np.ndarray): Blocos do canal Y com DPCM
        Cb_dpcm (np.ndarray): Blocos do canal Cb com DPCM
        Cr_dpcm (np.ndarray): Blocos do canal Cr com DPCM
        
    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Blocos recuperados para cada canal
    """
    Y_recovered = dpcm_decode(Y_dpcm)
    Cb_recovered = dpcm_decode(Cb_dpcm)
    Cr_recovered = dpcm_decode(Cr_dpcm)
    
    return Y_recovered, Cb_recovered, Cr_recovered

def visualize_dpcm_channels(Y_dpcm: np.ndarray, Cb_dpcm: np.ndarray, Cr_dpcm: np.ndarray, *, image_save_path: str | None = None):
    """
    Visualiza os canais após a aplicação do DPCM.
    
    Args:
        Y_dpcm (np.ndarray): Canal Y com DPCM aplicado
        Cb_dpcm (np.ndarray): Canal Cb com DPCM aplicado
        Cr_dpcm (np.ndarray): Canal Cr com DPCM aplicado
        image_save_path (str, optional): Caminho para salvar a imagem. Se None, não salva.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Aplicar log para melhor visualização (valores podem ser muito diferentes)
    def log_transform(x):
        return np.log(np.abs(x) + 0.0001)
    
    # Visualizar cada canal
    axes[0].imshow(log_transform(Y_dpcm[:, :, 0, 0]), cmap='gray')
    axes[0].set_title('Yb_DPCM')
    axes[0].axis('off')
    
    axes[1].imshow(log_transform(Cb_dpcm[:, :, 0, 0]), cmap='gray')
    axes[1].set_title('Cbb_DPCM')
    axes[1].axis('off')
    
    axes[2].imshow(log_transform(Cr_dpcm[:, :, 0, 0]), cmap='gray')
    axes[2].set_title('Crb_DPCM')
    axes[2].axis('off')
    
    plt.tight_layout()
    
    if image_save_path:
        # Garantir que o diretório exista
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        plt.savefig(image_save_path)
        print(f"Imagem DPCM salva em: {image_save_path}")
    
    # Sempre mostrar a imagem
    plt.show()

def visualize_idpcm_channels(Y_idpcm: np.ndarray, Cb_idpcm: np.ndarray, Cr_idpcm: np.ndarray, *, image_save_path: str | None = None):
    """
    Visualiza os canais após a decodificação do DPCM.
    
    Args:
        Y_idpcm (np.ndarray): Canal Y com DPCM decodificado
        Cb_idpcm (np.ndarray): Canal Cb com DPCM decodificado
        Cr_idpcm (np.ndarray): Canal Cr com DPCM decodificado
        image_save_path (str, optional): Caminho para salvar a imagem. Se None, não salva.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Aplicar log para melhor visualização (valores podem ser muito diferentes)
    def log_transform(x):
        return np.log(np.abs(x) + 0.0001)
    
    # Visualizar cada canal
    axes[0].imshow(log_transform(Y_idpcm[:, :, 0, 0]), cmap='gray')
    axes[0].set_title('Yb_iDPCM')
    axes[0].axis('off')
    
    axes[1].imshow(log_transform(Cb_idpcm[:, :, 0, 0]), cmap='gray')
    axes[1].set_title('Cbb_iDPCM')
    axes[1].axis('off')
    
    axes[2].imshow(log_transform(Cr_idpcm[:, :, 0, 0]), cmap='gray')
    axes[2].set_title('Crb_iDPCM')
    axes[2].axis('off')
    
    plt.tight_layout()
    
    if image_save_path:
        # Garantir que o diretório exista
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        plt.savefig(image_save_path)
        print(f"Imagem iDPCM salva em: {image_save_path}")
    
    # Sempre mostrar a imagem
    plt.show()

def main():
    """
    Função principal para testar a codificação DPCM.
    """
    import cv2
    from step1_color_space_conversion import rgb_to_ycbcr, rgb_from_ndarray
    from step3_discrete_cosine_transform import dct_channel
    from step4_quatization import get_quantization_matrix
    import numpy as np
    
    # Carregar e pré-processar a imagem
    image_path = IMAGES[0]  # airport.bmp
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Separar os canais RGB
    R, G, B = rgb_from_ndarray(image)
    
    # Converter para YCbCr
    Y, Cb, Cr = rgb_to_ycbcr(R, G, B)
    
    # Definir o tamanho do bloco e o fator de qualidade
    block_size = 8
    quality_factor = 75
    
    # Obter a matriz de quantização
    quant_matrix = get_quantization_matrix(quality_factor)
    
    # Função para dividir a imagem em blocos e aplicar DCT e quantização
    def process_channel(channel):
        h, w = channel.shape
        # Arredondar as dimensões para múltiplos de block_size
        h_blocks = h // block_size
        w_blocks = w // block_size
        
        # Criar array para armazenar os blocos
        blocks = np.zeros((h_blocks, w_blocks, block_size, block_size))
        
        # Processar cada bloco
        for i, j in product(range(h_blocks), range(w_blocks)):
            # Extrair o bloco
            block = channel[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size]
            # Aplicar DCT
            dct_block = dct_channel(block)
            # Aplicar quantização
            quant_block = np.round(dct_block / quant_matrix).astype(np.int32)
            # Armazenar o bloco
            blocks[i, j] = quant_block
            
        return blocks
    
    # Processar cada canal
    Y_blocks = process_channel(Y)
    Cb_blocks = process_channel(Cb)
    Cr_blocks = process_channel(Cr)
    
    # Aplicar DPCM
    Y_dpcm, Cb_dpcm, Cr_dpcm = apply_dpcm_to_channels(Y_blocks, Cb_blocks, Cr_blocks)
    
    # Visualizar os canais com DPCM
    dpcm_path = generate_path(image_path, "dpcm", output_dir=DOCS_DIR)
    visualize_dpcm_channels(Y_dpcm, Cb_dpcm, Cr_dpcm, image_save_path=dpcm_path)
    
    # Recuperar os canais originais
    Y_recovered, Cb_recovered, Cr_recovered = recover_channels_from_dpcm(Y_dpcm, Cb_dpcm, Cr_dpcm)
    
    # Visualizar os canais recuperados
    idpcm_path = generate_path(image_path, "idpcm", output_dir=DOCS_DIR)
    visualize_idpcm_channels(Y_recovered, Cb_recovered, Cr_recovered, image_save_path=idpcm_path)
    
    # Verificar se a recuperação foi bem-sucedida
    print(f"Erro máximo na recuperação do canal Y: {np.max(np.abs(Y_blocks - Y_recovered))}")
    print(f"Erro máximo na recuperação do canal Cb: {np.max(np.abs(Cb_blocks - Cb_recovered))}")
    print(f"Erro máximo na recuperação do canal Cr: {np.max(np.abs(Cr_blocks - Cr_recovered))}")

if __name__ == "__main__":
    main()
