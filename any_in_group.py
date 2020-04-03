from dataclasses import dataclass

from OORegex import OORegexBase, OOValue, Str
from typing import Tuple, Optional
import string


@dataclass
class AnyIn(OORegexBase):
    value: OOValue = None

    def __init__(self, value):
        assert value is not None
        self.value = value

    def build(self) -> str:
        return f"[{self.value}]"

    def __neg__(self):
        return f"[^{self.value}]"


@dataclass
class AnyChar(OORegexBase):
    value: OOValue = "."


@dataclass
class LettersAndDigits(AnyIn):
    value: OOValue = "a-zA-Z0-9"


@dataclass
class Letters(OORegexBase):
    value: OOValue = "a-zA-Z"


@dataclass
class Digit(OORegexBase):
    value: OOValue = r"\d"
    max: Optional[int] = None
    min: Optional[int] = None

    def build(self) -> str:
        if self.max is not None:
            q = self._build_range(self.max)
            if self.min:
                q = f"(?!{self._build_range(self.min-1)})" + q
            self.value = q
        return super().build()

    def _build_range(self, number):
        if number == 0:
            return "0"
        number_str = str(number)
        final_build = Str()

        for i in range(1, len(number_str)):
            final_build |= "[1-9]" + "[0-9]" * (i - 1)
        for i, di in enumerate(number_str):
            build_str = number_str[:i]
            for j, dj in enumerate(number_str[i:]):
                if int(number_str[i]) == 1:
                    break
                if j == 0:
                    build_str += f"[0-{int(dj) - 1}]"
                else:
                    build_str += f"[0-9]"
            else:
                final_build |= build_str

        final_build |= Str(number_str)
        return final_build.build()


@dataclass
class Unicode(OORegexBase):
    value: OOValue = r"\X"


@dataclass
class NewLine(OORegexBase):
    value: OOValue = r"\R"


@dataclass
class VerticalWhitespace(OORegexBase):
    value: OOValue = r"\v"


@dataclass
class HorizontalWhitespace(OORegexBase):
    value: OOValue = r"\h"


@dataclass
class Blank(OORegexBase):
    value: OOValue = "[:blank:]"

    def __neg__(self):
        return Visible()


@dataclass
class Control(OORegexBase):
    value: OOValue = "[:cntrl:]"


@dataclass
class Visible(OORegexBase):
    value: OOValue = "[:print:]"

    def __neg__(self):
        return Blank()


@dataclass
class Punctuation(OORegexBase):
    value: OOValue = f"[{string.punctuation}]"


@dataclass
class WhiteSpace(OORegexBase):
    value: OOValue = r"\s"


@dataclass
class Word(OORegexBase):
    value: OOValue = r"\w"


@dataclass
class Hexadecimal(OORegexBase):
    value: OOValue = "[:xdigit:]"
