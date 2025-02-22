from common import BUILD_DIR, IMAGES, QUALITIES
from sys import stderr
import ffmpeg
import itertools
import os

def compress_image(image_path: str, build_dir: str, quality: int) -> tuple[str, float]:
    """
    Compress bmp image to jpeg in the given build_dir with the given quality


    Parameters
    ----------
    image_path : str
        The original bmp file path

    build_dir : str
        The directory to build compressed image to.

    quality : int [1-100]
        The quality of jpeg compression.

    Returns
    -------
    tuple[str, float]
        The tuple containing the compressed image path and the compression ratio
    """
    assert 0 <= quality <= 100, f'The quality must be between 0 and 100. Provided: {quality}'

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    image_basename, ext = os.path.splitext(os.path.basename(image_path))
    assert ext == '.bmp', f'The file ({image_path}) provided is not bmp file.'

    compressed_image_path = os.path.join(build_dir, f"{image_basename}-q{quality}.jpeg")

    # NOTE: ffmpeg quality is between 1-31, so I am mapping 0-100 -> 1-31
    quality = int(32 - (quality / 3.125))
    try:
        (
            ffmpeg
            .input(image_path)
            .output(compressed_image_path, q=quality)
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        print('Error occurred:', e.stderr.decode())
        return compressed_image_path, 0

    original_size = os.path.getsize(image_path)
    compressed_size = os.path.getsize(compressed_image_path)

    if compressed_size <= 0:
        print('Compressed file size is zero, unable to calculate ratio.', file=stderr)
        return compressed_image_path, 0

    return compressed_image_path, original_size / compressed_size


def ex1():
    for image, quality in itertools.product(IMAGES, QUALITIES):
        compressed_path, compression_ratio = compress_image(image, BUILD_DIR, quality)
        print(f'{image} -> {compressed_path}: {compression_ratio=:.2f}')

def main():
    ex1()

if __name__ == '__main__':
    main()
