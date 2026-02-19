from dataclasses import dataclass

from ascii_art.character_ramp import CharacterRamp
from ascii_art.image_source import GrayscaleImage


@dataclass(frozen=True)
class AsciiArt:
    rows: tuple[str, ...]

    def __str__(self) -> str:
        return "\n".join(self.rows)


def convert(image: GrayscaleImage, ramp: CharacterRamp, *, invert: bool = False) -> AsciiArt:
    brightness = [255 - p if invert else p for p in image.pixels]
    characters = [ramp.character_for(b) for b in brightness]
    rows = tuple(
        "".join(characters[row * image.width:(row + 1) * image.width])
        for row in range(image.height)
    )
    return AsciiArt(rows=rows)
