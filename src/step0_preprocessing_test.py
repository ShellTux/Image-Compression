from step0_preprocessing import padding
import numpy as np

def test_padding():
    a = np.array([
        [1, 2],
        [3, 4],
    ])

    size = (5, 5)

    expected_a_padded = np.array([
        [1, 2, 2, 2, 2],
        [3, 4, 4, 4, 4],
        [3, 4, 4, 4, 4],
        [3, 4, 4, 4, 4],
        [3, 4, 4, 4, 4],
    ])

    a_padded = padding(a, size)

    # assert np.array_equal(a_padded, expected_a_padded), f'\n{a_padded}\n!=\n{expected_a_padded}'

    a = np.array([
        [
            [1, 2],
            [3, 4],
        ],
        [
            [6, 7],
            [8, 9],
        ],
        [
            [10, 11],
            [12, 13],
        ],
    ])

    a_padded = padding(a, (5, 5, 3))
    expected_a_padded = np.array([
        [
            [1, 2, 2, 2, 2],
            [3, 4, 4, 4, 4],
            [3, 4, 4, 4, 4],
            [3, 4, 4, 4, 4],
            [3, 4, 4, 4, 4],
        ],
        [
            [6, 7, 7, 7, 7],
            [8, 9, 9, 9, 9],
            [8, 9, 9, 9, 9],
            [8, 9, 9, 9, 9],
            [8, 9, 9, 9, 9],
        ],
        [
            [10, 11, 11, 11, 11],
            [12, 13, 13, 13, 13],
            [12, 13, 13, 13, 13],
            [12, 13, 13, 13, 13],
            [12, 13, 13, 13, 13],
        ],
    ])

    assert np.array_equal(a_padded, expected_a_padded), f'\n{a_padded}\n!=\n{expected_a_padded}'
