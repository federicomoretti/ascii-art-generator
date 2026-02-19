from dataclasses import dataclass

_DEFAULT_RAMP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
_SIMPLE_RAMP = "@%#*+=-:. "


@dataclass(frozen=True)
class CharacterRamp:
    characters: str

    def character_for(self, brightness: int) -> str:
        index = int(brightness / 255 * (len(self.characters) - 1))
        return self.characters[index]

    @classmethod
    def default(cls) -> "CharacterRamp":
        return cls(characters=_DEFAULT_RAMP)

    @classmethod
    def simple(cls) -> "CharacterRamp":
        return cls(characters=_SIMPLE_RAMP)

    @classmethod
    def from_string(cls, value: str | None) -> "CharacterRamp":
        return cls(characters=value) if value else cls.default()
