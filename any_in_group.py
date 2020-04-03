from dataclasses import dataclass

from OORegex import OORegexBase, OOValue, Str
from typing import Tuple, Optional


@dataclass
class AnyInGroup(OORegexBase):
    value: OOValue = ""

    def build(self) -> str:
        return f"[{self.value}]"


@dataclass
class LettersAndDigits(AnyInGroup):
    value: OOValue = "[:alnum:]"


@dataclass
class Letters(AnyInGroup):
    value: OOValue = "[:alpha:]"


@dataclass
class ASCII(AnyInGroup):
    value: OOValue = "[:ascii:]"


@dataclass
class Blank(AnyInGroup):
    value: OOValue = "[:blank:]"

    def __neg__(self):
        return Visible()


@dataclass
class Control(AnyInGroup):
    value: OOValue = "[:cntrl:]"


@dataclass
class Digit(AnyInGroup):
    value: OOValue = "[:digit:]"
    max: Optional[int] = None
    min: Optional[int] = None

    def build(self) -> str:
        if self.max is not None:
            return self._build_range()
        return super().build()

    def _build_range(self):
        min_str, max_str = str(self.min), str(self.max)
        final_build = Str()

        for i in range(1, len(max_str)):
            final_build |= "[1-9]" + "[0-9]"*(i-1)
        for i, di in enumerate(max_str):
            build_str = max_str[:i]
            for j, dj in enumerate(max_str[i:]):
                if int(max_str[i]) == 1:
                    break
                if j == 0:
                    build_str += f"[0-{int(dj) - 1}]"
                else:
                    build_str += f"[0-9]"
            else:
                final_build |= build_str

        final_build |= Str(max_str)
        self.value = final_build
        return final_build.build()



@dataclass
class Visible(AnyInGroup):
    value: OOValue = "[:print:]"

    def __neg__(self):
        return Blank()


@dataclass
class Punctuation(AnyInGroup):
    value: OOValue = "[:punct:]"


@dataclass
class WhiteSpace(AnyInGroup):
    value: OOValue = "[:space:]"


@dataclass
class Uppercase(AnyInGroup):
    value: OOValue = "[:upper:]"

    def __neg__(self):
        return Lowercase()


@dataclass
class Lowercase(AnyInGroup):
    value: OOValue = "[:lower:]"

    def __neg__(self):
        return Uppercase()


@dataclass
class Word(AnyInGroup):
    value: OOValue = "[:word:]"


@dataclass
class Hexadecimal(AnyInGroup):
    value: OOValue = "[:xdigit:]"
