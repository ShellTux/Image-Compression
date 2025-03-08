import numpy as np
import pytest
from step5_dpcm import dpcm_encode, dpcm_decode

def test_dpcm_encode():
    """
    Testa a função de codificação DPCM.
    """
    # Criar um array de teste com blocos 8x8
    # Cada bloco tem um valor DC diferente
    blocks = np.zeros((2, 2, 8, 8))
    blocks[0, 0, 0, 0] = 10
    blocks[0, 1, 0, 0] = 15
    blocks[1, 0, 0, 0] = 12
    blocks[1, 1, 0, 0] = 20
    
    # Aplicar DPCM
    dpcm_blocks = dpcm_encode(blocks)
    
    # Verificar os resultados
    # O primeiro bloco deve ter o mesmo valor DC (10)
    assert dpcm_blocks[0, 0, 0, 0] == 10
    # O segundo bloco deve ter a diferença (15 - 10 = 5)
    assert dpcm_blocks[0, 1, 0, 0] == 5
    # O terceiro bloco deve ter a diferença (12 - 15 = -3)
    assert dpcm_blocks[1, 0, 0, 0] == -3
    # O quarto bloco deve ter a diferença (20 - 12 = 8)
    assert dpcm_blocks[1, 1, 0, 0] == 8
    
    # Verificar que os outros valores não foram alterados
    assert np.all(dpcm_blocks[0, 0, 1:, :] == 0)
    assert np.all(dpcm_blocks[0, 0, 0, 1:] == 0)

def test_dpcm_decode():
    """
    Testa a função de decodificação DPCM.
    """
    # Criar um array de teste com blocos 8x8
    # Cada bloco tem um valor de diferença
    dpcm_blocks = np.zeros((2, 2, 8, 8))
    dpcm_blocks[0, 0, 0, 0] = 10  # Primeiro valor DC
    dpcm_blocks[0, 1, 0, 0] = 5   # Diferença para o segundo bloco
    dpcm_blocks[1, 0, 0, 0] = -3  # Diferença para o terceiro bloco
    dpcm_blocks[1, 1, 0, 0] = 8   # Diferença para o quarto bloco
    
    # Aplicar a decodificação DPCM
    decoded_blocks = dpcm_decode(dpcm_blocks)
    
    # Verificar os resultados
    # O primeiro bloco deve ter o valor DC original (10)
    assert decoded_blocks[0, 0, 0, 0] == 10
    # O segundo bloco deve ter o valor DC (10 + 5 = 15)
    assert decoded_blocks[0, 1, 0, 0] == 15
    # O terceiro bloco deve ter o valor DC (15 - 3 = 12)
    assert decoded_blocks[1, 0, 0, 0] == 12
    # O quarto bloco deve ter o valor DC (12 + 8 = 20)
    assert decoded_blocks[1, 1, 0, 0] == 20
    
    # Verificar que os outros valores não foram alterados
    assert np.all(decoded_blocks[0, 0, 1:, :] == 0)
    assert np.all(decoded_blocks[0, 0, 0, 1:] == 0)

def test_dpcm_roundtrip():
    """
    Testa o ciclo completo de codificação e decodificação DPCM.
    """
    # Criar um array de teste com blocos 8x8
    original_blocks = np.zeros((3, 3, 8, 8))
    
    # Definir valores DC aleatórios
    np.random.seed(42)
    for i in range(3):
        for j in range(3):
            original_blocks[i, j, 0, 0] = np.random.randint(-100, 100)
    
    # Aplicar DPCM
    dpcm_blocks = dpcm_encode(original_blocks)
    
    # Decodificar DPCM
    decoded_blocks = dpcm_decode(dpcm_blocks)
    
    # Verificar que os blocos originais e decodificados são iguais
    np.testing.assert_array_equal(original_blocks, decoded_blocks)

def test_airport_example():
    """
    Testa o exemplo específico da imagem airport mostrado nas imagens de validação.
    """
    # Criar um bloco 8x8 com os valores mostrados no exemplo
    block = np.zeros((1, 1, 8, 8))
    block[0, 0, 0, 0] = 226
    
    # Aplicar DPCM (como é o primeiro bloco, o valor deve permanecer o mesmo)
    dpcm_block = dpcm_encode(block)
    assert dpcm_block[0, 0, 0, 0] == 226
    
    # Decodificar DPCM
    decoded_block = dpcm_decode(dpcm_block)
    assert decoded_block[0, 0, 0, 0] == 226
    
    # Teste com dois blocos
    blocks = np.zeros((1, 2, 8, 8))
    blocks[0, 0, 0, 0] = 226
    blocks[0, 1, 0, 0] = 223  # Valor hipotético para o segundo bloco
    
    # Aplicar DPCM
    dpcm_blocks = dpcm_encode(blocks)
    assert dpcm_blocks[0, 0, 0, 0] == 226
    assert dpcm_blocks[0, 1, 0, 0] == -3  # 223 - 226 = -3
    
    # Decodificar DPCM
    decoded_blocks = dpcm_decode(dpcm_blocks)
    assert decoded_blocks[0, 0, 0, 0] == 226
    assert decoded_blocks[0, 1, 0, 0] == 223

if __name__ == "__main__":
    # Executar os testes
    test_dpcm_encode()
    test_dpcm_decode()
    test_dpcm_roundtrip()
    test_airport_example()
    print("Todos os testes passaram!")
