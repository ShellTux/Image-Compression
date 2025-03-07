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

- `docs`: Contains documentation files.
- `images`: Includes example images for testing the encoding algorithm.
- `src`: Holds the source code for the JPEG encoding algorithm.
- `flake.lock` and `flake.nix`: Flake lock and nix files for dependency management.
- `LICENSE`: The license file for the project.
- `README.md`: The file you are currently reading.
- `requirements.txt`: List of required packages for the project.

## Generating report

All available tools for compiling the report pdf are declared through nix
flakes. To manually activate it, run:

```sh
nix develop
```

To compile the report

```sh
make docs/relatorio.pdf
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for more information.
