from dataclasses import dataclass
from pathlib import Path

from PIL import Image

ASPECT_CORRECTION = 0.45


@dataclass(frozen=True)
class GrayscaleImage:
    pixels: list[int]
    width: int
    height: int


def load_image(
    path: Path,
    target_width: int,
    *,
    pixel_scale: tuple[int, int] = (1, 1),
    aspect_correction: float = ASPECT_CORRECTION,
) -> GrayscaleImage:
    image = Image.open(path).convert("RGB")
    scaled_width = target_width * pixel_scale[0]
    scaled_height = int(image.height / image.width * target_width * aspect_correction) * pixel_scale[1]
    image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
    image = image.convert("L")

    return GrayscaleImage(
        pixels=list(image.getdata()),
        width=scaled_width,
        height=scaled_height,
    )
