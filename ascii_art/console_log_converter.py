from dataclasses import dataclass
from itertools import groupby
from statistics import median

from ascii_art.character_ramp import CharacterRamp
from ascii_art.color import ColorImage, RgbColor


@dataclass(frozen=True)
class ColoredChar:
    character: str
    color: RgbColor


@dataclass(frozen=True)
class ColoredAsciiArt:
    rows: tuple[tuple[ColoredChar, ...], ...]


@dataclass(frozen=True)
class ConsoleLogSegment:
    text: str
    color: RgbColor


_BRAILLE_BASE = 0x2800

_DOT_BITS = (
    (0x01, 0x08),
    (0x02, 0x10),
    (0x04, 0x20),
    (0x40, 0x80),
)


def convert_braille_to_colored(
    image: ColorImage, *, invert: bool = False,
) -> ColoredAsciiArt:
    luminances = [
        255 - pixel.luminance() if invert else pixel.luminance()
        for pixel in image.pixels
    ]
    threshold = int(median(luminances))

    rows = tuple(
        tuple(
            _braille_colored_char(image, luminances, threshold, block_row, block_col)
            for block_col in range(image.width // 2)
        )
        for block_row in range(image.height // 4)
    )
    return ColoredAsciiArt(rows=rows)


def _braille_colored_char(
    image: ColorImage,
    luminances: list[int],
    threshold: int,
    block_row: int,
    block_col: int,
) -> ColoredChar:
    origin_row = block_row * 4
    origin_col = block_col * 2

    block_pixels: list[RgbColor] = []
    code_point = _BRAILLE_BASE
    for dr in range(4):
        for dc in range(2):
            row = origin_row + dr
            col = origin_col + dc
            if row < image.height and col < image.width:
                idx = row * image.width + col
                block_pixels.append(image.pixels[idx])
                if luminances[idx] < threshold:
                    code_point += _DOT_BITS[dr][dc]

    return ColoredChar(
        character=chr(code_point),
        color=RgbColor.average(block_pixels),
    )


def convert_to_colored(
    image: ColorImage, ramp: CharacterRamp, *, invert: bool = False,
) -> ColoredAsciiArt:
    colored_chars = tuple(
        ColoredChar(
            character=ramp.character_for(255 - pixel.luminance() if invert else pixel.luminance()),
            color=pixel,
        )
        for pixel in image.pixels
    )
    rows = tuple(
        colored_chars[row * image.width:(row + 1) * image.width]
        for row in range(image.height)
    )
    return ColoredAsciiArt(rows=rows)


def _segments_from_row(row: tuple[ColoredChar, ...]) -> tuple[ConsoleLogSegment, ...]:
    return tuple(
        ConsoleLogSegment(
            text="".join(char.character for char in group),
            color=color,
        )
        for color, group in groupby(row, key=lambda c: c.color)
    )


def _escape_js(text: str) -> str:
    return text.replace("\\", "\\\\").replace("'", "\\'")


def _escape_format(text: str) -> str:
    return text.replace("%", "%%")


def _format_row(segments: tuple[ConsoleLogSegment, ...]) -> str:
    format_string = "".join(
        f"%c{_escape_format(segment.text)}" for segment in segments
    )
    style_args = ", ".join(
        f"'color: {segment.color.to_hex()}; font-family: monospace;'"
        for segment in segments
    )
    return f"console.log('{_escape_js(format_string)}', {style_args});"


def format_as_console_log(art: ColoredAsciiArt) -> str:
    return "\n".join(
        _format_row(_segments_from_row(row))
        for row in art.rows
    )
