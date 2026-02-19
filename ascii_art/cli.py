import argparse
import shutil
import sys
from pathlib import Path

from PIL import UnidentifiedImageError

from ascii_art.braille_converter import convert_to_braille
from ascii_art.character_ramp import CharacterRamp
from ascii_art.converter import convert
from ascii_art.image_source import BRAILLE_ASPECT_CORRECTION, load_image

MIN_WIDTH = 10
MAX_WIDTH = 300


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ascii-art",
        description="Convert images to ASCII art",
    )
    parser.add_argument("image", type=Path, help="path to image file")
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=shutil.get_terminal_size().columns,
        help="output width in characters (default: terminal width)",
    )
    parser.add_argument("--invert", action="store_true", help="invert brightness (for light backgrounds)")
    parser.add_argument("--chars", type=str, default=None, help="custom character ramp (dark to light)")
    parser.add_argument("--braille", action="store_true", help="use braille characters for higher resolution")

    args = parser.parse_args(argv)
    args.width = max(MIN_WIDTH, min(MAX_WIDTH, args.width))
    return args


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)

    load_kwargs = (
        {"pixel_scale": (2, 4), "aspect_correction": BRAILLE_ASPECT_CORRECTION}
        if args.braille
        else {}
    )

    try:
        image = load_image(args.image, args.width, **load_kwargs)
    except FileNotFoundError:
        print(f"Error: file not found: {args.image}", file=sys.stderr)
        sys.exit(1)
    except UnidentifiedImageError:
        print(f"Error: unsupported image format: {args.image}", file=sys.stderr)
        sys.exit(1)

    if args.braille:
        art = convert_to_braille(image, invert=args.invert)
    else:
        ramp = CharacterRamp.from_string(args.chars)
        art = convert(image, ramp, invert=args.invert)

    print(art)
