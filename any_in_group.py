from dataclasses import dataclass

from OORegex import OORegexBase, OORValue, R
from typing import Tuple, Optional
import string


class AnyIn(OORegexBase):
    _D_value: OORValue = None

    def build(self) -> str:
        return f"[{self._value}]"

    def __neg__(self):
        return f"[^{self._value}]"


class AnyChar(OORegexBase):
    _D_value: OORValue = "."


class LettersAndDigits(AnyIn):
    _D_value: OORValue = "a-zA-Z0-9"


class Letters(OORegexBase):
    _D_value: OORValue = "a-zA-Z"


class Digit(R):
    def __init__(
        self,
        min: Optional[int] = None,
        max: Optional[int] = None,
        **kwargs
    ):
        self._min = min
        self._max = max
        super().__init__(**kwargs)

    def build(self) -> str:
        if self._max is not None:
            q = self._build_range(self._max)
            if self._min:
                q = f"(?!{self._build_range(self._min - 1)})" + q
            self._D_value = q
        return super().build()

    def _build_range(self, number):
        if number == 0:
            return "0"
        number_str = str(number)
        final_build = R()

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

        final_build |= R(number_str)
        return final_build.build()


class Unicode(OORegexBase):
    _D_value: OORValue = r"\X"


class NewLine(OORegexBase):
    _D_value: OORValue = r"\R"


class VerticalWhitespace(OORegexBase):
    _D_value: OORValue = r"\v"


class HorizontalWhitespace(OORegexBase):
    _D_value: OORValue = r"\h"


class Blank(OORegexBase):
    _D_value: OORValue = "[:blank:]"

    def __neg__(self):
        return Visible()


class Control(OORegexBase):
    _D_value: OORValue = "[:cntrl:]"


class Visible(OORegexBase):
    _D_value: OORValue = "[:print:]"

    def __neg__(self):
        return Blank()


class Punctuation(OORegexBase):
    _D_value: OORValue = f"[{string.punctuation}]"


class WhiteSpace(OORegexBase):
    _D_value: OORValue = r"\s"


class Word(OORegexBase):
    _D_value: OORValue = r"\w"


class Hexadecimal(OORegexBase):
    _D_value: OORValue = "[:xdigit:]"
