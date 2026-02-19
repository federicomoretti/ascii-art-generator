from statistics import median

from ascii_art.converter import AsciiArt
from ascii_art.image_source import GrayscaleImage

_BRAILLE_BASE = 0x2800

_DOT_BITS = (
    (0x01, 0x08),
    (0x02, 0x10),
    (0x04, 0x20),
    (0x40, 0x80),
)


def _compute_threshold(pixels: list[int]) -> int:
    return int(median(pixels))


def _pixel_at(pixels: list[int], width: int, height: int, row: int, col: int) -> int:
    if row >= height or col >= width:
        return 255
    return pixels[row * width + col]


def _braille_char(
    pixels: list[int],
    width: int,
    height: int,
    block_row: int,
    block_col: int,
    threshold: int,
) -> str:
    origin_row = block_row * 4
    origin_col = block_col * 2

    code_point = _BRAILLE_BASE + sum(
        _DOT_BITS[dr][dc]
        for dr in range(4)
        for dc in range(2)
        if _pixel_at(pixels, width, height, origin_row + dr, origin_col + dc) < threshold
    )

    return chr(code_point)


def convert_to_braille(image: GrayscaleImage, *, invert: bool = False) -> AsciiArt:
    brightness = [255 - p if invert else p for p in image.pixels]
    threshold = _compute_threshold(brightness)

    rows = tuple(
        "".join(
            _braille_char(brightness, image.width, image.height, block_row, block_col, threshold)
            for block_col in range(image.width // 2)
        )
        for block_row in range(image.height // 4)
    )

    return AsciiArt(rows=rows)
