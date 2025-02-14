import numpy as np

from step0_preprocessing import padding

def test_padding():
    a = np.array([
        [1, 2],
        [3, 4],
    ])

    size = (5, 5)

    expected_a_padded = np.array([
        [1, 2, 0, 0, 0],
        [3, 4, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ])

    a_padded = padding(a, size)

    assert np.array_equal(a_padded, expected_a_padded), f'\n{a_padded}\n!=\n{expected_a_padded}'
