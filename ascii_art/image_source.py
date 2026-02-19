from dataclasses import dataclass
from pathlib import Path

from PIL import Image

ASPECT_CORRECTION = 0.45


@dataclass(frozen=True)
class GrayscaleImage:
    pixels: list[int]
    width: int
    height: int


def load_image(path: Path, target_width: int) -> GrayscaleImage:
    image = Image.open(path).convert("RGB")
    target_height = int(image.height / image.width * target_width * ASPECT_CORRECTION)
    image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    image = image.convert("L")

    return GrayscaleImage(
        pixels=list(image.getdata()),
        width=target_width,
        height=target_height,
    )
