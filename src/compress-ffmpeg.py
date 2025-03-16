from common import BUILD_DIR, DOCS_DIR, IMAGES, QUALITIES, generate_path
from matplotlib import pyplot as plt
from sys import stderr
import argparse
import ffmpeg
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
    quality = int(32 - quality * 32 / 100)
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


def main():
    parser = argparse.ArgumentParser(description="Image Compression using ffmpeg")

    parser.add_argument('--hide-figures', action='store_true', help='Disable matplotlib figures')

    args = parser.parse_args()

    show_figures: bool = not args.hide_figures

    results: dict[str, list[float]] = {image: [] for image in IMAGES}

    n_qualities = len(QUALITIES)

    for image_path in IMAGES:
        fig, axes = plt.subplots(n_qualities + 1, 1, figsize=(3, 12))

        image = plt.imread(image_path)

        axes[0].imshow(image)
        axes[0].set_title(f'Original {image_path}')
        axes[0].axis('off')

        for i, quality in enumerate(QUALITIES):
            compressed_path, compression_ratio = compress_image(image_path, BUILD_DIR, quality)
            results[image_path].append(compression_ratio)
            print(f'{image_path} -> {compressed_path}: {compression_ratio=:.2f}')

            compressed_image = plt.imread(compressed_path)

            axes[i + 1].imshow(compressed_image)
            axes[i + 1].set_title(f'{image_path} Q{quality}')
            axes[i + 1].axis('off')

        fig.tight_layout()
        if show_figures:
            plt.show()

        image_save_path = generate_path(image_path, 'compression-ffmpeg', output_dir=DOCS_DIR)
        fig.savefig(image_save_path,bbox_inches='tight', dpi=150)
        print(f'Saved image: {image_save_path}')

    fig = plt.figure(figsize=(12, 6))

    for image_path, ratios in results.items():
        plt.plot(QUALITIES, ratios, marker='o', label=image_path)

    plt.title('Image Compression Ratios by Quality')
    plt.xlabel('Quality Level (1-100)')
    plt.ylabel('Compression Ratio')
    plt.xticks(QUALITIES)
    plt.grid()
    plt.legend()
    plt.gca().invert_xaxis()

    if show_figures:
        plt.show()

    image_save_path = f'{DOCS_DIR}/compression-plot.png'
    fig.savefig(image_save_path, bbox_inches='tight', dpi=150)
    print(f'Saved image: {image_save_path}')

if __name__ == '__main__':
    main()
