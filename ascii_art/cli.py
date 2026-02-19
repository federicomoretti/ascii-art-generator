import argparse
import shutil
import sys
from pathlib import Path

from PIL import UnidentifiedImageError

from ascii_art.braille_converter import convert_to_braille
from ascii_art.character_ramp import CharacterRamp
from ascii_art.console_log_converter import convert_braille_to_colored, convert_to_colored, format_as_console_log
from ascii_art.converter import convert
from ascii_art.image_source import load_color_image, load_image

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
    parser.add_argument("--console-log", action="store_true", help="output as colored JavaScript console.log statements")

    args = parser.parse_args(argv)
    args.width = max(MIN_WIDTH, min(MAX_WIDTH, args.width))
    return args


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)

    try:
        if args.braille and args.console_log:
            color_image = load_color_image(args.image, args.width, pixel_scale=(2, 4))
            art = convert_braille_to_colored(color_image, invert=args.invert)
            print(format_as_console_log(art))
        elif args.console_log:
            color_image = load_color_image(args.image, args.width)
            ramp = CharacterRamp.from_string(args.chars)
            art = convert_to_colored(color_image, ramp, invert=args.invert)
            print(format_as_console_log(art))
        elif args.braille:
            image = load_image(args.image, args.width, pixel_scale=(2, 4))
            print(convert_to_braille(image, invert=args.invert))
        else:
            image = load_image(args.image, args.width)
            ramp = CharacterRamp.from_string(args.chars)
            print(convert(image, ramp, invert=args.invert))
    except FileNotFoundError:
        print(f"Error: file not found: {args.image}", file=sys.stderr)
        sys.exit(1)
    except UnidentifiedImageError:
        print(f"Error: unsupported image format: {args.image}", file=sys.stderr)
        sys.exit(1)
