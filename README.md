# Image-Compression

This project is a Python implementation of JPEG encoding algorithm.

## Requirements

You need to have these packages installed on your system:
- Git
- Python >= 3.11
- ffmpeg >= 7.1

You need to have these python packages installed (via pip or conda, ...):
- Pytest: To run local unit test to check against expected results
- ffmpeg-python
- matplotlib
- numpy
- opencv-python
- scipy

Or you can simply use the python virtual environment with the `requirements.txt` provided in this repo.

## Setup

1. Clone this repository to your local machine.

```sh
cd <directory you want to clone into>
git clone https://github.com/ShellTux/Image-Compression.git
```

2. Create a virtual environment for the project:

> [!WARNING]
> Not needed if you manage your python packages through conda.
> You can skip to step 3

> [!NOTE]
> You only need to do this step one time

```sh
python -m venv .venv
```

3. Activate the virtual environment:

- On Windows:

```sh
venv\Scripts\activate
```

- On macOS and Linux:

```sh
source venv/bin/activate
```

4. Install the required packages by running:

> [!NOTE]
> You only need to do this step once

```sh
pip install -r requirements.txt
```

## Usage


1. Run the main script to encode an image:

```sh
python src/main.py
```

2. Run tests

```sh
pytest
```

3. Follow the instructions on the terminal to select an image to encode.

## Project Structure

<!--Report Project Structure Start-->

This repository is organized into several key directories and files to maintain
clarity and functionality for the JPEG codec implementation. Below is an
overview of the directory structure:

```
.
├── docs                  # Documentation and analysis related files
│   ├── step0            # Contains images and results for the report
│   ├── step1            # Contains images and results for the report
│   ├── step2            # Contains images and results for the report
│   ├── step3            # Contains images and results for the report
│   ├── step4            # Contains images and results for the report
│   ├── step5            # Contains images and results for the report
│   ├── airport-compression-ffmpeg.png        # Compression results for airport image using FFmpeg
│   ├── airport-error-analysis-qf75-422.png   # Error analysis for airport image at quality factor 75 (4:2:2)
│   ├── compression-plot.png                  # Plot visualizing compression metrics
│   ├── geometric-compression-ffmpeg.png      # Compression results for geometric image using FFmpeg
│   ├── jpeg-encoding.svg                     # SVG representation of the JPEG encoding process
│   ├── nature-compression-ffmpeg.png         # Compression results for nature image using FFmpeg
│   └── relatorio.md                          # Report documenting findings and results
├── images                # Source images used for compression
│   ├── airport.bmp       # BMP image of airport for testing
│   ├── geometric.bmp     # BMP image of geometric shapes for testing
│   └── nature.bmp        # BMP image of nature for testing
├── src                                 # Source code for the JPEG codec
│   ├── alinea10_analise_resultados.py  # Analysis script for results
│   ├── common.py                       # Common utilities and functions
│   ├── compress-ffmpeg.py              # Script for compression using FFmpeg
│   ├── decoder.py                      # JPEG decoder implementation
│   ├── decoder_test.py                 # Unit tests for decoder
│   ├── encoder.py                      # JPEG encoder implementation
│   ├── encoder_test.py                 # Unit tests for encoder
│   ├── step0_preprocessing.py                    # Preprocessing steps before encoding
│   ├── step0_preprocessing_test.py               # Unit Tests for preprocessing
│   ├── step1_color_space_conversion.py           # Color space conversion step in encoding
│   ├── step1_color_space_conversion_test.py      # Unit Tests for color space conversion
│   ├── step2_chrominance_downsampling.py         # Chrominance downsampling step
│   ├── step2_chrominance_downsampling_test.py    # Unit Tests for chrominance downsampling
│   ├── step3_discrete_cosine_transform.py        # DCT implementation
│   ├── step3_discrete_cosine_transform_test.py   # Unit Tests for DCT
│   ├── step4_quatization.py                      # Quantization step
│   ├── step4_quatization_test.py                 # Unit Tests for quantization
│   ├── step5_dpcm.py                             # DPCM (Differential Pulse Code Modulation) step
│   ├── step5_dpcm_test.py                        # Unit Tests for DPCM
│   ├── step6_run_length_huffman_encoding.py      # Run-length and Huffman encoding step
│   ├── step6_run_length_huffman_encoding_test.py # Unit Tests for encoding
│   └── step10_error_analysis.py # Error analysis module
├── all-python-scripts.sh # Script to run all Python files
├── flake.lock            # Dependency lock file for Flake
├── flake.nix             # Nix file for building the environment
├── generate-images.sh    # Script to generate images for testing
├── LICENSE               # License information for the project
├── makefile              # Makefile for build automation
├── README.md             # This README file
└── requirements.txt      # Python dependencies
```

<!--Report Project Structure End-->

## Generating report

All available tools for compiling the report pdf are declared through nix
flakes. To manually activate it, run:

```sh
nix develop
```

For example to activate the nix flake profile named `pedro`:

```sh
nix develop .#pedro
```

To compile the report

```sh
make docs/relatorio.pdf
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for more information.
