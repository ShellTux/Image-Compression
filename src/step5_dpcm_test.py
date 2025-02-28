import numpy as np
import pytest
from step5_dpcm import dpcm_encode_dc, dpcm_decode_dc, pad_to_multiple_of_8

def test_dpcm_encode_decode():
    """
    Testa se a codificação e decodificação DPCM mantém a integridade dos dados
    """
    # Cria uma matriz de teste 8x8
    test_block = np.array([
        [226, 0, 0, 0, 0, 0, 0, 0],
        [223, 0, 0, 0, 0, 0, 0, 0],
        [220, 0, 0, 0, 0, 0, 0, 0],
        [219, 0, 0, 0, 0, 0, 0, 0],
        [218, 0, 0, 0, 0, 0, 0, 0],
        [217, 0, 0, 0, 0, 0, 0, 0],
        [216, 0, 0, 0, 0, 0, 0, 0],
        [215, 0, 0, 0, 0, 0, 0, 0]
    ])

    # Aplica DPCM
    encoded = dpcm_encode_dc(test_block)
    decoded = dpcm_decode_dc(encoded)

    # Verifica se a decodificação recupera os valores originais
    assert np.allclose(test_block, decoded), "A decodificação DPCM não recuperou os valores originais"

def test_dpcm_first_block_unchanged():
    """
    Testa se o primeiro bloco permanece inalterado após DPCM
    """
    test_block = np.array([
        [100, 0, 0, 0, 0, 0, 0, 0],
        [50, 0, 0, 0, 0, 0, 0, 0]
    ])

    encoded = dpcm_encode_dc(test_block)
    # Verifica se o primeiro valor permanece o mesmo
    assert encoded[0,0] == test_block[0,0], "O primeiro coeficiente DC não deveria mudar"

def test_pad_to_multiple_of_8():
    """
    Testa se a função de padding funciona corretamente
    """
    # Cria uma matriz 5x5
    test_matrix = np.ones((5, 5))
    padded = pad_to_multiple_of_8(test_matrix)

    # Verifica se as dimensões são múltiplas de 8
    assert padded.shape[0] % 8 == 0, "Altura não é múltipla de 8"
    assert padded.shape[1] % 8 == 0, "Largura não é múltipla de 8"
    assert padded.shape == (8, 8), "Dimensões incorretas após padding"

def test_dpcm_difference_encoding():
    """
    Testa se a codificação DPCM está calculando as diferenças corretamente
    """
    test_block = np.array([
        [100, 0, 0, 0, 0, 0, 0, 0],
        [90, 0, 0, 0, 0, 0, 0, 0],
        [85, 0, 0, 0, 0, 0, 0, 0],
        [80, 0, 0, 0, 0, 0, 0, 0]
    ])

    encoded = dpcm_encode_dc(test_block)
    
    # O segundo valor deve ser a diferença entre 90 e 100
    assert encoded[1,0] == -10, "A diferença DPCM não foi calculada corretamente"

if __name__ == "__main__":
    pytest.main([__file__])
