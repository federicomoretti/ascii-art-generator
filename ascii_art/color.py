from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class RgbColor:
    r: int
    g: int
    b: int

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def luminance(self) -> int:
        return int(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)

    @classmethod
    def average(cls, colors: Sequence["RgbColor"]) -> "RgbColor":
        count = len(colors)
        return cls(
            r=sum(c.r for c in colors) // count,
            g=sum(c.g for c in colors) // count,
            b=sum(c.b for c in colors) // count,
        )


@dataclass(frozen=True)
class ColorImage:
    pixels: tuple[RgbColor, ...]
    width: int
    height: int
