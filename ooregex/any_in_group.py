import string
from typing import Optional

from ooregex.OORegex import OORValue, OORegexBase, R
from ooregex.number_range_to_regex import regex_for_range


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
    _D_value: OORValue = r"\d"

    def __init__(
        self,
        min: Optional[int] = None,
        max: Optional[int] = None,
        zfill: bool = False,
        optional_zfill: bool = False,
        **kwargs,
    ):
        if max is not None:
            assert min is not None
            assert max > min
        if min is not None:
            assert max is not None
        assert not zfill or not optional_zfill

        self._min = min
        self._max = max
        self._zfill = zfill
        self._optional_zfill = optional_zfill
        super().__init__(**kwargs)

    def build(self) -> str:
        if self._max is not None:
            q = regex_for_range(self._min, self._max, self._zfill, self._optional_zfill)
            self._value = q
        else:
            self._value = self._D_value
        return super().build()


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
