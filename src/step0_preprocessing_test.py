from step0_preprocessing import padding
import numpy as np

def test_padding():
    actual_data = [
        np.array([
            [1, 2],
            [3, 4]
        ]),
        np.array([
            [5, 6],
            [7, 8]
        ]),
    ]

    size_data = [
        (5, 5),
        (8, 8),
    ]

    expected_data = [
        np.array([
            [1, 2, 2, 2, 2],
            [3, 4, 4, 4, 4],
            [3, 4, 4, 4, 4],
            [3, 4, 4, 4, 4],
            [3, 4, 4, 4, 4]
        ]),
        np.array([
            [5, 6, 6, 6, 6, 6, 6, 6],
            [7, 8, 8, 8, 8, 8, 8, 8],
            [7, 8, 8, 8, 8, 8, 8, 8],
            [7, 8, 8, 8, 8, 8, 8, 8],
            [7, 8, 8, 8, 8, 8, 8, 8],
            [7, 8, 8, 8, 8, 8, 8, 8],
            [7, 8, 8, 8, 8, 8, 8, 8],
            [7, 8, 8, 8, 8, 8, 8, 8]
        ])
    ]

    for actual, size, expected in zip(actual_data, size_data, expected_data):
        got = padding(actual, size)
        assert np.array_equal(got, expected), f'\n{got}\n!=\n{expected}'
