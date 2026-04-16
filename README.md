# Heart shaped QR code generator for Python

Generate aesthetic heart-shaped QR codes with this Python library. It converts standard QR patterns into heart geometry with support for custom colors, transparent backgrounds, and CLI usage.

## Command-line usage

Generate images from the terminal using the CLI script.

```bash
PYTHONPATH=. ./.venv/bin/python3 cli.py "https://google.com" -o "heart_qr.png" -c "#c80000"
```

The script supports the following arguments:
* `text`: The target text or URL.
* `-o`, `--output`: Target path for the generated image. Default is `heart_qr.png`.
* `-c`, `--color`: Heart color in hex format. Default is `#c80000`.
* `-s`, `--size`: Output image canvas size in pixels. Default is `1000`.
* `-g`, `--gap`: Pixel gap between the QR square and the lobes. Default is `20.0`.
* `-bg`, `--bg-color`: Background color in hex. Default is `#ffffff`.
* `--solid-bg`: Flag to use a solid background instead of transparency.

### CLI Examples

Standard heart
```bash
python3 cli.py "Hello World" -o basic.png
```

Transparent background
```bash
python3 cli.py "Transparent" -o transparent.png
```

Large resolution
```bash
python3 cli.py "Big QR" -s 1024 -o 1024.png
```

Custom palette
```bash
python3 cli.py "Palette" -c "#FFD6A6" -bg "#FF9A86" --solid-bg -o palette.png
```

No gap
```bash
python3 cli.py "No Gap" -g 0 -o no_gap.png
```

Solid background
```bash
python3 cli.py "Solid BG" --solid-bg -o solid.png
```

## Installation

The project requires Python
Create a virtual environment and install the necessary dependencies before running the scripts.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Pillow qrcode
```

## Getting started

Generate a base QR code first. Then, pass the resulting byte buffer into the image composer to apply the heart-shaped transformations.

Example script for a transparent, heart-shaped QR code:

```python
import io
from qr.models import QRConfig
from qr.generator import QRCodeGenerator
from composer.composer import ImageComposer
from composer.models import CompositionConfig

# Set up the generator
target_color = (200, 0, 0)
qr_gen = QRCodeGenerator()
qr_config = QRConfig(
    fill_color=f"#{target_color[0]:02x}{target_color[1]:02x}{target_color[2]:02x}",
    back_color="transparent"
)

# Build the standard square QR code
qr_buffer = qr_gen.generate("https://google.com", qr_config)

# Configure the shape modifications
composer = ImageComposer()
config = CompositionConfig(
    background_size=(1000, 1000),
    transparent_bg=True,
    qr_scale=0.9,
    add_heart=True,
    heart_color=target_color,
    heart_gap=20.0,
    use_qr_pattern_lobes=True,
    source_text="https://google.com"
)

# Apply transformations and save
final_buffer = composer.compose_centered(qr_buffer, config)

with open("output.png", "wb") as file:
    file.write(final_buffer.getvalue())
```

## Configuration parameters

`CompositionConfig` defines the output format.

* `background_size`: Tuple defining the final width and height of the image frame.
* `transparent_bg`: Boolean that toggles an RGBA output mask instead of a solid color block.
* `qr_scale`: Float indicating how much of the target background the heart should fill.
* `heart_color`: RGB tuple matching the QR code fill color.
* `heart_gap`: Float setting the separation distance between the central diamond and the upper lobes.
* `use_qr_pattern_lobes`: Boolean that forces the script to generate a secondary QR pattern to disguise the empty circles.
* `source_text`: The string used to construct the lobe patterns. Match this to your primary URL.

## Running tests

Verify the composition logic by running the test module from the project root.

```bash
PYTHONPATH=. ./.venv/bin/python3 -m composer.test_composer
```

This runs the internal checks and outputs `.png` files for manual review.
