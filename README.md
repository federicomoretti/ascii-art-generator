# ASCII Art Generator

A CLI tool that converts images to ASCII art.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
ascii-art <image> [-w WIDTH] [--invert] [--chars CHARS] [--braille] [--console-log]
```

| Flag | Description | Default |
|------|-------------|---------|
| `image` | Path to image file (any Pillow-supported format) | required |
| `-w, --width` | Output width in characters, clamped to [10, 300] | terminal width |
| `--invert` | Invert brightness (for light backgrounds) | off |
| `--chars` | Custom character ramp (dark to light) | 70-char default |
| `--braille` | Use braille characters for higher resolution | off |
| `--console-log` | Output as colored JavaScript `console.log` statements | off |

`--braille` and `--console-log` can be combined for high-resolution colored braille output in the browser console.

### Examples

```bash
# Basic usage
ascii-art photo.png

# Set output width to 80 characters
ascii-art photo.png -w 80

# Invert for light terminal backgrounds
ascii-art photo.png --invert

# Use a custom character ramp
ascii-art photo.png --chars "@#. "

# Braille mode for higher detail
ascii-art photo.png -w 40 --braille

# Colored output for browser console
ascii-art photo.png --console-log

# Colored braille for browser console
ascii-art photo.png --braille --console-log

# Can also run as a Python module
python -m ascii_art photo.png
```
