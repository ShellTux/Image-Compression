from common import TEST_PARAMETERS
from matplotlib import pyplot as plt
import decoder
import encoder
import numpy as np

image = plt.imread(TEST_PARAMETERS.image_path)
jpeg_encoded_data, jpeg_intermidiate_values = encoder.encoder(
    image,
    downsampling=TEST_PARAMETERS.downsampling,
    quality_factor=TEST_PARAMETERS.quality_factor,
    return_intermidiate_values=True
)

image_reconstructed, jpge_decoded_iv = decoder.decoder(
    jpeg_encoded_data,
    downsampling=TEST_PARAMETERS.downsampling,
    quality_factor=TEST_PARAMETERS.quality_factor,
    return_intermidiate_values=True,
)

Yb_iDPCM = np.array([
    [226,   0,   0,   0,   0,   0,   0,   0],
    [ -3,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0],
])

def test_decoder_idpcm():
    assert False
